class Config():
    pass

# for development database
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:anoganteng@new-ecommerce.cijobjllzstt.ap-southeast-1.rds.amazonaws.com/ecommerce_new'

# for testing database
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:anoganteng@new-ecommerce.cijobjllzstt.ap-southeast-1.rds.amazonaws.com/ecommerce_test_new'