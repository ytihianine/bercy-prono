import pytest
from flask_appbuilder import AppBuilder, SQLA
from back.api import create_app
from back.api.match.match import Match
from back.api.user.user import User


@pytest.fixture()
def app():
    appbuilder = AppBuilder()
    db = SQLA()
    app = create_app("back.tests.config", app_builder=appbuilder, db=db)

    appbuilder.add_api(Match)
    appbuilder.add_api(User)

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def user_enregistrement():
    return b'{"username": "test", "password": "test", "mail": "test@finances.gouv.fr"}'


@pytest.fixture
def match_informations():
    return b'{"msg":{"jour": "01/01/2024", "heure": "18:00", "equipe_1": "FRA", "equipe_2": "ESP", "score_1": 1, "score2": 0}}\n'
