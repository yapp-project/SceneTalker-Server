from .base import *
import pymysql
import json

DEBUG = False
LANGUAGE_CODE = 'en'
pymysql.install_as_MySQLdb()
SECRET_DIR = os.path.join(BASE_DIR, 'conf')
secrets = json.load(open(os.path.join(SECRET_DIR, 'secrets.json'), 'rb'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scene_talker',  # DB명
        'USER': secrets['DATABASES_USER'],  # 데이터베이스 계정
        'PASSWORD': secrets['DATABASES_PASSWORD'],  # 계정 비밀번호
        'HOST': secrets['DATABASES_HOST'],  # 데이테베이스 주소(IP)
        'PORT': '3306',  # 데이터베이스 포트(보통은 3306)
    }
}

# AWS S3 설정
DEFAULT_FILE_STORAGE = 'conf.storages.S3DefaultStorage'
STATICFILES_STORAGE = 'conf.storages.S3StaticStorage'

# AWS Access
AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_ACL = secrets['AWS_DEFAULT_ACL']
AWS_S3_REGION_NAME = secrets['AWS_S3_REGION_NAME']
AWS_S3_SIGNATURE_VERSION = secrets['AWS_S3_SIGNATURE_VERSION']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'access': {
            'level': 'INFO',
            'filename': '/home/ubuntu/scenetalker/SceneTalker-Server/SceneTalker/settings/logs/request-access.log',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': "midnight",
            'backupCount': 3,  # 로그 파일을 최대 5개까지 유지
            'formatter': 'verbose',
        },
        'error': {
            'level': 'WARNING',
            'filename': '/home/ubuntu/scenetalker/SceneTalker-Server/SceneTalker/settings/logs/request-error.log',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': "midnight",
            'backupCount': 3,  # 로그 파일을 최대 5개까지 유지
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['access', 'error'],
            'level': 'INFO',  # change debug level as appropiate
            'propagate': False,
        },
    },
}
