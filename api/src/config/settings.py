from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_token_expiration: int = 600
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str


settings = Settings()
