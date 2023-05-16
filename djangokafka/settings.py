import logging
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
BASE_DIR = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-bd$thkr^&a6)_-wyo#)0sc2c_gt*1q7&+o@)!i+si9a7oc#1c7"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# CORS CONFIGURATION
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "X-Content-Type-Options",
    "use-case",
    "x-csrftoken",
    "x-requested-with",
    "User-Platform",
    "OS",
    "usecase",
    "use-case",
]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]


# SETTING PROJECT APPLICATIONS
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = ["corsheaders", "rest_framework", "django_crontab"]
LOCAL_APPS = [
    "common"
]
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

UTH_USER_MODEL = "common.UserProxy"

# SETTING PROJECT MIDDLEWARE
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangokafka.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangokafka.wsgi.application"
SERVICE_NAME = os.environ.get("SERVICE_NAME")

# SETTING PROJECT KAFKA
try:
    # Enable producer to send events
    KAFKA_PRODUCE_EVENTS = os.getenv("KAFKA_PRODUCE_EVENTS", "False").lower() in (
        "true",
        "1",
        "t",
    )
    KAFKA_CONSUME_EVENTS = os.getenv("KAFKA_CONSUME_EVENTS", "False").lower() in (
        "true",
        "1",
        "t",
    )
    KAFKA_EVENTS_BROKER = os.environ.get("KAFKA_EVENTS_BROKER")
    KAFKA_EVENTS_TOPIC = os.environ.get("KAFKA_EVENTS_TOPIC")
    KAFKA_EVENTS_TOPIC_CONSUMER_GROUP = os.environ.get(
        "KAFKA_EVENTS_TOPIC_CONSUMER_GROUP"
    )
    KAFKA_PRODUCER_SEND_RETRIES = int(os.environ.get("KAFKA_PRODUCER_SEND_RETRIES"))
    KAFKA_AUTOCOMMIT_OFFSET = os.getenv("KAFKA_AUTOCOMMIT_OFFSET", "False").lower() in (
        "true",
        "1",
        "t",
    )
except Exception as ex:
    logger.error("ERROR: KAFKA CONFIGURATION ERROR!!! CHECK YOUR .env file")
    logger.warning(ex)


# SETTING PROJECT DATABASE
try:
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": DATABASE_HOST,
            "NAME": DATABASE_NAME,
            "USER": DATABASE_USER,
            "PASSWORD": DATABASE_PASSWORD,
            "PORT": DATABASE_PORT,
        }
    }
except Exception as database_exception:
    logger.error("ERROR: DATABASE SETTINGS ERROR!!! CHECK YOUR .env file")
    logger.warning(database_exception)



# JWT and FERNET SETTINGS
try:
    USERMS_JWT_ENCODING_ALGO = os.environ.get("USERMS_JWT_ENCODING_ALGO")
    USERMS_JWT_ENCODING_SECRET_KEY = os.environ.get("USERMS_JWT_ENCODING_SECRET_KEY")
    USERMS_JWT_TOKEN_EXPIRY_DELTA = int(os.environ.get("USERMS_JWT_TOKEN_EXPIRY_DELTA"))
    USERMS_FERTNET_SECRET_KEY = os.environ.get("USERMS_FERTNET_SECRET_KEY").encode()
except Exception as ex:
    logger.error("ERROR: JWT SETTINGS ERROR!!! CHECK YOUR .env file")
    logger.warning(ex)

# EMAIL SERVICE SETTINGS
try:
    EMAIL_SERVICE_URL = os.environ.get("EMAIL_SERVICE_URL")
except Exception as ex:
    logger.error("ERROR: EMAIL_SERVICE_URL SETTINGS ERROR!!! CHECK YOUR .env file")
    logger.warning(ex)

# DJANGO REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/min",
        "user": "100/min",
    },
    "EXCEPTION_HANDLER": "common.baselayer.baseapiviews.custom_exception_handler",
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
MSG_LOCALE = "en"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# MEDIA AND STATIC FILES SETTINGS
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


EMAIL_HOST = "smtpout.asia.secureserver.net"
EMAIL_HOST_USER = "support1@hypernymbiz.com"
EMAIL_HOST_PASSWORD = "hypernymbiz123"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
