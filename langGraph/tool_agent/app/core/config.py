from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # === Project Info ===
    PROJECT_NAME: str = "Agentic Chatbot"

    # === OpenAI & Pinecone ===
    OPENAI_API_KEY: Optional[str] = None
    EMBEDDINGS_MODEL: Optional[str] = None
    PINECONE_API_KEY:str
    MODEL_NAME: Optional[str] = None
    NEWS_API_KEY: Optional[str] = None  
    
    # === PGAdmin Config ===
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "your_password"
    PG_HOST: str = "localhost"
    PG_PORT: str = "12345"
    PG_DATABASE: str = "postgres"
    postgres_driver: str = "asyncpg"

    # === JWT ===
    JWT_SECRET: str
    JWT_ALGORITHM: str

    # === Pydantic Settings ===
    model_config = SettingsConfigDict(
        env_file=".env",       
        extra="allow"          
    )
    
    @property
    def database_url(self) -> str:
        """Create a valid Postgres database URL with proper encoding."""
        encoded_password = quote_plus(self.PG_PASSWORD)
        return (
            f"postgresql+{self.postgres_driver}://{self.PG_USER}:"
            f"{encoded_password}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}"
        )

    
    @property
    def fastapi_kwargs(self) -> dict:
        """Return FastAPI settings."""
        return {
            "docs_url": "/docs",
            "title": self.PROJECT_NAME,
            "version": "1.1",
        }



settings = Settings()