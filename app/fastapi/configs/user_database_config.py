from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError
from dotenv import load_dotenv

from src.fastapi.services.exceptions import EnvValidationException

load_dotenv()

class UserDBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )
    
    USER_DATABASE_URL: str = Field(min_length=3)
    PSQL_USER: str = Field(min_length=3)
    PSQL_HOST: str = Field(min_length=3)
    PSQL_PORT: int = Field(ge=0)

@lru_cache(maxsize=1)
def get_user_db_config() -> UserDBConfig:
    return UserDBConfig()

try:
    user_db_settings =  get_user_db_config()
    SEPARATOR = '=' * 45
    print(SEPARATOR)
    print('Полученый конфиг для пользователькой БД')
    print(f'database path: {user_db_settings.USER_DATABASE_URL}')
    print(f'host: {user_db_settings.PSQL_HOST}, port: {user_db_settings.PSQL_PORT}')
    print(SEPARATOR)
except ValidationError as error:
    raise EnvValidationException(error)
