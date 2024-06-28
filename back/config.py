import os
from flask_mail import Mail

from utils.interactions import Database, SqlMethods

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
app_database = Database(
    "localhost",
    "BercyProno",
    "NotImplemented",
    "postgres",
    "root",
    "5433",
    "DEV",
    app_logger=None,
)
app_sql = SqlMethods(current_app_database=app_database)

FAB_ADD_SECURITY_API = True
CSRF_ENABLED = True
SECRET_KEY = "\2\1thisismyscretkey\1\2\e\y\y\h"


SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5433/BercyProno"

SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_RECYCLE = 3

SCHEDULER_API_ENABLED = True


# ------------------------------
# GLOBALS FOR GENERAL APP's
# ------------------------------


FAB_API_SWAGGER_UI = True

UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_URL = "/static/uploads/"
AUTH_TYPE = 1
# AUTH_LDAP_SERVER = "ldap://dc.domain.net"
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"
RECAPTCHA_PUBLIC_KEY = "6LedRP0SAAAAAOF03Nsv_ny2NzOF_Dthe_Xn269v"
RECAPTCHA_PRIVATE_KEY = "6LedRP0SAAAAAPnsdEKgj5VU1QbFcPv7mO8cW0So"

MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_SERVER = "smtp-mail.outlook.com"
MAIL_USE_TLS = True
MAIL_USERNAME = "bercy-prono@outlook.com"
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = "bercy-prono@outlook.com"

AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLE_PUBLIC = "Public"
APP_NAME = "Bercy Prono"
APP_THEME = ""
