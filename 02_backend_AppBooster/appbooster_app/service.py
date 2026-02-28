from __future__ import annotations

import hashlib

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from appbooster_app.models import Assignment, Device, Experiment, ExperimentOption

BPS_TOTAL = 10_000


def _hash_to_bps(device_token: str, experiment_key: str) -> int:
    payload = f"{experiment_key}:{device_token}".encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    as_int = int.from_bytes(digest[:8], byteorder="big", signed=False)
    return as_int % BPS_TOTAL


def get_or_create_device(db_session: Session, token: str) -> Device:
    device = db_session.execute(
        select(Device).where(Device.token == token).limit(1),
    ).scalar_one_or_none()
    if device is not None:
        return device

    device = Device(token=token)
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)
    return device


def list_known_experiments_for_device(
    db_session: Session,
    device: Device,
) -> list[Experiment]:
    # Experiments created after device first_seen_at are NOT visible to device.
    statement = select(Experiment).where(Experiment.created_at <= device.first_seen_at)
    return list(db_session.execute(statement).scalars().all())


def get_assignment(
    db_session: Session,
    device_id: int,
    experiment_id: int,
) -> Assignment | None:
    statement = (
        select(Assignment)
        .where(Assignment.device_id == device_id)
        .where(Assignment.experiment_id == experiment_id)
        .limit(1)
    )
    return db_session.execute(statement).scalar_one_or_none()


def choose_option_value(device_token: str, experiment: Experiment) -> str:
    bps = _hash_to_bps(device_token, experiment.key)
    cumulative = 0
    for option in experiment.options:
        cumulative += option.weight_bps
        if bps < cumulative:
            return option.value
    return experiment.options[-1].value


def get_or_create_assignment(
    db_session: Session,
    device: Device,
    experiment: Experiment,
) -> Assignment:
    existing = get_assignment(db_session, device.id, experiment.id)
    if existing is not None:
        return existing

    option_value = choose_option_value(device.token, experiment)
    assignment = Assignment(
        device_id=device.id,
        experiment_id=experiment.id,
        option_value=option_value,
    )
    db_session.add(assignment)
    db_session.commit()
    db_session.refresh(assignment)
    return assignment


def ensure_seed_experiments(db_session: Session) -> None:
    if db_session.execute(select(Experiment.id).limit(1)).scalar_one_or_none():
        return

    button = Experiment(key="button_color")
    button.options = [
        ExperimentOption(value="#FF0000", weight_bps=3334),
        ExperimentOption(value="#00FF00", weight_bps=3333),
        ExperimentOption(value="#0000FF", weight_bps=3333),
    ]

    price = Experiment(key="price")
    price.options = [
        ExperimentOption(value="10", weight_bps=7500),
        ExperimentOption(value="20", weight_bps=1000),
        ExperimentOption(value="50", weight_bps=500),
        ExperimentOption(value="5", weight_bps=1000),
    ]

    db_session.add_all([button, price])
    db_session.commit()


def get_stats(db_session: Session) -> list[dict[str, object]]:
    experiments = list(db_session.execute(select(Experiment)).scalars().all())
    result: list[dict[str, object]] = []
    for experiment in experiments:
        total = db_session.execute(
            select(func.count(Assignment.id)).where(
                Assignment.experiment_id == experiment.id,
            ),
        ).scalar_one()

        rows = db_session.execute(
            select(Assignment.option_value, func.count(Assignment.id))
            .where(Assignment.experiment_id == experiment.id)
            .group_by(Assignment.option_value),
        ).all()
        result.append(
            {
                "key": experiment.key,
                "created_at": experiment.created_at,
                "total_devices": int(total),
                "options": [
                    {"value": value, "devices": int(count)} for value, count in rows
                ],
            },
        )
    return result

