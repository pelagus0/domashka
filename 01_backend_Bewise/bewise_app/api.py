"""
API endpoints для управления вопросами викторины.

Этот модуль реализует REST API для сервиса вопросов Bewise.
Он обрабатывает HTTP-запросы, валидирует входные данные через Pydantic схемы,
и использует сервисный слой для выполнения бизнес-логики.

Основные компоненты:
- create_questions: создает указанное количество уникальных вопросов
- Использует внешний API для получения новых вопросов
- Гарантирует уникальность сохраняемых вопросов

Эндпоинты:
    POST /api/v1/questions - Создание новых вопросов
        Принимает: {"questions_num": integer}
        Возвращает: последний сохраненный вопрос или пустой объект

Зависимости:
    - FastAPI
    - SQLAlchemy (PostgreSQL)
    - Pydantic для валидации
"""

from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from bewise_app.db import get_db
from bewise_app.schemas import QuestionOut, QuestionsRequest
from bewise_app.service import get_last_saved_question, save_unique_questions

router = APIRouter(prefix="/api/v1")


@router.post(
    "/questions",
    response_model=QuestionOut | dict[str, str],
    description="""
    Создает указанное количество уникальных вопросов.

    Процесс:
    1. Получает вопросы из внешнего API
    2. Проверяет их уникальность в БД
    3. Сохраняет только уникальные вопросы
    4. Возвращает последний сохраненный вопрос

    Возможные ошибки:
    - 400: Неверный формат запроса (questions_num должно быть > 0)
    - 422: Ошибка валидации данных
    - 500: Ошибка при обращении к внешнему API
    """,
    responses={
        200: {
            "description": "Успешное создание вопросов",
            "model": QuestionOut
        },
        400: {
            "description": "Неверный формат запроса",
            "content": {
                "application/json": {
                    "example": {"detail": "questions_num должно быть больше 0"}
                }
            }
        },
        422: {
            "description": "Ошибка валидации",
            "content": {
                "application/json": {
                    "example": {"detail": "Ошибка валидации"}
                }
            }
        },
        500: {
            "description": "Ошибка сервера",
            "content": {
                "application/json": {
                    "example": {"detail": "Не удалось получить вопросы из внешнего API"}
                }
            }
        }
    }
)
def create_questions(
        body: QuestionsRequest,
        db_session: Session = Depends(get_db),
) -> QuestionOut | dict[str, str]:
    """
    Создает новые уникальные вопросы.

    Args:
        body: запрос с количеством вопросов (questions_num)
        db_session: сессия базы данных (внедряется через Depends)

    Returns:
        QuestionOut: последний сохраненный вопрос
        {}: пустой словарь, если не было сохраненных вопросов

    Raises:
        HTTPException: при ошибках валидации или работе с внешним API
    """
    # Проверка входных данных
    if body.questions_num <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="questions_num должно быть больше 0"
        )

    # Получаем последний вопрос до сохранения новых
    previous = get_last_saved_question(db_session)

    try:
        # Сохраняем уникальные вопросы
        save_unique_questions(db_session, body.questions_num)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении вопросов: {str(e)}"
        )

    # Если не было предыдущих вопросов, возвращаем пустой объект
    if previous is None:
        return {}

    # Возвращаем последний вопрос (который был до сохранения новых)
    return QuestionOut(
        question_id=previous.question_id,
        question=previous.question,
        answer=previous.answer,
        created_at=previous.created_at,
    )