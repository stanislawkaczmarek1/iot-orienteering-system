from pydantic import BaseModel, ConfigDict


class CheckpointBase(BaseModel):
  id: int
  uuid: str
  name: str


class CheckpointCreate(BaseModel):
  uuid: str
  name: str


class CheckpointUpdate(BaseModel):
  name: str | None = None


class CheckpointResponse(CheckpointBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
