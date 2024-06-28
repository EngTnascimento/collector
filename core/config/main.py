from pydantic_settings import BaseSettings


class MainSettings(BaseSettings):
    app_port: int = 8000
