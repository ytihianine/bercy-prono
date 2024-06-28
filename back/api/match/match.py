from flask_appbuilder.api import BaseApi, expose
from flask import request, g
from datetime import datetime
import pandas as pd
import numpy as np

from config import app_database, app_sql


def get_user():
    return g.user


class Match(BaseApi):

    def scrap_info_match():
        print("SCRAP INFO")

    def determiner_statut_match():
        print("STATUT MATCH")
        matchs = app_database.execute_query("SELECT * FROM matchs")

        heure_actuelle = datetime.now()

        for match in matchs:
            heure_match = datetime.combine(match["date_match"], match["heure_match"])
            difference = heure_actuelle - heure_match
            difference_en_minutes = difference.total_seconds() / 60

            if difference_en_minutes < 0:
                match["statut_match"] = "a venir"

            if 0 < difference_en_minutes and difference_en_minutes < 120:
                match["statut_match"] = "terminé"
            elif difference_en_minutes > 120:
                match["statut_match"] = "en cours"

        query_update = app_sql.generate_update_clause("matchs", matchs[0])
        condition = f" WHERE id_match=%(id_match)s;"
        query = query_update + condition
        queries = [(query, match) for match in matchs]
        app_database.execute_queries(queries)

    @expose("/information", methods=["POST"])
    def get_match(self):

        conversion_mois = {"June": "Juin", "July": "Juillet"}
        matchs = app_database.execute_query(
            "SELECT * FROM matchs ORDER BY date_match, heure_match;"
        )
        for match in matchs:
            combined_date = datetime.combine(match["date_match"], match["heure_match"])
            match["date_match"] = datetime.strftime(combined_date, "%d %B à %H:%M")
            for mois in conversion_mois:
                match["date_match"] = match["date_match"].replace(
                    mois, conversion_mois[mois]
                )
            match.pop("heure_match")

        data = request.get_json()
        user = app_database.execute_query(
            f"SELECT * FROM ab_user WHERE username='{data['username']}'"
        )
        pronos = app_database.execute_query(
            f"SELECT * FROM pronostiques WHERE id_joueur={user[0]['id']};"
        )
        if len(pronos) == 0:
            return self.response(code=200, results=matchs)

        df_matchs = pd.DataFrame(matchs)
        df_pronos = pd.DataFrame(pronos)

        df_informations = pd.merge(df_matchs, df_pronos, how="left", on=["id_match"])
        df_informations = (
            df_informations.fillna(np.nan).replace([np.nan], [None]).reset_index()
        )

        df_informations = df_informations.to_dict("records")

        return self.response(code=200, results=df_informations)

    @expose("/prono", methods=["POST"])
    def make_prono(self):
        data = request.get_json()
        needed_columns = ["id_match", "username", "score_prono_a", "score_prono_b"]

        if not set(needed_columns) == set(data.keys()):
            return self.response_400("Invalid data format")

        print(data)
        user = app_database.execute_query(
            f"SELECT * FROM ab_user WHERE username='{data['username']}'"
        )
        print(user)
        if len(user) != 1:
            return self.response_400(message="Erreur utilisateur")

        data.pop("username", None)
        data["id_joueur"] = user[0]["id"]
        match_data = app_database.execute_query(
            f"SELECT * FROM matchs WHERE id_match={int(data['id_match'])}"
        )[0]
        heure_match = datetime.combine(
            match_data["date_match"], match_data["heure_match"]
        )

        heure_actuelle = datetime.now()
        if heure_actuelle > heure_match:
            return self.response_400(
                msg="Désolé, il est trop tard pour faire un pronostique!"
            )

        # check si le joueur a déjà fait un pronostique pour le match
        prono = app_database.execute_query(
            f"SELECT * FROM pronostiques WHERE id_match={int(data['id_match'])} and id_joueur={int(data['id_joueur'])}"
        )
        # On ajout son prono
        if len(prono) == 0:
            query = app_sql.generate_insert_clause("pronostiques", data)
            app_database.execute_query(query, data)
            return self.response(code=201, msg="Pronostique enregistré")
        # Sinon, on l'update
        elif len(prono) == 1:
            conditions = f" WHERE id_match={int(data['id_match'])} AND id_joueur={int(data['id_joueur'])};"
            query = app_sql.generate_update_clause("pronostiques", data) + conditions
            app_database.execute_query(query, data)
            return self.response(code=200, msg="Pronostique enregistré")

        return self.response_500("Une erreur interne est survenue")
