"""
Author : Mitch Suzara <suzaram3@gmail.com>
Date   : 2022-04-14
Purpose: Config file for setting up env and database variables 
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # spotipy env variables
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

    # database env variables
    database_params = {
        "DATABASE_HOST": os.getenv("DATABASE_HOST"),
        "DATABASE_NAME": os.getenv("DATABASE_NAME"),
        "DATABASE_USER": os.getenv("DATABASE_USER"),
        "DATABASE_PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "DATABASE_PORT": os.getenv("DATABASE_PORT"),
    }

    # word cloud env variables
    TOP_ARTISTS_FILE_PATH = os.getenv("TOP_ARTISTS_FILE_PATH")
    WORDCLOUD_MASK = os.getenv("WORDCLOUD_MASK")
    WORDCLOUD_FONT = os.getenv("WORDCLOUD_FONT")
    SAVE_WORDCLOUD_PATH = os.getenv("SAVE_WORDCLOUD_PATH")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")


config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
}
