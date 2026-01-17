from pydantic import BaseModel, ConfigDict


class RunnerBase(BaseModel):
  rfid_uid: str
  name: str
  surname: str


class RunnerCreate(RunnerBase):
  pass


class RunnerUpdate(BaseModel):
  rfid_uid: str | None = None
  name: str | None = None
  surname: str | None = None


class RunnerResponse(RunnerBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
