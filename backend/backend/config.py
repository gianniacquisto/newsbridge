from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    llama_server_url: str = "http://host.docker.internal:8000"
    llm_model: str = "gemma:7b"
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.3

    # RSS polling
    poll_interval: int = 1  # minutes

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/newsbridge.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
