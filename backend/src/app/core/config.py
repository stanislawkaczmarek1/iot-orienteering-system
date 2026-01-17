from functools import lru_cache


class Config:
  """Application config"""
  USE_SQLITE: bool = True
  API_PREFIX: str = "/api"  


@lru_cache()
def get_config() -> Config:
  return Config()


config = get_config()
