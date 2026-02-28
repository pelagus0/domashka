from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from appbooster_app.db import Base


class Experiment(Base):
    __tablename__ = "experiments"
    __table_args__ = (UniqueConstraint("key", name="uq_experiments_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    options: Mapped[list[ExperimentOption]] = relationship(
        back_populates="experiment",
        cascade="all, delete-orphan",
    )


class ExperimentOption(Base):
    __tablename__ = "experiment_options"
    __table_args__ = (
        UniqueConstraint("experiment_id", "value", name="uq_option_value"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"))
    value: Mapped[str] = mapped_column(String, nullable=False)
    weight_bps: Mapped[int] = mapped_column(Integer, nullable=False)

    experiment: Mapped[Experiment] = relationship(back_populates="options")


class Device(Base):
    __tablename__ = "devices"
    __table_args__ = (UniqueConstraint("token", name="uq_devices_token"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )


class Assignment(Base):
    __tablename__ = "assignments"
    __table_args__ = (
        UniqueConstraint(
            "device_id",
            "experiment_id",
            name="uq_assignments_device_experiment",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"))
    option_value: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

