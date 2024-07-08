from pydantic_settings import BaseSettings


class Config(BaseSettings):
    host: str
    port: int
    db_url: str


config = Config(_env_file='.env')

__all__ = ['config']