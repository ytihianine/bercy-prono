from werkzeug.security import generate_password_hash
from flask_appbuilder.api import BaseApi, expose
from flask import request, g
from flask_mail import Message
from datetime import datetime

from config import app_database, app_sql, mail


class User(BaseApi):

    def calculer_rang():
        joueurs = app_database.execute_query(
            "SELECT * FROM classement ORDER BY points DESC"
        )

        for i in range(len(joueurs)):
            joueurs[i]["rang_joueur"] = i + 1

        query_update = app_sql.generate_update_clause("classement", joueurs[0])
        condition = f" WHERE id_joueur=%(id_joueur)s;"
        query = query_update + condition
        queries = [(query, joueur) for joueur in joueurs]
        app_database.execute_queries(queries)

    @expose("/enregistrement", methods=["POST"])
    def enregistrement(self):
        data = request.get_json()
        if set(["username", "password", "mail"]) == set(data.keys()):
            mail_split = data["mail"].split("@")
            if len(mail_split) == 2:
                # if not mail_split[1] == 'finances.gouv.fr':
                #    return self.response_400(message='Format de mail incorrect')

                check_mail = app_database.execute_query(
                    f"SELECT * FROM ab_user WHERE email='{mail_split[1]}'"
                )
                check_username = app_database.execute_query(
                    f"SELECT * FROM ab_user WHERE username='{data['username']}'"
                )

                if len(check_mail) != 0:
                    return self.response_400(message="mail déjà utilisé")

                if len(check_username) != 0:
                    return self.response_400(message="identifiant déjà utilisé")

                heure_creation = datetime.now()
                max_id_user = app_database.execute_query(
                    "SELECT MAX(id) as id FROM ab_user;"
                )
                app_database.execute_query(
                    f"""INSERT INTO ab_user (id, first_name, last_name, username, password, active, email, created_on)
                                           VALUES ('{max_id_user[0]['id'] + 1}','{data['username']}', 'bercy', '{data['username']}','{generate_password_hash(data['password'])}', {True}, '{data['mail']}', '{heure_creation}');"""
                )
                new_user_id = app_database.execute_query(
                    f"SELECT id FROM ab_user WHERE username='{data['username']}'"
                )

                if len(new_user_id) == 0:
                    return self.response_500(
                        message="Erreur lors de la création de l'utilisateur"
                    )

                max_id_user_role = app_database.execute_query(
                    "SELECT MAX(id) as id FROM ab_user_role;"
                )
                app_database.execute_query(
                    f"""INSERT INTO ab_user_role (id, user_id, role_id) VALUES ({max_id_user_role[0]['id'] + 1}, {new_user_id[0]['id']}, 2);"""
                )

                msg = Message(
                    subject="Prono Bercy - Confirmation d'inscription",
                    html="Ce mail confirme la création de votre compte sur Prono Bercy!",
                    recipients=[data["mail"]],
                )
                mail.send(msg)

                return self.response(201, message="Nouvel utilisateur créé")

            else:
                return self.response_400(message="Format de mail incorrect")
        else:
            return self.response_400(data)

    @expose("/classement", methods=["GET"])
    def classement(self):
        joueurs = app_database.execute_query(
            "SELECT id_joueur, points, rang_joueur FROM classement ORDER BY points DESC"
        )
        return self.response(code=200, result=joueurs)
