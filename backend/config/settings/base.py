import os
from pathlib import Path
from dotenv import load_dotenv

# Diretório raiz do backend e do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

# Carregar variáveis de ambiente do .env da raiz do projeto
load_dotenv(ROOT_DIR / '.env')
load_dotenv(BASE_DIR / '.env')

# Suporte automático a PyMySQL como driver MySQL quando mysqlclient não tem binários C
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'argus-insecure-key-for-development-change-me')
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('true', '1', 't')

allowed_hosts_raw = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_raw.split(',') if host.strip()]

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Terceiros
    'corsheaders',
    # Apps Argus (Clean Service Architecture)
    'apps.users',
    'apps.catalog',
    'apps.datasets',
    'apps.access',
    'apps.moderation',
    'apps.audit',
    'apps.analytics',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Configuração da Base de Dados MySQL 8
DB_NAME = os.getenv('DB_NAME', 'argus_db')
DB_USER = os.getenv('DB_USER', 'argus_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'argus_pass')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION'",
        },
    }
}

# Validação de Palavras-passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Ficheiros Estáticos e Storage
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
STORAGE_DIR = os.getenv('STORAGE_DIR', '../storage')
MEDIA_ROOT = (BASE_DIR / STORAGE_DIR).resolve()

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração CORS & CSRF
cors_raw = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_raw.split(',') if origin.strip()]
CORS_ALLOW_CREDENTIALS = True

csrf_raw = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_raw.split(',') if origin.strip()]
