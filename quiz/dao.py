from abc import ABC, abstractmethod

from quiz.models import Quiz, Question, Category


class AbstractCategoryService(ABC):
    """Интерфейс для работы c категориями"""

    @abstractmethod
    def list_categories(self) -> list[Category]:
        """Метод для получения списка категорий"""
        ...

    @abstractmethod
    def get_category(self, category_id: int) -> Category:
        """
        Метод для получения категории по идентификатору.

        :param category_id: Идентификатор категории.
        :return: Категория из БД.
        """
        ...

    @abstractmethod
    def create_category(self, title: str) -> Category:
        """
        Создает категорию вопросов.

        :param title: Название для категории.
        :return: Созданная категория.
        """
        ...

    @abstractmethod
    def update_category(self, category_id: int, data: dict) -> Category:
        """
        Обновляет категорию новыми данными.

        :param category_id: Идентификатор категории.
        :param data: Данные для обновления категории.
        :return: Обновленная категория.
        """
        ...

    @abstractmethod
    def delete_category(self, category_id: int) -> None:
        """
        Удаляет категорию.

        :param category_id: Идентификатор категории для удаления.
        """
        ...


class AbstractQuizService(ABC):
    """Интерфейс для работы с квизами"""

    @abstractmethod
    def list_quizzes(self) -> list[Quiz]:
        """Возвращает список всех квизов."""
        ...

    @abstractmethod
    def get_quiz(self, quiz_id: int) -> Quiz:
        """
        Возвращает квиз по его идентификатору.

        :param quiz_id: Идентификатор квиза.
        :return: Квиз из БД.
        """
        ...

    @abstractmethod
    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        """
        Возвращает список квизов по названию.

        :param title: Название квиза.
        :return: Список квизов с подходящими названиями.
        """
        ...

    @abstractmethod
    def create_quiz(self, data: dict) -> Quiz:
        """
        Создает новый квиз.

        :param data: Данные из запроса для создания квиза.
        :return: Созданный квиз.
        """
        ...

    @abstractmethod
    def update_quiz(self, quiz_id: int, data: dict) -> Quiz:
        """
        Обновляет существующий квиз.

        :param quiz_id: Идентификатор квиза.
        :param data: Данные для обновления квиза.
        :return: Обновленный квиз.
        """
        ...

    @abstractmethod
    def delete_quiz(self, quiz_id: int) -> None:
        """
        Удаляет квиз по его идентификатору.

        :param quiz_id: Идентификатор квиза для удаления.
        """
        ...


class AbstractQuestionService(ABC):
    """Интерфейс для работы с вопросами"""

    @abstractmethod
    def list_questions(self) -> list[Question]:
        """
        Возвращает список всех вопросов.

        :return: Список вопросов.
        """
        ...

    @abstractmethod
    def get_question(self, question_id: int) -> Question:
        """
        Возвращает вопрос по его идентификатору.

        :param question_id: Идентификатор вопроса.
        :return: Вопрос из БД.
        """
        ...

    @abstractmethod
    def get_questions_by_text(self, text: str) -> list[Question]:
        """
        Возвращает вопрос по его тексту.

        :param text: Текст вопроса.
        :return: Вопрос из БД.
        """
        ...

    @abstractmethod
    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        """
        Получение вопросов по идентификатору квиза.

        :param quiz_id: Идентификатор квиза.
        :return: Список вопросов квиза.
        """
        ...

    @abstractmethod
    def create_question(self, quiz_id: int, data: dict) -> Question:
        """
        Создает новый вопрос.

        :param quiz_id: Идентификатор квиза, к которому относится вопрос.
        :param data: Данные из запроса для создания вопроса.
        :return: Созданный вопрос.
        """
        ...

    @abstractmethod
    def update_question(self, question_id: int, data: dict) -> Question:
        """
        Обновляет существующий вопрос.

        :param question_id: Идентификатор вопроса.
        :param data: Данные для обновления вопроса.
        :return: Обновленный вопрос.
        """
        ...

    @abstractmethod
    def delete_question(self, question_id: int) -> None:
        """
        Удаляет вопрос по его идентификатору.

        :param question_id: Идентификатор вопроса для удаления.
        """
        ...

    @abstractmethod
    def check_answer(self, question_id: int, answer: str) -> bool:
        """
        Проверяет ответ на вопрос.

        :param question_id: Идентификатор вопроса.
        :param answer: Ответ пользователя.
        :return: True, если ответ правильный, False - в противном случае.
        """
        ...

    @abstractmethod
    def random_question_from_quiz(self, quiz_id: int) -> Question:
        """
        Возвращает случайный вопрос из указанного квиза.

        :param quiz_id: Идентификатор квиза.
        :return: Случайный вопрос из квиза.
        """
        ...
