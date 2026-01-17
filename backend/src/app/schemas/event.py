from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
  runner_id: int
  checkpoint_id: int
  race_id: int
  timestamp: datetime


class EventCreate(EventBase):
  pass


class EventResponse(EventBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
