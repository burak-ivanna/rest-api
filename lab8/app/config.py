from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0

    class Config:
        env_file = ".env"


settings = Settings()
