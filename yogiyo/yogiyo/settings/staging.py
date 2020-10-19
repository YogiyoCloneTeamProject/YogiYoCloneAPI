from .base import *

PROFILE = 'staging'
DEBUG = True

DEFAULT_FILE_STORAGE = 'core.asset_storage.MediaStorage'
STATICFILES_STORAGE = 'core.asset_storage.StaticStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
