import os

class Config:
    APP_NAME ="RecipeGenie"
    SECRET_KEY = "SuperWieRdTOpSecRETKeY"

class DevConfig(Config):
    DEBUG = True
    DB_URI = os.environ.get('DATABASE_URI')
    DB_NAME = "all_recipes"

class ProdConfig(Config):
    DEBUG = False
    DB_URI = os.environ.get('DATABASE_URI')
    DB_NAME = "all_recipes"


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}