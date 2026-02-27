from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import httpx
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from bewise_app.models import Question


@dataclass(frozen=True, slots=True)
class RemoteQuestion:
    question_id: int
    question: str
    answer: str
    created_at: datetime


def _parse_datetime(value: str) -> datetime:
    # jservice returns ISO strings, sometimes with Z suffix.
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def fetch_random_question(client: httpx.Client) -> RemoteQuestion:
    response = client.get(
        "https://jservice.io/api/random",
        params={"count": 1},
        timeout=10.0,
    )
    response.raise_for_status()
    payload = response.json()
    item = payload[0]
    return RemoteQuestion(
        question_id=int(item["id"]),
        question=str(item["question"]),
        answer=str(item["answer"]),
        created_at=_parse_datetime(str(item["created_at"])),
    )


def get_last_saved_question(db_session: Session) -> Question | None:
    statement = select(Question).order_by(desc(Question.inserted_at)).limit(1)
    return db_session.execute(statement).scalar_one_or_none()


def question_exists(db_session: Session, question_id: int) -> bool:
    statement = select(Question.id).where(Question.question_id == question_id).limit(1)
    return db_session.execute(statement).scalar_one_or_none() is not None


def save_unique_questions(db_session: Session, questions_num: int) -> None:
    with httpx.Client() as client:
        saved = 0
        while saved < questions_num:
            remote_question = fetch_random_question(client)
            if question_exists(db_session, remote_question.question_id):
                continue

            db_question = Question(
                question_id=remote_question.question_id,
                question=remote_question.question,
                answer=remote_question.answer,
                created_at=remote_question.created_at,
            )
            db_session.add(db_question)
            db_session.commit()
            saved += 1

