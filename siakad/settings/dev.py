from .common import *


DEBUG = True

SECRET_KEY = 'xmpq)%y#ne-v15)o2@=!66=mf*j*n^(qtb*^v+*8z!j3a*4pzf'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway',
        'HOST': 'containers-us-west-148.railway.app',
        'USER': 'root',
        'PORT': '5463',
        'PASSWORD': 'iUHGIxa4YBJblokWiqHO'
    }
}
