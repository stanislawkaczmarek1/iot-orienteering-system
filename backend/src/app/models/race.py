from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.core.db import Base

from app.models.event import Event

if TYPE_CHECKING:
  from app.models.runner import Runner
  from app.models.checkpoint import Checkpoint


class Race(Base):
  __tablename__ = "races"
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(30))
  date: Mapped[datetime] = mapped_column(DateTime)
  location: Mapped[str] = mapped_column(String(30))
  is_active: Mapped[bool] = mapped_column(Boolean)

  race_runners: Mapped[List["RaceRunner"]] = relationship(
    "RaceRunner",
    back_populates="race",
    cascade="all, delete-orphan"
  )
  race_checkpoints: Mapped[List["RaceCheckpoint"]] = relationship(
    "RaceCheckpoint",
    back_populates="race",
    cascade="all, delete-orphan",
  )
  events: Mapped[List[Event]] = relationship(
    "Event",
    back_populates="race",
    cascade="all, delete-orphan"
  )


class RaceCheckpoint(Base):
  __tablename__ = "race_checkpoints"
  race_id: Mapped[int] = mapped_column(
    ForeignKey("races.id"),
    primary_key=True,
    autoincrement=False
  )
  checkpoint_id: Mapped[int] = mapped_column(
    ForeignKey("checkpoints.id"),
    primary_key=True,
    autoincrement=False
  )

  order: Mapped[int] = mapped_column(Integer)

  race: Mapped["Race"] = relationship(
    "Race",
    back_populates="race_checkpoints",
  )
  checkpoint: Mapped["Checkpoint"] = relationship(
    "Checkpoint",
    back_populates="race_checkpoints",
  )


class RaceRunner(Base):
  __tablename__ = "race_runners"
  race_id: Mapped[int] = mapped_column(
    ForeignKey("races.id"),
    primary_key=True,
    autoincrement=False
  )
  runner_id: Mapped[int] = mapped_column(
    ForeignKey("runners.id"),
    primary_key=True,
    autoincrement=False
  )

  runner: Mapped["Runner"] = relationship(
    "Runner",
    back_populates="race_runners",
  )
  race: Mapped["Race"] = relationship(
    "Race",
    back_populates="race_runners",
  )
