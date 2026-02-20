from datetime import datetime

from pydantic import BaseModel, Field


class QuestionsRequest(BaseModel):
    questions_num: int = Field(ge=1, le=100)


class QuestionOut(BaseModel):
    question_id: int
    question: str
    answer: str
    created_at: datetime

