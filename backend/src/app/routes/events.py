from datetime import datetime
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.event import EventCreate, EventResponse
from app.crud import event as event_crud

from app.models.event import Event

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
  event_in: EventCreate,
  db: AsyncSession = Depends(get_db)
):
  """Create a new event (runner checkpoint scan)."""
  logger.debug(f"Creating event: runner={event_in.rfid_uid}, checkpoint={event_in.checkpoint_id}")
  return await event_crud.create_event(db, event_in)


@router.get("/", response_model=list[EventResponse])
async def list_events(
  skip: int = 0,
  limit: int = 100,
  db: AsyncSession = Depends(get_db)
):
  """Get all events with pagination."""
  logger.debug(f"Listing events (skip={skip}, limit={limit})")
  return await event_crud.get_events(db, skip, limit)


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
  event_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Get a specific event by ID."""
  logger.debug(f"Getting event with ID: {event_id}")
  event = await event_crud.get_event(db, event_id)
  if not event:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Event with ID {event_id} not found"
    )
  return event


@router.get("/race/{race_id}/runner/{runner_id}", response_model=list[EventResponse])
async def get_race_runner_events(
  race_id: int,
  runner_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Get all events for a specific race and runner."""
  logger.debug(f"Getting events for race {race_id} and runner {runner_id}")
  return await event_crud.get_race_runner_events(db, race_id, runner_id)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
  event_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Delete an event."""
  logger.debug(f"Deleting event with ID: {event_id}")
  success = await event_crud.delete_event(db, event_id)
  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Event with ID {event_id} not found"
    )
