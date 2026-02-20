from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from bewise_app.db import get_db
from bewise_app.schemas import QuestionOut, QuestionsRequest
from bewise_app.service import get_last_saved_question, save_unique_questions

router = APIRouter(prefix="/api/v1")


@router.post("/questions", response_model=QuestionOut | dict[str, Any])
def create_questions(
    body: QuestionsRequest,
    db_session: Session = Depends(get_db),
) -> Any:
    previous = get_last_saved_question(db_session)
    save_unique_questions(db_session, body.questions_num)

    if previous is None:
        return {}

    return QuestionOut(
        question_id=previous.question_id,
        question=previous.question,
        answer=previous.answer,
        created_at=previous.created_at,
    )

