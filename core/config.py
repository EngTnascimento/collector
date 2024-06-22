from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_port: int = 8000
    minio_key: str = 'admin'
    minio_secret: str = 'SsG7Wh0gAT'
    minio_endpoint: str = 'http://localhost:9000'

settings = Settings()
