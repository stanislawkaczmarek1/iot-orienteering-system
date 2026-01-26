from typing import Sequence, List
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.race import Race, RaceCheckpoint, RaceRunner
from app.models.checkpoint import Checkpoint
from app.models.runner import Runner
from app.schemas.race import RaceCreate, RaceUpdate

# Race CRUD operations
async def get_race(db: AsyncSession, race_id: int) -> Race | None:
  """Get a single race by ID."""
  result = await db.execute(select(Race).where(Race.id == race_id))
  return result.scalar_one_or_none()


async def get_races(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Race]:
  """Get all races with pagination."""
  result = await db.execute(select(Race).offset(skip).limit(limit))
  return result.scalars().all()


async def create_race(db: AsyncSession, race_in: RaceCreate) -> Race:
  """Create a new race."""
  race = Race(**race_in.model_dump())
  db.add(race)
  await db.commit()
  await db.refresh(race)
  return race


async def update_race(db: AsyncSession, race_id: int, race_in: RaceUpdate) -> Race | None:
  """Update an existing race."""
  race = await get_race(db, race_id)
  if not race:
    return None
  
  update_data = race_in.model_dump(exclude_unset=True)
  for field, value in update_data.items():
    setattr(race, field, value)
  
  await db.commit()
  await db.refresh(race)
  return race


async def delete_race(db: AsyncSession, race_id: int) -> bool:
  """Delete a race."""
  race = await get_race(db, race_id)
  if not race:
    return False
  
  await db.delete(race)
  await db.commit()
  return True


# Race-Checkpoint association operations
async def get_race_checkpoints(db: AsyncSession, race_id: int) -> Sequence[Checkpoint]:
  """Get all checkpoints for a specific race."""
  result = await db.execute(
    select(Checkpoint)
    .join(RaceCheckpoint)
    .where(RaceCheckpoint.race_id == race_id)
    .order_by(RaceCheckpoint.order.asc())
  )
  return result.scalars().all()


async def add_race_checkpoint(db: AsyncSession, race_id: int, checkpoint_id: int) -> RaceCheckpoint:
  """Add a checkpoint to a race."""

  r = await db.execute(
    select(func.max(RaceCheckpoint.order))
    .where(RaceCheckpoint.race_id == race_id)
  )
  max_order = r.scalar()
  if max_order is None:
    max_order = 1
    
  race_checkpoint = RaceCheckpoint(race_id=race_id, checkpoint_id=checkpoint_id, order=(max_order + 1))
  db.add(race_checkpoint)
  await db.commit()
  await db.refresh(race_checkpoint)
  return race_checkpoint


async def remove_race_checkpoint(db: AsyncSession, race_id: int, checkpoint_id: int) -> bool:
  """Remove a checkpoint from a race."""
  result = await db.execute(
    delete(RaceCheckpoint).where(
      RaceCheckpoint.race_id == race_id,
      RaceCheckpoint.checkpoint_id == checkpoint_id
    )
  )
  await db.commit()
  return result.rowcount > 0


# Race-Runner association operations
async def get_race_runners(db: AsyncSession, race_id: int) -> Sequence[Runner]:
  """Get all runners for a specific race."""
  result = await db.execute(
    select(Runner)
    .join(RaceRunner)
    .where(RaceRunner.race_id == race_id)
  )
  return result.scalars().all()

async def delete_race_checkpoints(db: AsyncSession, race_id: int):
  result = await db.execute(
    delete(RaceCheckpoint).where(
      RaceCheckpoint.race_id == race_id
    )
  )
  await db.commit()
  return True


async def replace_race_checkpoints(db: AsyncSession, race_id: int, new_checkpoints: List[int]):
  result = await db.execute(
    delete(RaceCheckpoint).where(
      RaceCheckpoint.race_id == race_id
    )
  )
  await db.commit()
  i = 1
  for c in new_checkpoints:
    db.add( RaceCheckpoint(race_id=race_id, checkpoint_id=c, order=i))
    i += 1
  await db.commit()

async def add_race_runner(db: AsyncSession, race_id: int, runner_id: int) -> RaceRunner:
  """Add a runner to a race."""
  race_runner = RaceRunner(race_id=race_id, runner_id=runner_id)
  db.add(race_runner)
  await db.commit()
  await db.refresh(race_runner)
  return race_runner


async def remove_race_runner(db: AsyncSession, race_id: int, runner_id: int) -> bool:
  """Remove a runner from a race."""
  result = await db.execute(
    delete(RaceRunner).where(
      RaceRunner.race_id == race_id,
      RaceRunner.runner_id == runner_id
    )
  )
  await db.commit()
  return result.rowcount > 0

async def get_active_race_with_checkpoint(db: AsyncSession, checkpoint_id: int) -> Race | None:
  result = await db.execute(
    select(Race).join(RaceCheckpoint).where((Race.is_active == True) & (RaceCheckpoint.checkpoint_id == checkpoint_id))
  )
  return result.scalar_one_or_none()




