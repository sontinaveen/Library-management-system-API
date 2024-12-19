import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'library.db')
    
    # Pagination settings
    ITEMS_PER_PAGE = 2
    
    # Token expiration time (in minutes)
    TOKEN_EXPIRATION = 60

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False