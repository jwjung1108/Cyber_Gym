class Config:
    SECRET_KEY =  "this is secret key"
    TESTING = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI ='mysql+mysqlconnector://cyber:range@localhost/cyberrange'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI ='mysql+mysqlconnector://cyber:range@localhost/cyberrange'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = False
    DEBUG = True
    
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

