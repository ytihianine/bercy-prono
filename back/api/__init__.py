def create_app(config_filename: str, app_builder, db, scheduler):
    from flask import Flask

    app = Flask(__name__)
    app.config.from_object(config_filename)
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    with app.app_context():
        app_builder.init_app(app, db.session)
    return app
