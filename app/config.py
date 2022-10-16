from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    local_connection_string: str
    atlas_connection_string: str

    class Config:
        env_file = ".env"


settings = Settings()