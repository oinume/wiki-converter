import os

class Config(object):
    DEBUG = False
    SECRET_KEY = 'dev_key_h8hfne89vm'
    CSRF_ENABLED = True
    CSRF_SESSION_LKEY = 'dev_key_h8asSNJ9s9=+'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(DevelopmentConfig):
    TESTING = True

class ProductionConfig(Config):
    PRODUCTION = True

mode = os.environ.get('WIKI_CONVERTER_ENV', 'development')
object = DevelopmentConfig
if mode == 'development':
    object = DevelopmentConfig
elif mode == 'testing':
    object = TestingConfig
elif mode == 'production':
    object = ProductionConfig
else:
    raise ValueError("Unknown config mode.")
