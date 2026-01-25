import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.runner import RunnerCreate, RunnerUpdate, RunnerResponse
from app.crud import runner as runner_crud

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/runners", tags=["runners"])


@router.post("/", response_model=RunnerResponse, status_code=status.HTTP_201_CREATED)
async def create_runner(
  runner_in: RunnerCreate,
  db: AsyncSession = Depends(get_db)
):
  """Create a new runner."""
  logger.debug(f"Creating runner with rfid_uid: {runner_in.rfid_uid}: ")
  return await runner_crud.create_runner(db, runner_in)


@router.get("/", response_model=list[RunnerResponse])
async def list_runners(
  skip: int = 0,
  limit: int = 100,
  db: AsyncSession = Depends(get_db),
  race_id: int | None = Query(None)
):
  """Get all runners with pagination."""
  logger.debug(f"Listing runners (skip={skip}, limit={limit})")
  if race_id is not None:
      return await runner_crud.get_runners_of_race(db, race_id, skip, limit)
  return await runner_crud.get_runners(db, skip, limit)


@router.get("/{runner_id}", response_model=RunnerResponse)
async def get_runner(
  runner_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Get a specific runner by ID."""
  logger.debug(f"Getting runner with ID: {runner_id}")
  runner = await runner_crud.get_runner(db, runner_id)
  if not runner:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Runner with ID {runner_id} not found"
    )
  return runner


@router.put("/{runner_id}", response_model=RunnerResponse)
async def update_runner(
  runner_id: int,
  runner_in: RunnerUpdate,
  db: AsyncSession = Depends(get_db)
):
  """Update a runner."""
  logger.debug(f"Updating runner with ID: {runner_id}")
  runner = await runner_crud.update_runner(db, runner_id, runner_in)
  if not runner:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Runner with ID {runner_id} not found"
    )
  return runner


@router.delete("/{runner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_runner(
  runner_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Delete a runner."""
  logger.debug(f"Deleting runner with ID: {runner_id}")
  success = await runner_crud.delete_runner(db, runner_id)
  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Runner with ID {runner_id} not found"
    )
