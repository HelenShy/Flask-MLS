from datetime import timedelta

DEBUG = True

# SERVER_NAME = 'localhost:8000'
SECRET_KEY = 'kG2\xf3\xf1\xee\x1d\xfcV\xf0\xbbu\xeb\xe8\x1f\xf3$\xf6)\xd7?oRF'

# Flask-Mail
MAIL_DEFAULT_SENDER = 'contact@local.host'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'mls.housestage@gmail.com'
MAIL_PASSWORD = 'skorost123'

# Celery
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5

# SQLALchemy
db_uri = 'postgresql://mls:devpassword@postgres:5432/mls'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User
SEED_ADMIN_USERNAME = 'admin'
SEED_ADMIN_EMAIL = 'mls.housestage@gmail.com'
SEED_ADMIN_PASSWORD = 'devpasssword'
REMEMBER_COOKIE_DURATION = timedelta(days=90)

# JWT
JWT_SECRET_KEY = 'jwt-secret-string'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

JWT_TOKEN_LOCATION = ['cookies']
JWT_ACCESS_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/api/auth/token/refresh'
JWT_COOKIE_CSRF_PROTECT = False
JWT_COOKIE_SECURE = False  # for prod True
JWT_SESSION_COOKIE = False

# Flask-RESTPlus
SWAGGER_UI_JSON_EDITOR = True