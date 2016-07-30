import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'avancemacas',
        'USER': 'root',
        'PASSWORD': 'juliohurtado1208',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
            'init_command': 'SET foreign_key_checks = 0;'
        },
    }
}

DEBUG = True