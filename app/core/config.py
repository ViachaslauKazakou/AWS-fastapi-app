# File: /fastapi-app/fastapi-app/app/core/config.py

class Settings:
    PROJECT_NAME: str = "FastAPI Application"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A simple FastAPI application with multiple endpoints."
    API_PREFIX: str = "/api"


settings = Settings()
