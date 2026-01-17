from typing import TYPE_CHECKING, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.core.db import Base

if TYPE_CHECKING:
  from app.models.race import RaceRunner
  

class Runner(Base):
  __tablename__ = "runners"
  id: Mapped[int] = mapped_column(primary_key=True)
  rfid_uid: Mapped[str] = mapped_column(String(30))
  name: Mapped[str] = mapped_column(String(30))
  surname: Mapped[str] = mapped_column(String(30))

  race_runners: Mapped[List["RaceRunner"]] = relationship(
    "RaceRunner",
    back_populates="runner",
    cascade="all, delete-orphan",
  )
