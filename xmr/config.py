from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV_UPLOAD: str = "/mnt/volume_ams3_01/upload/"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
