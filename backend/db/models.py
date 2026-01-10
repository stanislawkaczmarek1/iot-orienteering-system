from datetime import datetime
from typing import List

from sqlalchemy import create_engine, select, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, relationship
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    def __repr__(self):
        # Collect all column names and values
        values = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
        }
        values_str = ", ".join(f"{k}={v!r}" for k, v in values.items())
        return f"{self.__class__.__name__}({values_str})"


class Runner(Base):
    __tablename__ = "runners"
    id: Mapped[int] = mapped_column(primary_key=True)
    rfid_uid: Mapped[str] = mapped_column(String(30))  # todo check
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))

    race_runners: Mapped[List["RaceRunner"]] = relationship(
        "RaceRunner",
        back_populates="runner",
        cascade="all, delete-orphan",
    )


class Checkpoint(Base):
    __tablename__ = "checkpoints"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    race_checkpoints: Mapped[List["RaceCheckpoint"]] = relationship(
        "RaceCheckpoint",
        back_populates="checkpoint",
        cascade="all, delete-orphan",
    )


class Race(Base):
    __tablename__ = "races"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime] = mapped_column(DateTime)
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


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    runner_id: Mapped[int] = mapped_column(ForeignKey("runners.id", ondelete="CASCADE"))
    checkpoint_id: Mapped[int] = mapped_column(ForeignKey("checkpoints.id", ondelete="CASCADE"))
    race_id: Mapped[int] = mapped_column(ForeignKey("races.id", ondelete="CASCADE"))
    timestamp: Mapped[datetime] = mapped_column(DateTime)

    runner: Mapped[Runner] = relationship(
        "Runner",
    )

    checkpoint: Mapped[Checkpoint] = relationship(
        "Checkpoint",
    )

    race: Mapped[Race] = relationship(
        "Race"
    )


class RaceCheckpoint(Base):
    __tablename__ = "race_checkpoints"
    race_id: Mapped[int] = mapped_column(ForeignKey("races.id"), primary_key=True,
                                         autoincrement=False)
    checkpoint_id: Mapped[int] = mapped_column(ForeignKey("checkpoints.id"), primary_key=True,
                                               autoincrement=False)

    race: Mapped[Race] = relationship(
        "Race",
        back_populates="race_checkpoints",
    )
    checkpoint: Mapped[Checkpoint] = relationship(
        "Checkpoint",
        back_populates="race_checkpoints",
    )


class RaceRunner(Base):
    __tablename__ = "race_runners"
    race_id: Mapped[int] = mapped_column(ForeignKey("races.id"), primary_key=True,
                                         autoincrement=False)
    runner_id: Mapped[int] = mapped_column(ForeignKey("runners.id"), primary_key=True,
                                           autoincrement=False)

    runner: Mapped[Runner] = relationship(
        "Runner",
        back_populates="race_runners",
    )
    race: Mapped[Race] = relationship(
        "Race",
        back_populates="race_runners",
    )
