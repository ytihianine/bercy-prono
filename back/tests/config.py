import os
import random
import string

basedir = os.path.abspath(os.path.dirname(__file__))

FAB_ADD_SECURITY_API = True
CSRF_ENABLED = True
SECRET_KEY = "\2\1thisismyscretkey\1\2\e\y\y\h"


# creating a random name for the temporary memory DB
sqlite_shared_name = "test_db_{}".format(random.sample(string.ascii_letters, k=4))

SQLALCHEMY_DATABASE_URI = "sqlite:///file:{}?mode=memory&cache=shared&uri=true".format(
    sqlite_shared_name
)

SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_RECYCLE = 3


# ------------------------------
# GLOBALS FOR GENERAL APP's
# ------------------------------
FAB_API_SWAGGER_UI = True

UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_URL = "/static/uploads/"
AUTH_TYPE = 1
# AUTH_LDAP_SERVER = "ldap://dc.domain.net"
AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLE_PUBLIC = "Public"
APP_NAME = "Bercy Prono"
APP_THEME = ""
