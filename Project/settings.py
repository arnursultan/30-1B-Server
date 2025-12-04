import os
from pathlib import Path

from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",

    "dj_rest_auth",
    "dj_rest_auth.registration",

    'Server',
]


SITE_ID = int(os.getenv("SITE_ID", 1))

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

JAZZMIN_SETTINGS = {
    "site_title": "Administration panel",
    "site_header": "Library",
    "site_brand": "Server 30-1B",
    "welcome_sign": "Welcome to the Server 30-1B admin panel",
    "copyright": "Geeks",
    "search_model": ["auth.User", "auth.Group"],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://t.me/ar_nursultan", "new_window": True},
        {"model": "auth.User"},
    ],
    "show_sidebar": True,
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    #  Light themes
    # "theme" : "flatly",
    # "theme" : "simplex",
    # "theme" : "cerulean",
    # "theme" : "cosmo",
    # "theme" : "journal",
    # "theme" : "litera",
    # "theme" : "lumen",
    # "theme" : "lux",
    # "theme" : "materia",
    # "theme" : "minty",
    # "theme" : "pulse",
    # "theme" : "sandstone",
    # "theme" : "simplex",
    # "theme" : "sketchy",
    # "theme" : "spacelab",
    # "theme" : "united",
    # "theme" : "yeti",
    #  Dark themes
    "theme": "darkly",
    # "theme" : "slate",
    # "theme" : "cyborg",
    # "theme" : "solar",
    # "theme" : "superhero",
}

AUTH_USER_MODEL = "Server.User"

ROOT_URLCONF = 'Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Project.wsgi.application'

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

REST_USE_JWT = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_ACCESS_MINUTES", 15))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", 7))),
    "ROTATE_REFRESH_TOKENS": True if os.getenv("JWT_ROTATE_REFRESH", "True").lower() == "true" else False,
    "BLACKLIST_AFTER_ROTATION": True if os.getenv("JWT_BLACKLIST_AFTER_ROTATION", "True").lower() == "true" else False,
    "ALGORITHM": os.getenv("JWT_ALGORITHM", "HS256"),
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": tuple(os.getenv("AUTH_HEADER_TYPES", "Bearer").split(",")),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

ACCOUNT_LOGIN_METHODS = set(
    os.getenv("ACCOUNT_LOGIN_METHODS", "email,username").replace(" ", "").split(",")
)

ACCOUNT_SIGNUP_FIELDS = os.getenv(
    "ACCOUNT_SIGNUP_FIELDS",
    "email*,username*,password1*,password2*"
).replace(" ", "").split(",")

SOCIALACCOUNT_QUERY_EMAIL = True

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    },
    "github": {
        "SCOPE": ["user:email"],
    },
}


if os.getenv("ENABLE_CORS", "False").lower() == "true":
    INSTALLED_APPS += ["corsheaders"]
    MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
    CORS_ALLOWED_ORIGINS = [u for u in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if u]

CSRF_TRUSTED_ORIGINS = [u for u in os.getenv("CORS_TRUSTED_ORIGINS", "").split(",") if u]

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}

if DEBUG:
    print("DEBUG mode is on")
    print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
    print(f"SITE_ID: {SITE_ID}")