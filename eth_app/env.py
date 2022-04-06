class Config(object):
    TESTING = False

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
    API_KEY = 

class DevelopmentConfig(Config):
    DATABASE_URI = "sqlite:////tmp/foo.db"

class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
