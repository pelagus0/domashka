from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from appbooster_app.db import get_db
from appbooster_app.schemas import ExperimentOut, StatsExperimentOut
from appbooster_app.service import (
    ensure_seed_experiments,
    get_or_create_assignment,
    get_or_create_device,
    get_stats,
    list_known_experiments_for_device,
)

router = APIRouter(prefix="/api/v1")


@router.get("/experiments", response_model=list[ExperimentOut])
def get_experiments(
    device_token: str | None = Header(default=None, alias="Device-Token"),
    db_session: Session = Depends(get_db),
) -> list[ExperimentOut]:
    if not device_token:
        raise HTTPException(status_code=400, detail="Device-Token header is required")

    ensure_seed_experiments(db_session)
    device = get_or_create_device(db_session, device_token)
    experiments = list_known_experiments_for_device(db_session, device)

    out: list[ExperimentOut] = []
    for experiment in experiments:
        assignment = get_or_create_assignment(db_session, device, experiment)
        out.append(ExperimentOut(key=experiment.key, value=assignment.option_value))
    return out


@router.get("/stats", response_model=list[StatsExperimentOut])
def stats(db_session: Session = Depends(get_db)) -> list[StatsExperimentOut]:
    ensure_seed_experiments(db_session)
    raw = get_stats(db_session)
    return [StatsExperimentOut.model_validate(item) for item in raw]

