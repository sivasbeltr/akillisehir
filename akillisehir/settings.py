import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
print(
    f"🔑 SECRET_KEY: {SECRET_KEY[:10]}..."
)  # Only print the first 10 characters for security

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
print(f"🔧 DEBUG mode: {'enabled' if DEBUG else 'disabled'}")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
print(f"🌐 ALLOWED_HOSTS: {ALLOWED_HOSTS}")

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "cms.apps.CmsConfig",
    "projects.apps.ProjectsConfig",
]
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "akillisehir.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "akillisehir.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "tr"

TIME_ZONE = "Europe/Istanbul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Media files (uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# MinIO Storage Configuration
USE_MINIO = os.getenv("USE_MINIO", "False").lower() == "true"

if USE_MINIO:
    # MinIO Settings
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "10.0.0.70:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", os.getenv("AWS_ACCESS_KEY_ID"))
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", os.getenv("AWS_SECRET_ACCESS_KEY"))
    MINIO_BUCKET_NAME = os.getenv(
        "MINIO_BUCKET_NAME", os.getenv("AWS_STORAGE_BUCKET_NAME", "akillisehir")
    )
    # HTTPS ayarını DEBUG moduna göre otomatik ayarla
    MINIO_USE_HTTPS = (
        False if DEBUG else os.getenv("MINIO_USE_HTTPS", "False").lower() == "true"
    )
    MINIO_CUSTOM_DOMAIN = os.getenv(
        "MINIO_CUSTOM_DOMAIN",
        os.getenv(
            "AWS_S3_CUSTOM_DOMAIN", MINIO_ENDPOINT
        ),  # Varsayılan olarak endpoint kullan
    )

    # Static ve Media klasör ayarları
    MINIO_STATIC_FILES_BUCKET = MINIO_BUCKET_NAME
    MINIO_MEDIA_FILES_BUCKET = MINIO_BUCKET_NAME
    MINIO_STATIC_LOCATION = os.getenv("MINIO_STATIC_LOCATION", "static")
    MINIO_MEDIA_LOCATION = os.getenv("MINIO_MEDIA_LOCATION", "media")

    # Django 4.2+ Storage System Configuration
    STORAGES = {
        "default": {
            "BACKEND": "akillisehir.storage_backends.MinIOMediaStorage",
        },
        "staticfiles": {
            "BACKEND": "akillisehir.storage_backends.MinIOStaticStorage",
        },
    }

    # Legacy support (Django < 4.2 için)
    DEFAULT_FILE_STORAGE = "akillisehir.storage_backends.MinIOMediaStorage"
    STATICFILES_STORAGE = "akillisehir.storage_backends.MinIOStaticStorage"

    # Static ve Media URL'leri - Her zaman HTTP kullan (DEBUG mode'da)
    protocol = "https"  # SSL hatası nedeniyle zorla HTTP kullan
    STATIC_URL = f"{protocol}://{MINIO_CUSTOM_DOMAIN}/{MINIO_STATIC_LOCATION}/"
    MEDIA_URL = f"{protocol}://{MINIO_CUSTOM_DOMAIN}/{MINIO_MEDIA_LOCATION}/"

    # STATIC_ROOT collectstatic için gerekli (geçici klasör)
    STATIC_ROOT = BASE_DIR / "staticfiles"

    print(f"✅ MinIO Storage aktif: {protocol}://{MINIO_ENDPOINT}")
    print(f"   📦 Bucket: {MINIO_BUCKET_NAME}")
    print(f"   🌐 Domain: {MINIO_CUSTOM_DOMAIN}")
    print(f"   🔒 HTTPS: {MINIO_USE_HTTPS}")
    print(f"   📁 Static: {STATIC_URL}")
    print(f"   📷 Media: {MEDIA_URL}")
else:
    # Local storage (development)
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
    print("📁 Local storage aktif")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
