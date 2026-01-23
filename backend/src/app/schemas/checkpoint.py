from pydantic import BaseModel, ConfigDict


class CheckpointBase(BaseModel):
  id: int
  uuid: str
  name: str


class CheckpointCreate(BaseModel):
  checkpoint_id: str
  timestamp: str


class CheckpointUpdate(BaseModel):
  name: str | None = None


class CheckpointResponse(CheckpointBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
