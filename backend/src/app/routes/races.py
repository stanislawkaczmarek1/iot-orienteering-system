import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.race import RaceCreate, RaceUpdate, RaceResponse
from app.schemas.checkpoint import CheckpointResponse
from app.schemas.runner import RunnerResponse
from app.crud import race as race_crud

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/races", tags=["races"])


@router.post("/", response_model=RaceResponse, status_code=status.HTTP_201_CREATED)
async def create_race(
  race_in: RaceCreate,
  db: AsyncSession = Depends(get_db)
):
  """Create a new race."""
  logger.debug(f"Creating race: {race_in.name}")
  return await race_crud.create_race(db, race_in)


@router.get("/", response_model=list[RaceResponse])
async def list_races(
  skip: int = 0,
  limit: int = 100,
  db: AsyncSession = Depends(get_db)
):
  """Get all races with pagination."""
  logger.debug(f"Listing races (skip={skip}, limit={limit})")
  return await race_crud.get_races(db, skip, limit)


@router.get("/{race_id}", response_model=RaceResponse)
async def get_race(
  race_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Get a specific race by ID."""
  logger.debug(f"Getting race with ID: {race_id}")
  race = await race_crud.get_race(db, race_id)
  if not race:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Race with ID {race_id} not found"
    )
  return race


@router.put("/{race_id}", response_model=RaceResponse)
async def update_race(
  race_id: int,
  race_in: RaceUpdate,
  db: AsyncSession = Depends(get_db)
):
  """Update a race."""
  logger.debug(f"Updating race with ID: {race_id}")
  race = await race_crud.update_race(db, race_id, race_in)
  if not race:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Race with ID {race_id} not found"
    )
  return race


@router.delete("/{race_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_race(
  race_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Delete a race."""
  logger.debug(f"Deleting race with ID: {race_id}")
  success = await race_crud.delete_race(db, race_id)
  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Race with ID {race_id} not found"
    )


# Race-Checkpoint association endpoints
@router.get("/{race_id}/checkpoints", response_model=list[CheckpointResponse])
async def get_race_checkpoints(
  race_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Get all checkpoints for a specific race."""
  logger.debug(f"Getting checkpoints for race ID: {race_id}")
  # Verify race exists
  race = await race_crud.get_race(db, race_id)
  if not race:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Race with ID {race_id} not found"
    )
  return await race_crud.get_race_checkpoints(db, race_id)


@router.post("/{race_id}/checkpoints/{checkpoint_id}", status_code=status.HTTP_201_CREATED)
async def add_checkpoint_to_race(
  race_id: int,
  checkpoint_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Add a checkpoint to a race."""
  logger.debug(f"Adding checkpoint {checkpoint_id} to race {race_id}")
  try:
    await race_crud.add_race_checkpoint(db, race_id, checkpoint_id)
    return {"message": "Checkpoint added to race successfully"}
  except Exception as e:
    logger.error(f"Error adding checkpoint to race: {e}")
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Failed to add checkpoint to race. Check if both exist and association doesn't already exist."
    )


@router.delete("/{race_id}/checkpoints/{checkpoint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_checkpoint_from_race(
  race_id: int,
  checkpoint_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Remove a checkpoint from a race."""
  logger.debug(f"Removing checkpoint {checkpoint_id} from race {race_id}")
  success = await race_crud.remove_race_checkpoint(db, race_id, checkpoint_id)
  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Race-Checkpoint association not found"
    )


# Race-Runner association endpoints
@router.get("/{race_id}/runners", response_model=list[RunnerResponse])
async def get_race_runners(
  race_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Get all runners for a specific race."""
  logger.debug(f"Getting runners for race ID: {race_id}")
  # Verify race exists
  race = await race_crud.get_race(db, race_id)
  if not race:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Race with ID {race_id} not found"
    )
  return await race_crud.get_race_runners(db, race_id)


@router.post("/{race_id}/runners/{runner_id}", status_code=status.HTTP_201_CREATED)
async def add_runner_to_race(
  race_id: int,
  runner_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Add a runner to a race."""
  logger.debug(f"Adding runner {runner_id} to race {race_id}")
  try:
    await race_crud.add_race_runner(db, race_id, runner_id)
    return {"message": "Runner added to race successfully"}
  except Exception as e:
    logger.error(f"Error adding runner to race: {e}")
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Failed to add runner to race. Check if both exist and association doesn't already exist."
    )


@router.delete("/{race_id}/runners/{runner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_runner_from_race(
  race_id: int,
  runner_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Remove a runner from a race."""
  logger.debug(f"Removing runner {runner_id} from race {race_id}")
  success = await race_crud.remove_race_runner(db, race_id, runner_id)
  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Race-Runner association not found"
    )
