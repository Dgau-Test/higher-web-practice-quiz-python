"""Тесты API слоя."""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from quiz.models import Category, Difficulty, Question, Quiz


@pytest.mark.django_db
class TestCategoryAPI:
    """Тесты API категорий."""

    def test_category_crud(self, client: Client) -> None:
        """Проверяет CRUD-эндпоинты категории."""
        create_response = client.post(
            reverse('category-list-create'),
            {'title': 'History'},
            content_type='application/json',
        )
        assert create_response.status_code == HTTPStatus.CREATED
        category_id = create_response.json()['id']

        list_response = client.get(reverse('category-list-create'))
        assert list_response.status_code == HTTPStatus.OK
        assert list_response.json()[0]['title'] == 'History'

        get_response = client.get(
            reverse('category-detail', kwargs={'id': category_id})
        )
        assert get_response.status_code == HTTPStatus.OK

        update_response = client.put(
            reverse('category-detail', kwargs={'id': category_id}),
            {'title': 'World History'},
            content_type='application/json',
        )
        assert update_response.status_code == HTTPStatus.OK
        assert update_response.json()['title'] == 'World History'

        delete_response = client.delete(
            reverse('category-detail', kwargs={'id': category_id})
        )
        assert delete_response.status_code == HTTPStatus.NO_CONTENT

    def test_category_404_on_missing_id(self, client: Client) -> None:
        """Проверяет ответ 404 для несуществующей категории."""
        response = client.get(reverse('category-detail', kwargs={'id': 9999}))
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
class TestQuizAndQuestionAPI:
    """Тесты API квизов и вопросов."""

    def _create_quiz_question(self) -> tuple[int, int]:
        """Создает базовые данные для тестов и возвращает id квиза/вопроса."""
        category = Category.objects.create(title='Algorithms')
        quiz = Quiz.objects.create(title='CS Quiz', description='base')
        question = Question.objects.create(
            quiz=quiz,
            category=category,
            text='Сложность O(1)?',
            description='',
            options=['Да', 'Нет'],
            correct_answer='Да',
            explanation='Это константа',
            difficulty=Difficulty.MEDIUM,
        )
        return quiz.id, question.id

    def test_quiz_and_question_endpoints(self, client: Client) -> None:
        """Проверяет специализированные endpoints квизов и вопросов."""
        category = Category.objects.create(title='Algorithms')
        quiz_response = client.post(
            reverse('quiz-list-create'),
            {'title': 'CS Quiz', 'description': 'base'},
            content_type='application/json',
        )
        assert quiz_response.status_code == HTTPStatus.CREATED
        quiz_id = quiz_response.json()['id']

        question_response = client.post(
            reverse('question-list-create'),
            {
                'quiz': quiz_id,
                'category': category.id,
                'text': 'Сложность O(1)?',
                'description': '',
                'options': ['Да', 'Нет'],
                'correct_answer': 'Да',
                'explanation': 'Это константа',
                'difficulty': Difficulty.MEDIUM,
            },
            content_type='application/json',
        )
        assert question_response.status_code == HTTPStatus.CREATED
        question_id = question_response.json()['id']

        quizzes_list = client.get(reverse('quiz-list-create'))
        assert quizzes_list.status_code == HTTPStatus.OK
        assert len(quizzes_list.json()) == 1

        questions_list = client.get(reverse('question-list-create'))
        assert questions_list.status_code == HTTPStatus.OK
        assert len(questions_list.json()) == 1

        by_title = client.get(reverse('quiz-by-title', kwargs={'title': 'CS'}))
        assert by_title.status_code == HTTPStatus.OK
        assert len(by_title.json()) == 1

        random_question = client.get(
            reverse('quiz-random-question', kwargs={'id': quiz_id})
        )
        assert random_question.status_code == HTTPStatus.OK
        assert random_question.json()['id'] == question_id

        by_text = client.get(
            reverse('question-by-text', kwargs={'text': 'O(1)'})
        )
        assert by_text.status_code == HTTPStatus.OK
        assert by_text.json()[0]['id'] == question_id

        check = client.post(
            reverse('question-check', kwargs={'id': question_id}),
            {'answer': 'Да'},
            content_type='application/json',
        )
        assert check.status_code == HTTPStatus.OK
        assert check.json()['is_correct'] is True

        wrong_check = client.post(
            reverse('question-check', kwargs={'id': question_id}),
            {'answer': 'Нет'},
            content_type='application/json',
        )
        assert wrong_check.status_code == HTTPStatus.OK
        assert wrong_check.json()['is_correct'] is False

        detail = client.get(
            reverse('question-detail', kwargs={'id': question_id})
        )
        assert detail.status_code == HTTPStatus.OK

        update_quiz = client.put(
            reverse('quiz-detail', kwargs={'id': quiz_id}),
            {'title': 'CS Quiz 2', 'description': 'updated'},
            content_type='application/json',
        )
        assert update_quiz.status_code == HTTPStatus.OK

        delete_question = client.delete(
            reverse('question-detail', kwargs={'id': question_id})
        )
        assert delete_question.status_code == HTTPStatus.NO_CONTENT

        delete_quiz = client.delete(
            reverse('quiz-detail', kwargs={'id': quiz_id})
        )
        assert delete_quiz.status_code == HTTPStatus.NO_CONTENT

    def test_question_validation_errors(self, client: Client) -> None:
        """Проверяет валидационные ошибки создания вопроса."""
        category = Category.objects.create(title='Math')
        quiz = Quiz.objects.create(title='Basics')

        invalid_options = client.post(
            reverse('question-list-create'),
            {
                'quiz': quiz.id,
                'category': category.id,
                'text': '1+1?',
                'options': ['2'],
                'correct_answer': '2',
                'difficulty': Difficulty.EASY,
            },
            content_type='application/json',
        )
        assert invalid_options.status_code == HTTPStatus.BAD_REQUEST
        assert 'options' in invalid_options.json()

        invalid_answer = client.post(
            reverse('question-list-create'),
            {
                'quiz': quiz.id,
                'category': category.id,
                'text': '2+2?',
                'options': ['3', '4'],
                'correct_answer': '5',
                'difficulty': Difficulty.EASY,
            },
            content_type='application/json',
        )
        assert invalid_answer.status_code == HTTPStatus.BAD_REQUEST
        assert 'correct_answer' in invalid_answer.json()

    def test_check_answer_requires_nonempty_string(
        self, client: Client
    ) -> None:
        """Проверяет, что check требует непустое поле answer."""
        _, question_id = self._create_quiz_question()

        missing_answer = client.post(
            reverse('question-check', kwargs={'id': question_id}),
            {},
            content_type='application/json',
        )
        assert missing_answer.status_code == HTTPStatus.BAD_REQUEST

        empty_answer = client.post(
            reverse('question-check', kwargs={'id': question_id}),
            {'answer': '   '},
            content_type='application/json',
        )
        assert empty_answer.status_code == HTTPStatus.BAD_REQUEST

    def test_404_and_empty_cases(self, client: Client) -> None:
        """Проверяет 404-кейсы и пустой random_question."""
        missing_quiz = client.get(reverse('quiz-detail', kwargs={'id': 9999}))
        assert missing_quiz.status_code == HTTPStatus.NOT_FOUND

        missing_question = client.get(
            reverse('question-detail', kwargs={'id': 9999})
        )
        assert missing_question.status_code == HTTPStatus.NOT_FOUND

        empty_quiz = Quiz.objects.create(title='Empty')
        empty_random = client.get(
            reverse('quiz-random-question', kwargs={'id': empty_quiz.id})
        )
        assert empty_random.status_code == HTTPStatus.NOT_FOUND

    def test_quiz_detail_success(self, client: Client) -> None:
        """Проверяет успешное получение квиза по id."""
        quiz = Quiz.objects.create(title='Detail Quiz', description='desc')
        response = client.get(reverse('quiz-detail', kwargs={'id': quiz.id}))
        assert response.status_code == HTTPStatus.OK
        assert response.json()['id'] == quiz.id

    def test_question_update_success(self, client: Client) -> None:
        """Проверяет успешное обновление вопроса."""
        category = Category.objects.create(title='Update cat')
        quiz = Quiz.objects.create(title='Update quiz')
        question = Question.objects.create(
            quiz=quiz,
            category=category,
            text='old text',
            options=['a', 'b'],
            correct_answer='a',
            difficulty=Difficulty.EASY,
        )

        response = client.put(
            reverse('question-detail', kwargs={'id': question.id}),
            {
                'quiz': quiz.id,
                'category': category.id,
                'text': 'new text',
                'description': 'updated',
                'options': ['a', 'b', 'c'],
                'correct_answer': 'b',
                'explanation': 'because',
                'difficulty': Difficulty.HARD,
            },
            content_type='application/json',
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()['text'] == 'new text'
        assert response.json()['difficulty'] == Difficulty.HARD

    def test_put_delete_missing_entities_return_404(
        self, client: Client
    ) -> None:
        """Проверяет 404 для PUT/DELETE несуществующих question и quiz."""
        category = Category.objects.create(title='Miss cat')
        quiz = Quiz.objects.create(title='Miss quiz')

        put_missing_question = client.put(
            reverse('question-detail', kwargs={'id': 9999}),
            {
                'quiz': quiz.id,
                'category': category.id,
                'text': 'x',
                'description': '',
                'options': ['x', 'y'],
                'correct_answer': 'x',
                'explanation': '',
                'difficulty': Difficulty.EASY,
            },
            content_type='application/json',
        )
        assert put_missing_question.status_code == HTTPStatus.NOT_FOUND

        delete_missing_question = client.delete(
            reverse('question-detail', kwargs={'id': 9999})
        )
        assert delete_missing_question.status_code == HTTPStatus.NOT_FOUND

        put_missing_quiz = client.put(
            reverse('quiz-detail', kwargs={'id': 9999}),
            {'title': 'nope', 'description': ''},
            content_type='application/json',
        )
        assert put_missing_quiz.status_code == HTTPStatus.NOT_FOUND

        delete_missing_quiz = client.delete(
            reverse('quiz-detail', kwargs={'id': 9999})
        )
        assert delete_missing_quiz.status_code == HTTPStatus.NOT_FOUND

    def test_quiz_list_supports_title_query_filter(
        self, client: Client
    ) -> None:
        """Проверяет фильтрацию списка квизов по query-параметру title."""
        Quiz.objects.create(title='Python Basics')
        Quiz.objects.create(title='Java Basics')

        response = client.get(reverse('quiz-list-create'), {'title': 'Python'})
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) == 1
        assert response.json()[0]['title'] == 'Python Basics'

    def test_question_list_supports_text_and_quiz_query_filters(
        self, client: Client
    ) -> None:
        """Проверяет фильтрацию вопросов по text и quiz."""
        category = Category.objects.create(title='Filtering')
        quiz_1 = Quiz.objects.create(title='Quiz 1')
        quiz_2 = Quiz.objects.create(title='Quiz 2')
        Question.objects.create(
            quiz=quiz_1,
            category=category,
            text='Python question',
            options=['a', 'b'],
            correct_answer='a',
            difficulty=Difficulty.EASY,
        )
        Question.objects.create(
            quiz=quiz_2,
            category=category,
            text='Java question',
            options=['a', 'b'],
            correct_answer='b',
            difficulty=Difficulty.EASY,
        )

        response = client.get(
            reverse('question-list-create'),
            {'text': 'Python', 'quiz': quiz_1.id},
        )
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) == 1
        assert response.json()[0]['text'] == 'Python question'

    def test_quiz_list_ignores_blank_title_filter(
        self, client: Client
    ) -> None:
        """Проверяет, что пустой title-фильтр не сужает выдачу."""
        Quiz.objects.create(title='Quiz A')
        Quiz.objects.create(title='Quiz B')

        response = client.get(reverse('quiz-list-create'), {'title': ''})
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) == 2

    def test_question_list_ignores_invalid_quiz_filter_value(
        self, client: Client
    ) -> None:
        """Проверяет, что нечисловой quiz-фильтр не ломает endpoint."""
        category = Category.objects.create(title='Invalid quiz filter cat')
        quiz = Quiz.objects.create(title='Invalid quiz filter quiz')
        Question.objects.create(
            quiz=quiz,
            category=category,
            text='Edge question',
            options=['a', 'b'],
            correct_answer='a',
            difficulty=Difficulty.EASY,
        )

        response = client.get(reverse('question-list-create'), {'quiz': 'abc'})
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) == 1

    def test_quiz_list_combined_filters_no_match(
        self, client: Client
    ) -> None:
        """Проверяет комбинированный фильтр quiz без совпадений."""
        Quiz.objects.create(title='Python Advanced')
        Quiz.objects.create(title='Java Basics')

        response = client.get(
            reverse('quiz-list-create'),
            {'title': 'GoLang'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    def test_question_list_combined_filters_no_match(
        self, client: Client
    ) -> None:
        """Проверяет комбинированный фильтр question без совпадений."""
        category = Category.objects.create(title='Combined filter cat')
        quiz_1 = Quiz.objects.create(title='Combined quiz 1')
        quiz_2 = Quiz.objects.create(title='Combined quiz 2')
        Question.objects.create(
            quiz=quiz_1,
            category=category,
            text='Python decorators',
            options=['a', 'b'],
            correct_answer='a',
            difficulty=Difficulty.EASY,
        )
        Question.objects.create(
            quiz=quiz_2,
            category=category,
            text='Java streams',
            options=['a', 'b'],
            correct_answer='b',
            difficulty=Difficulty.MEDIUM,
        )

        response = client.get(
            reverse('question-list-create'),
            {'text': 'Python', 'quiz': quiz_2.id},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []
