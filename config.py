import os

class BaseConfig(object):
    SUPPORTED_LANGUAGES = {'fi': 'Finnish', 'en': 'English'}
    BABEL_DEFAULT_LOCALE = 'fi'
    BABEL_DEFAULT_TIMEZONE = 'UTC+2'
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')