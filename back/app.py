from flask_appbuilder import SQLA, AppBuilder
from flask_apscheduler import APScheduler

from api import create_app
from api.match.match import Match
from api.user.user import User
from config import mail

db = SQLA()
appbuilder = AppBuilder()
scheduler = APScheduler()

app = create_app("config", app_builder=appbuilder, db=db, scheduler=scheduler)
mail.init_app(app)
appbuilder.add_api(Match)
appbuilder.add_api(User)

# Ajout de job
scheduler.add_job(
    id="Scheduled Task - User", func=User.calculer_rang, trigger="interval", minutes=5
)
scheduler.add_job(
    id="Scheduled Task - Match statut",
    func=Match.determiner_statut_match,
    trigger="interval",
    minutes=5,
)
""" scheduler.add_job(
    id="Scheduled Task - Match scrap",
    func=Match.scrap_info_match,
    trigger="interval",
    minutes=60,
) """


@app.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


if __name__ == "__main__":
    app.run(host="localhost", port=5050, debug=True)
