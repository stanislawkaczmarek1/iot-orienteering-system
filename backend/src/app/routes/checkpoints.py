import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.checkpoint import CheckpointCreate, CheckpointUpdate, CheckpointResponse
from app.crud import checkpoint as checkpoint_crud

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/checkpoints", tags=["checkpoints"])


@router.post("/", response_model=CheckpointResponse, status_code=status.HTTP_201_CREATED)
async def create_checkpoint(
  checkpoint_in: CheckpointCreate,
  db: AsyncSession = Depends(get_db)
):
  """Create a new checkpoint."""
  logger.debug(f"Creating checkpoint: {checkpoint_in.checkpoint_id}")
  return await checkpoint_crud.create_checkpoint(db, checkpoint_in)


@router.get("/", response_model=list[CheckpointResponse])
async def list_checkpoints(
  skip: int = 0,
  limit: int = 100,
  db: AsyncSession = Depends(get_db)
):
  """Get all checkpoints with pagination."""
  logger.debug(f"Listing checkpoints (skip={skip}, limit={limit})")
  return await checkpoint_crud.get_checkpoints(db, skip, limit)


@router.get("/{checkpoint_id}", response_model=CheckpointResponse)
async def get_checkpoint(
  checkpoint_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Get a specific checkpoint by ID."""
  logger.debug(f"Getting checkpoint with ID: {checkpoint_id}")
  checkpoint = await checkpoint_crud.get_checkpoint(db, checkpoint_id)
  if not checkpoint:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Checkpoint with ID {checkpoint_id} not found"
    )
  return checkpoint


@router.put("/{checkpoint_id}", response_model=CheckpointResponse)
async def update_checkpoint(
  checkpoint_id: int,
  checkpoint_in: CheckpointUpdate,
  db: AsyncSession = Depends(get_db)
):
  """Update a checkpoint."""
  logger.debug(f"Updating checkpoint with ID: {checkpoint_id}")
  checkpoint = await checkpoint_crud.update_checkpoint(db, checkpoint_id, checkpoint_in)
  if not checkpoint:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Checkpoint with ID {checkpoint_id} not found"
    )
  return checkpoint


@router.delete("/{checkpoint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checkpoint(
  checkpoint_id: int,
  db: AsyncSession = Depends(get_db)
):
  """Delete a checkpoint."""
  logger.debug(f"Deleting checkpoint with ID: {checkpoint_id}")
  success = await checkpoint_crud.delete_checkpoint(db, checkpoint_id)
  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Checkpoint with ID {checkpoint_id} not found"
    )
