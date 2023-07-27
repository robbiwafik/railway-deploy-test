from .common import *


DEBUG = True

SECRET_KEY = 'xmpq)%y#ne-v15)o2@=!66=mf*j*n^(qtb*^v+*8z!j3a*4pzf'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'siakad',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': 'coutpassrootendl;'
    }
}
