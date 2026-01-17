from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.core.db import Base

if TYPE_CHECKING:
  from app.models.runner import Runner
  from app.models.checkpoint import Checkpoint
  from app.models.race import Race


class Event(Base):
  __tablename__ = "events"
  id: Mapped[int] = mapped_column(primary_key=True)
  runner_id: Mapped[int] = mapped_column(ForeignKey("runners.id", ondelete="CASCADE"))
  checkpoint_id: Mapped[int] = mapped_column(ForeignKey("checkpoints.id", ondelete="CASCADE"))
  race_id: Mapped[int] = mapped_column(ForeignKey("races.id", ondelete="CASCADE"))
  timestamp: Mapped[datetime] = mapped_column(DateTime)

  runner: Mapped["Runner"] = relationship("Runner")
  checkpoint: Mapped["Checkpoint"] = relationship("Checkpoint")
  race: Mapped["Race"] = relationship("Race")
