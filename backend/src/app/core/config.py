from functools import lru_cache


class Config:
  """Application config"""
  USE_SQLITE: bool = True
  API_PREFIX: str = "/api"  
  VERSION: str = "0.1.0"


@lru_cache()
def get_config() -> Config:
  return Config()


config = get_config()
