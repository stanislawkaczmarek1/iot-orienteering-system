from datetime import datetime
from time import strftime
from typing import Sequence, List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.event import EventCreate

from app.crud.checkpoint import get_checkpoint_by_uuid
from app.crud.runner import get_runner_by_rfid
from app.crud.race import get_active_races_with_checkpoint


async def get_event(db: AsyncSession, event_id: int) -> Event | None:
  """Get a single event by ID."""
  result = await db.execute(select(Event).where(Event.id == event_id))
  return result.scalar_one_or_none()


async def get_events(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Event]:
  """Get all events with pagination."""
  result = await db.execute(select(Event).offset(skip).limit(limit))
  return result.scalars().all()

async def get_events_of_race(db: AsyncSession, race_id: int, skip: int = 0, limit: int = 100) -> Sequence[Event]:
  """Get all events with pagination."""
  result = await db.execute(select(Event).where(Event.race_id == race_id).offset(skip).limit(limit))
  return result.scalars().all()


async def get_race_runner_events(db: AsyncSession, race_id: int, runner_id: int) -> Sequence[Event]:
  """Get all events for a specific race and runner."""
  result = await db.execute(
    select(Event).where(
      Event.race_id == race_id,
      Event.runner_id == runner_id
    )
  )
  return result.scalars().all()


async def create_event(db: AsyncSession, event_in: EventCreate) -> List[Event]:
  """Create a new event."""
  checkpoint = await get_checkpoint_by_uuid(db, event_in.checkpoint_id)
  if not checkpoint:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Checkpoint with id {event_in.checkpoint_id} not found"
    )

  runner = await get_runner_by_rfid(db, event_in.rfid_uid)
  if not runner:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Runner with rfid_uid: {event_in.rfid_uid} not found"
    )

  races = await get_active_races_with_checkpoint(db, checkpoint.id)
  if len(races) == 0:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Checkpoint with id: {checkpoint.id} is not a part of any active race"
    )


  events = [
      Event(runner_id=runner.id, checkpoint_id=checkpoint.id, race_id=race.id,
            timestamp=datetime.fromisoformat(event_in.timestamp))
      for race in races
    ]

  db.add_all(events)
  await db.commit()

  for event in events:
    await db.refresh(event)

  return events


async def delete_event(db: AsyncSession, event_id: int) -> bool:
  """Delete an event."""
  event = await get_event(db, event_id)
  if not event:
    return False

  await db.delete(event)
  await db.commit()
  return True
