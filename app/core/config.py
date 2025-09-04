from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite://./db.sqlite3"
    secret_key: str = "31dajkdalkjdskaj132dasczx123"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 300
    debug: bool = True
    app_name: str = "My App"
    app_version: str = "0.1.0"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()