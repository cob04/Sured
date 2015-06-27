import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard string to guess'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = ''
    MAIL_PORT = ''
    MAIL_USERNAME = os.environ.get('MAIN_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SURED_MAIL_SUBJECT_PREFIX = '[SURED]'
    SURED_MAIL_SENDER = 'Sured Admin <sured@example.com>'
    SURED_POSTS_PER_PAGE = 20
    SURED_FOLLOWERS_PER_PAGE = 50
    SURED_COMMENTS_PER_PAGE = 30
    SURED_SLOW_DB_QUERY_TIME = 0.5
    SURED_ADMIN = 'ericobain@gmail.com'
    # TODO correct the SURED_ADMIN configuration

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI =  os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'datasqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
