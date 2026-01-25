from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.runner import Runner
from app.models.race import RaceRunner
from app.schemas.runner import RunnerCreate, RunnerUpdate




async def get_runner(db: AsyncSession, runner_id: int) -> Runner | None:
  """Get a single runner by ID."""
  result = await db.execute(select(Runner).where(Runner.id == runner_id))
  return result.scalar_one_or_none()


async def get_runners(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Runner]:
  """Get all runners with pagination."""
  result = await db.execute(select(Runner).offset(skip).limit(limit))
  return result.scalars().all()

async def get_runners_of_race(db: AsyncSession, race_id: int, skip: int = 0, limit: int = 100) -> Sequence[Runner]:
  """Get all runners with pagination."""
  result = await db.execute(select(Runner).join(RaceRunner).where(RaceRunner.race_id == race_id).offset(skip).limit(limit))
  return result.scalars().all()

async def create_runner(db: AsyncSession, runner_in: RunnerCreate) -> Runner:
  """Create a new runner."""
  runner_with_rfid_uid = await get_runner_by_rfid(db, runner_in.rfid_uid)
  if runner_with_rfid_uid:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=f"Runner with rfid_uid: {str(runner_in.rfid_uid)} already exists",
    )

  runner = Runner(**runner_in.model_dump(), name="", surname="")
  db.add(runner)
  await db.commit()
  await db.refresh(runner)
  return runner


async def update_runner(db: AsyncSession, runner_id: int, runner_in: RunnerUpdate) -> Runner | None:
  """Update an existing runner."""
  runner = await get_runner(db, runner_id)
  if not runner:
    return None
  
  update_data = runner_in.model_dump(exclude_unset=True)
  for field, value in update_data.items():
    setattr(runner, field, value)
  
  await db.commit()
  await db.refresh(runner)
  return runner


async def delete_runner(db: AsyncSession, runner_id: int) -> bool:
  """Delete a runner."""
  runner = await get_runner(db, runner_id)
  if not runner:
    return False
  
  await db.delete(runner)
  await db.commit()
  return True

async def get_runner_by_rfid(db: AsyncSession, rfid: str) -> Runner | None:
  """Get a runner by rfid."""
  result = await db.execute(
    select(Runner).where(Runner.rfid_uid == rfid)
  )
  return result.scalar_one_or_none()
