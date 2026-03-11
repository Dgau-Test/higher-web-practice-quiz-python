# Quiz API

Quiz API - backend-сервис для платформы викторин (квизов) с категориями, вопросами и проверкой ответов.

## Возможности
- CRUD для категорий, квизов и вопросов.
- Получение случайного вопроса из квиза.
- Поиск квизов по части названия.
- Поиск вопросов по части текста.
- Проверка правильности ответа на вопрос.
- Версионирование API (`/api/v1/...`, заготовка `/api/v2/...`).
- Swagger/ReDoc документация.

## Технологии
- Python 3.10+
- Django
- Django REST Framework
- drf-yasg
- SQLite (по умолчанию)
- pytest
- ruff

## Как запустить локально
1. Клонируйте репозиторий:

```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd higher-web-practice-quiz-python-main
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# или
call venv\Scripts\activate     # Windows
```

3. Установите зависимости:

```bash
uv sync
```

4. Примените миграции:

```bash
python manage.py migrate
```

5. Запустите сервер:

```bash
python manage.py runserver
```

Документация API:
- Swagger: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## Примеры запросов

### Создание категории
`POST /api/v1/category`

```json
{
  "title": "History"
}
```

### Создание квиза
`POST /api/v1/quiz`

```json
{
  "title": "World History",
  "description": "Базовые вопросы по истории"
}
```

### Создание вопроса
`POST /api/v1/question`

```json
{
  "quiz": 1,
  "category": 1,
  "text": "В каком году была принята Конституция США?",
  "description": "Один правильный ответ",
  "options": ["1776", "1787", "1804"],
  "correct_answer": "1787",
  "explanation": "Конституция принята в 1787 году",
  "difficulty": "medium"
}
```

### Проверка ответа
`POST /api/v1/question/1/check`

```json
{
  "answer": "1787"
}
```

Ответ:

```json
{
  "is_correct": true
}
```

## Тесты и линтинг

```bash
ruff check ./project ./quiz ./tests
pytest -q
```

## Автор
Проект выполнен Вакуленко Артемом в рамках НИР от Яндекс Практикума.
