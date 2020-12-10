from os import environ
from os.path import join, dirname, isfile

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
if isfile(dotenv_path):
    print("* ENV: attached from .env file, only for local development!!!")
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")

    EMAIL_USE_TLS = environ.get("EMAIL_USE_TLS")
    EMAIL_HOST = environ.get("EMAIL_HOST")

    EMAIL_SENDING = False
    EMAIL_PORT = environ.get("EMAIL_PORT")
    EMAIL_HOST_USER = environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = environ.get("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = environ.get("DEFAULT_FROM_EMAIL")

    DATABASE_NAME = environ.get("DATABASE_NAME")
    DATABASE_USER = environ.get("DATABASE_USER")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
    DATABASE_HOST = environ.get("DATABASE_HOST")
    DATABASE_PORT = environ.get("DATABASE_PORT")

    SOCIAL_AUTH_FACEBOOK_KEY = environ.get("SOCIAL_AUTH_FACEBOOK_KEY")
    SOCIAL_AUTH_FACEBOOK_SECRET = environ.get("SOCIAL_AUTH_FACEBOOK_SECRET")

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")


app_config = Config()
