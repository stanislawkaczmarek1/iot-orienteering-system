from pydantic import BaseModel, ConfigDict


class CheckpointBase(BaseModel):
  name: str


class CheckpointCreate(CheckpointBase):
  pass


class CheckpointUpdate(BaseModel):
  name: str | None = None


class CheckpointResponse(CheckpointBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
