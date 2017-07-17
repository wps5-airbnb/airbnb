"""
이 파일은 SETTINGS의 DEPLOY 파일 입니다.
"""
from .base import *

# WSGI 설정
WSGI_APPLICATION = 'config.wsgi.deploy.application'


config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())
