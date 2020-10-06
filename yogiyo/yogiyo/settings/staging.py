from .base import *

PROFILE = 'staging'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ['DEPLOY_DB_HOST'],
        'NAME': os.environ['DEPLOY_DB_NAME'],
        'USER': os.environ['DEPLOY_DB_USER'],
        'PASSWORD': os.environ['DEPLOY_DB_PASSWORD'],
        'PORT': os.environ['DEPLOY_DB_PORT'],
    }
}
