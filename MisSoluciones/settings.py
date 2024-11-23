"""
Django settings for MisSoluciones project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import MySQLdb

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6f6g%62c^-d8r^dljr#4d7xg&d4(8nmg)9fh=w9an133^*-u60'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['missoluciones2022.pythonanywhere.com']
CORS_ALLOWED_ORIGINS = [
    "http://mozilla.github.io/pdf.js/build/pdf.mjs",
    "https://api.domain.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000"
]
CORS_ALLOWED_ORIGIN_REGEXES = [
r"^https://\w+\.domain\.com$",
]
CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
]

CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'Soluciones',
    'rest_framework',
    'django_crontab',
    'corsheaders',



]
CRONJOBS = [('5 23 * * *', 'Soluciones.evento.actvivar_pqt')]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'MisSoluciones.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MisSoluciones.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'missoluciones202$misSoluciones2023',
        'USER': 'missoluciones202',
        'PASSWORD': 'Tamara2023',
        'HOST': 'missoluciones2022.mysql.pythonanywhere-services.com',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

X_FRAME_OPTIONS="SAMEORIGIN"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
LOGIN_REDIRECT_URL='/index/'
LOGOUT_REDIRECT_URL='/index/'
STATIC_URL = '/static/'
STATIC_ROOT = '/home/missoluciones2022/MisSoluciones/static'
MEDIA_URL = '/problemas/'
MEDIA_ROOT =os.path.join(BASE_DIR, 'problemas')
#MEDIA_ROOT =os.path.join(BASE_DIR, 'static')
#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'misoluciones22@yandex.com'
EMAIL_HOST_PASSWORD = 'gejjtdbxardnvarx'

#RECIPIENT_ADDRESS = 'ignaciohg2022@gmail.com'
#Clave para correo Yandex Tamara2023**
#Clave para correo Gmail Gutierrez2022*




