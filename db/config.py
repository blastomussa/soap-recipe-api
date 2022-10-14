from pydantic import BaseSettings


class Settings(BaseSettings):
    local_connection_string: str | None = None
    atlas_connection_string: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()