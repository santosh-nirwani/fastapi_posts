from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
      database_host: str
      database_username: str
      database_password: str
      secret_key: str
      algorithm: str
      access_token_expire: int

      model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
# settings.secret_key = os.getenv('secret_key')
# settings.algorithm = os.getenv('secret_key')
# settings.access_token_expire = os.getenv('secret_key')

print(settings.secret_key)
