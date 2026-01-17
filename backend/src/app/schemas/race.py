from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RaceBase(BaseModel):
  name: str
  date: datetime
  is_active: bool


class RaceCreate(RaceBase):
  pass


class RaceUpdate(BaseModel):
  name: str | None = None
  date: datetime | None = None
  is_active: bool | None = None


class RaceResponse(RaceBase):
  id: int

  model_config = ConfigDict(from_attributes=True)


# Association schemas
class RaceCheckpointCreate(BaseModel):
  race_id: int
  checkpoint_id: int


class RaceRunnerCreate(BaseModel):
  race_id: int
  runner_id: int
