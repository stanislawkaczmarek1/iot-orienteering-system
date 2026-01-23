from pydantic import BaseModel, ConfigDict


class RunnerBase(BaseModel):
  rfid_uid: int
  name: str
  surname: str


class RunnerCreate(BaseModel):
  rfid_uid: int


class RunnerUpdate(BaseModel):
  rfid_uid: int | None = None
  name: str | None = None
  surname: str | None = None


class RunnerResponse(RunnerBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
