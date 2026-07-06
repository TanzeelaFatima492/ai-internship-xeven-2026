from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Restaurant RAG API"
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        extra = "allow"  # ✅ Allows GROK_API_KEY and other new env vars


settings = Settings()