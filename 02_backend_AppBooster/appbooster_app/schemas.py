from datetime import datetime

from pydantic import BaseModel


class ExperimentOut(BaseModel):
    key: str
    value: str


class StatsOptionOut(BaseModel):
    value: str
    devices: int


class StatsExperimentOut(BaseModel):
    key: str
    created_at: datetime
    total_devices: int
    options: list[StatsOptionOut]

