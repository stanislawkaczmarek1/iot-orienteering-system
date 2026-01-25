from typing import Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.checkpoint import Checkpoint
from app.models.race import RaceCheckpoint
from app.schemas.checkpoint import CheckpointCreate, CheckpointUpdate


async def get_checkpoint(db: AsyncSession, checkpoint_id: int) -> Checkpoint | None:
  """Get a single checkpoint by ID."""
  result = await db.execute(select(Checkpoint).where(Checkpoint.id == checkpoint_id))
  return result.scalar_one_or_none()

async def get_checkpoints_of_race(db: AsyncSession, race_id: int) ->  Sequence[Checkpoint]:
  result = await db.execute(select(Checkpoint).join(RaceCheckpoint).where(RaceCheckpoint.race_id == race_id))
  return result.scalars().all()

async def get_checkpoints(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Checkpoint]:
  """Get all checkpoints with pagination."""
  result = await db.execute(select(Checkpoint).offset(skip).limit(limit))
  return result.scalars().all()


async def create_checkpoint(db: AsyncSession, checkpoint_in: CheckpointCreate) -> Checkpoint:
  """Create a new checkpoint."""
  checkpoint = Checkpoint(name="", uuid=checkpoint_in.checkpoint_id)
  db.add(checkpoint)
  await db.commit()
  await db.refresh(checkpoint)
  return checkpoint


async def update_checkpoint(db: AsyncSession, checkpoint_id: int, checkpoint_in: CheckpointUpdate) -> Checkpoint | None:
  """Update an existing checkpoint."""
  checkpoint = await get_checkpoint(db, checkpoint_id)
  if not checkpoint:
    return None
  
  update_data = checkpoint_in.model_dump(exclude_unset=True)
  for field, value in update_data.items():
    setattr(checkpoint, field, value)
  
  await db.commit()
  await db.refresh(checkpoint)
  return checkpoint


async def delete_checkpoint(db: AsyncSession, checkpoint_id: int) -> bool:
  """Delete a checkpoint."""
  checkpoint = await get_checkpoint(db, checkpoint_id)
  if not checkpoint:
    return False
  
  await db.execute(delete(Checkpoint).where(Checkpoint.id == checkpoint_id))
  await db.commit()
  return True

async def get_checkpoint_by_uuid(db: AsyncSession, uuid: str) -> Checkpoint | None:
  """Get a single checkpoint by UUID."""
  result = await db.execute(select(Checkpoint).where(Checkpoint.uuid == uuid))
  return result.scalar_one_or_none()
