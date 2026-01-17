from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.schemas.event import EventCreate


async def get_event(db: AsyncSession, event_id: int) -> Event | None:
  """Get a single event by ID."""
  result = await db.execute(select(Event).where(Event.id == event_id))
  return result.scalar_one_or_none()


async def get_events(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Event]:
  """Get all events with pagination."""
  result = await db.execute(select(Event).offset(skip).limit(limit))
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


async def create_event(db: AsyncSession, event_in: EventCreate) -> Event:
  """Create a new event."""
  event = Event(**event_in.model_dump())
  db.add(event)
  await db.commit()
  await db.refresh(event)
  return event


async def delete_event(db: AsyncSession, event_id: int) -> bool:
  """Delete an event."""
  event = await get_event(db, event_id)
  if not event:
    return False
  
  await db.delete(event)
  await db.commit()
  return True
