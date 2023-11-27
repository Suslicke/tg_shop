from pydantic_settings import BaseSettings
from pydantic import SecretStr, PostgresDsn
from dotenv import load_dotenv
load_dotenv('.env.test')


class Settings(BaseSettings):
    bot_token: SecretStr
    payment_token: SecretStr
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: SecretStr
    db_url: PostgresDsn

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class TestSettings(Settings):
    class Config(Settings.Config):
        env_file = '.env.test'


test_config = TestSettings()
config = Settings()

