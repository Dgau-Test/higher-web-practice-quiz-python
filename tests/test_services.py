import pytest
from django.http import Http404

from quiz.models import Category, Difficulty, Question, Quiz
from quiz.services.category import CategoryService
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService


@pytest.mark.django_db
class TestCategoryService:
    """Тесты CategoryService."""

    def setup_method(self) -> None:
        """Подготавливает сервис."""
        self.service = CategoryService()

    def test_create_update_delete(self) -> None:
        """Проверяет CRUD для категории."""
        category = self.service.create_category('Science')
        assert self.service.get_category(category.id).title == 'Science'

        updated = self.service.update_category(category.id, {'title': 'Math'})
        assert updated.title == 'Math'

        self.service.delete_category(category.id)
        assert Category.objects.count() == 0

    def test_list_categories_returns_created_items(self) -> None:
        """Проверяет list_categories для созданных категорий."""
        self.service.create_category('Cat 1')
        self.service.create_category('Cat 2')

        categories = self.service.list_categories()
        assert len(categories) == 2
        assert {item.title for item in categories} == {'Cat 1', 'Cat 2'}

    def test_get_missing_category_raises_404(self) -> None:
        """Проверяет, что несуществующая категория вызывает 404."""
        with pytest.raises(Http404):
            self.service.get_category(9999)


@pytest.mark.django_db
class TestQuizService:
    """Тесты QuizService."""

    def setup_method(self) -> None:
        """Подготавливает сервис."""
        self.service = QuizService()

    def test_crud_and_filter_by_title(self) -> None:
        """Проверяет CRUD и поиск по title."""
        quiz = self.service.create_quiz(
            {'title': 'Python Basics', 'description': 'desc'}
        )
        self.service.create_quiz(
            {'title': 'Python Advanced', 'description': ''}
        )

        assert len(self.service.list_quizzes()) == 2
        assert len(self.service.get_quizes_by_title('Basics')) == 1

        updated = self.service.update_quiz(
            quiz.id, {'title': 'Python Intro', 'description': 'new'}
        )
        assert updated.title == 'Python Intro'

        self.service.delete_quiz(quiz.id)
        assert Quiz.objects.count() == 1

    def test_get_missing_quiz_raises_404(self) -> None:
        """Проверяет, что несуществующий квиз вызывает 404."""
        with pytest.raises(Http404):
            self.service.get_quiz(9999)


@pytest.mark.django_db
class TestQuestionService:
    """Тесты QuestionService."""

    def setup_method(self) -> None:
        """Подготавливает сервис и фикстуры."""
        self.service = QuestionService()
        self.category = Category.objects.create(title='Backend')
        self.quiz = Quiz.objects.create(title='Django')

    def test_list_questions_returns_created_items(self) -> None:
        """Проверяет list_questions для созданных вопросов."""
        Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            text='Q1',
            options=['A', 'B'],
            correct_answer='A',
            difficulty=Difficulty.EASY,
        )
        Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            text='Q2',
            options=['A', 'B'],
            correct_answer='B',
            difficulty=Difficulty.MEDIUM,
        )

        questions = self.service.list_questions()
        assert len(questions) == 2
        assert {item.text for item in questions} == {'Q1', 'Q2'}

    def test_question_main_methods(self) -> None:
        """Проверяет основные методы QuestionService."""
        question = self.service.create_question(
            self.quiz.id,
            {
                'category': self.category.id,
                'text': 'Что такое ORM?',
                'description': '',
                'options': ['A', 'B'],
                'correct_answer': 'A',
                'explanation': '',
                'difficulty': Difficulty.EASY,
            },
        )
        assert self.service.get_question(question.id).text == 'Что такое ORM?'
        assert len(self.service.get_questions_by_text('ORM')) == 1
        assert len(self.service.get_questions_for_quiz(self.quiz.id)) == 1
        assert self.service.check_answer(question.id, 'a') is True

        updated = self.service.update_question(
            question.id, {'text': 'Новый текст', 'difficulty': Difficulty.HARD}
        )
        assert updated.text == 'Новый текст'
        assert (
            self.service.random_question_from_quiz(self.quiz.id).id
            == question.id
        )

        self.service.delete_question(question.id)
        assert Question.objects.count() == 0

    def test_check_answer_false_case(self) -> None:
        """Проверяет отрицательный сценарий check_answer."""
        question = Question.objects.create(
            quiz=self.quiz,
            category=self.category,
            text='2 + 2 = ?',
            options=['3', '4'],
            correct_answer='4',
            difficulty=Difficulty.EASY,
        )
        assert self.service.check_answer(question.id, '3') is False

    def test_random_question_for_empty_quiz_raises(self) -> None:
        """Проверяет ошибку при запросе случайного вопроса у пустого квиза."""
        empty_quiz = Quiz.objects.create(title='Empty quiz')
        with pytest.raises(Question.DoesNotExist):
            self.service.random_question_from_quiz(empty_quiz.id)

    def test_get_missing_question_raises_404(self) -> None:
        """Проверяет, что несуществующий вопрос вызывает 404."""
        with pytest.raises(Http404):
            self.service.get_question(9999)
