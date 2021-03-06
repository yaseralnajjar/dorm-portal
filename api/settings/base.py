import os
import i18n

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SETTINGS_DIR)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # < Per Whitenoise, to disable built in
    'django.contrib.staticfiles',
    'rest_framework',

    'rest_framework.authtoken',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'corsheaders',

    'behave_django',
    'polymorphic',
    'adminsortable2',
    'djmoney.contrib.exchange',
    'api.engine',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'api.middlewares.CrossDomainSessionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'api.middlewares.SystemYokMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Add dist to
        'DIRS': ['dist', os.path.join(BASE_DIR, 'email_templates')],
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

WSGI_APPLICATION = 'api.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# i18n Plugin Settings

i18n.set('locale', 'en')
i18n.set('fallback', 'en')
i18n.load_path.append('locale')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# When Vue Builds, path will be `/static/css/...` so we will have Django Serve
# In Production, it's recommended use an alternative approach such as:
# http://whitenoise.evans.io/en/stable/django.html?highlight=django

STATIC_URL = '/static/'
# Serve `dist` as is, built by webpack
STATIC_ROOT = os.path.join(BASE_DIR, 'dist', 'static')
STATICFILES_DIRS = []
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


##########
# STATIC #
##########

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Insert Whitenoise Middleware at top but below Security Middleware
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware',)
# http://whitenoise.evans.io/en/stable/django.html#make-sure-staticfiles-is-configured-correctly

# Custom user

AUTH_USER_MODEL = 'engine.User'

# Account Settings

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
#ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'
ACCOUNT_ADAPTER = 'api.engine.adapters.MyAccountAdapter'
#ACCOUNT_USERNAME_BLACKLIST = ['system', ]

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'api.engine.serializers.PasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'api.engine.serializers.PasswordResetConfirmSerializer',
    'USER_DETAILS_SERIALIZER': 'api.engine.serializers.UserSerializer'
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'api.engine.serializers.RegisterSerializer',
}


# Email Settings

EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''


# Currency Exchange Settings

EXCHANGE_BACKEND = 'api.engine.exchange_backends.ExchangeRatesIOBackend'
