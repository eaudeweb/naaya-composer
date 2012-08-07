import os
import os.path
import json


with open(os.environ['SARGEAPP_CFG'], 'rb') as f:
    _services = json.load(f)['services']

SENTRY_KEY = str(_services['secret']['sentry_key'])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(str(_services['db_folder']['path']), 'sentry.db'),
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SENTRY_PUBLIC = False

SENTRY_URL_PREFIX = 'http://sentry.vulture.eea.europa.eu'  # No trailing slash!

SENTRY_WEB_HOST = '127.0.0.1'
SENTRY_WEB_PORT = 32748
SENTRY_WEB_OPTIONS = {
    'workers': 3,  # the number of gunicorn workers
    # 'worker_class': 'gevent',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'localhost'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False

SENTRY_MAIL_LEVEL = 100
