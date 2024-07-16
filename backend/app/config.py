from pydantic_settings import BaseSettings


class Config(BaseSettings):
    host: str
    port: int
    db_url: str
    bin_model_path: str
    yolo_model_path: str
    static_dir: str


config = Config(_env_file='.env')

__all__ = ['config']