from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional
from functools import lru_cache



class Settings(BaseSettings):
    PROJECT_NAME: str = "LibraMind API"
    ENVIRONMENT: str = "development"

    DB_URL: Optional[str] = Field(
        None,
        description="Complete database URL, overrides individual parts if set"
    )
    DB_USER: Optional[str] = Field(None, env="DB_USER")
    DB_PASSWORD: Optional[str] = Field(None, env="DB_PASSWORD")
    DB_SERVER: Optional[str] = Field(None, env="DB_SERVER")
    DB_PORT: Optional[int] = Field(None, env="DB_PORT")
    DB_NAME: Optional[str] = Field(None, env="DB_NAME")


    # SMTP settings
    # These are used for sending emails, e.g., for password resets or notifications. 
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    REDIS_URL: str


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_URL:
            return self.DB_URL

        required = (self.DB_USER, self.DB_PASSWORD, self.DB_SERVER, self.DB_PORT, self.DB_NAME)
        if not all(required):
            missing = [name for name, val in zip(
                ["DB_USER", "DB_PASSWORD", "DB_SERVER", "DB_PORT", "DB_NAME"], required) if not val]
            raise ValueError(f"Missing config(s): {', '.join(missing)}")

        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()


# =====================================================================