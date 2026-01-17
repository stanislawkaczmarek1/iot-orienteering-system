from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.core.db import Base

if TYPE_CHECKING:
  from app.models.race import RaceCheckpoint
  

class Checkpoint(Base):
  __tablename__ = "checkpoints"
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(30))

  race_checkpoints: Mapped[List["RaceCheckpoint"]] = relationship(
    "RaceCheckpoint",
    back_populates="checkpoint",
    cascade="all, delete-orphan",
  )
