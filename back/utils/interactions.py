import psycopg2
from psycopg2.extras import DictCursor, execute_values
from psycopg2.extensions import register_adapter, AsIs
from psycopg2.errors import OperationalError
import numpy as np
import logging

register_adapter(np.datetime64, AsIs)

from datetime import datetime
from zoneinfo import ZoneInfo


# from utils.Logger_custom import DatabaseLogHandler
# Logger pour envoyer les logs vers la base de données


class DatabaseLogHandler(logging.Handler):
    def __init__(
        self,
        host: str,
        db_dev_name: str,
        db_deployment_name: str,
        user: str,
        password: str,
        port: str,
        app_statut: str,
    ):
        logging.Handler.__init__(self)
        self.host = host
        self.db_dev_name = db_dev_name
        self.db_deployment_name = db_deployment_name
        self.user = user
        self.password = password
        self.port = port
        self.app_statut = app_statut

    def which_database(self) -> str:
        if self.app_statut == "DEV":
            return self.db_dev_name

        if self.app_statut == "DEPLOYMENT":
            return self.db_deployment_name

    def emit(self, record):
        log_entry = self.format(record)
        log_timestamp = datetime.now(tz=ZoneInfo("Europe/Paris"))
        jour = log_timestamp.strftime("%Y/%m/%d")
        heure = log_timestamp.strftime("%H:%M:%S")
        level = record.levelname
        message = log_entry

        # Récupérer les extra keys si elles existent
        reponse = getattr(record, "reponse", None)

        if isinstance(reponse, list):
            if len(reponse) > 3:
                reponse = reponse[:3]

        if isinstance(reponse, dict):
            for current_key in reponse:
                if len(reponse) > 3:
                    reponse[current_key] = reponse[current_key][:3]

        data_to_insert = {
            "date_envoi": log_timestamp,
            "jour": jour,
            "heure": heure,
            "type_requete": getattr(record, "type_requete", None),
            "url": getattr(record, "url", None),
            "route": getattr(record, "route", None),
            "code_http": getattr(record, "code_http", None),
            "methode_http": getattr(record, "methode_http", None),
            "reponse": getattr(record, "reponse", None),
            "body": getattr(record, "body", None),
            "level": level,
            "sql_query": getattr(record, "sql_query", None),
            "data_query": getattr(record, "data_query", None),
            "message": getattr(record, "message", None),
            "message_erreur": getattr(record, "exc_text", None),
        }

        query = """INSERT INTO logs (date_envoi, jour, heure,
                    type_requete, url, route, code_http, reponse, body,
                    level, sql_query, data_query, message, message_erreur)
                    VALUES (%(date_envoi)s, %(jour)s, %(heure)s,
                            %(type_requete)s, %(url)s, %(route)s, %(code_http)s, %(reponse)s, %(body)s,
                            %(level)s, %(sql_query)s, %(data_query)s, %(message)s, %(message_erreur)s)

        """
        try:
            with psycopg2.connect(
                host=self.host,
                database=self.which_database(),
                user=self.user,
                password=self.password,
                port=self.port,
            ) as connector:
                with connector.cursor(cursor_factory=DictCursor) as cursor:
                    try:
                        cursor.execute(query, data_to_insert)
                        connector.commit()
                    except Exception as e:
                        print(f"Failed to insert log entry: {e}")

        except OperationalError as e:
            print(f"Failed to insert log entry: {e}")


# Configuration du logger


def setup_logger(
    host: str,
    db_dev_name: str,
    db_deployment_name: str,
    user: str,
    password: str,
    port: str,
    app_statut: str,
):
    logger = logging.getLogger("DatabaseLogger")
    logger.setLevel(logging.DEBUG)
    db_handler = DatabaseLogHandler(
        host, db_dev_name, db_deployment_name, user, password, port, app_statut
    )
    logger.addHandler(db_handler)
    return logger


class Database:
    def __init__(
        self,
        host: str,
        db_dev_name: str,
        db_deployment_name: str,
        user: str,
        password: str,
        port: str,
        app_statut: str,
        app_logger: DatabaseLogHandler,
    ):
        self.host = host
        self.db_dev_name = db_dev_name
        self.db_deployment_name = db_deployment_name
        self.user = user
        self.password = password
        self.port = port
        self.app_statut = app_statut
        self.app_logger = app_logger

    def which_database(self) -> str:
        if self.app_statut == "DEV":
            return self.db_dev_name

        if self.app_statut == "DEPLOYMENT":
            return self.db_deployment_name

    def execute_query(
        self, query: str, data_placeholders=None
    ) -> None | list[dict[str, any]]:
        try:
            with psycopg2.connect(
                host=self.host,
                database=self.which_database(),
                user=self.user,
                password=self.password,
                port=self.port,
            ) as connector:
                with connector.cursor(cursor_factory=DictCursor) as cursor:
                    try:
                        """self.app_logger.info(
                            msg="SQL",
                            extra={"sql_query": query, "data_query": data_placeholders},
                        )"""
                        cursor.execute(query, data_placeholders)

                        # Principalement SELECT
                        if query.strip().upper().startswith("SELECT"):
                            columns = [desc.name for desc in cursor.description]
                            results = [
                                dict(zip(columns, row)) for row in cursor.fetchall()
                            ]
                            return results

                        # Principalement CREATE, DROP, UPDATE, INSERT, DELETE
                        else:
                            connector.commit()

                    except Exception as e:
                        ##self.app_logger.exception(msg=e)
                        print(e)
                        raise Exception("Erreur interne") from e

        except OperationalError as e:
            print(f"Nombre de connexions sur la base de données atteintes : {e}")

        except Exception as e:
            print(f"Une erreur est survenue: {e}")

    # Uniquement pour INSERT pour le moment
    def execute_queries(self, queries: list[tuple[str, tuple]]) -> None:
        try:
            with psycopg2.connect(
                host=self.host,
                database=self.which_database(),
                user=self.user,
                password=self.password,
                port=self.port,
            ) as connector:
                with connector.cursor(cursor_factory=DictCursor) as cursor:
                    try:
                        for query, data_placeholders in queries:
                            """self.app_logger.info(
                                msg="SQL",
                                extra={
                                    "sql_query": query,
                                    "data_query": data_placeholders,
                                },
                            )"""
                            cursor.execute(query, data_placeholders)
                        connector.commit()
                    except Exception as e:
                        print(f"Une erreur est survenue: {e}")

        except OperationalError as e:
            print(f"Nombre de connexions sur la base de données atteintes : {e}")
        except Exception as e:
            print(f"Une erreur est survenue: {e}")

    """ Insérer plusieurs données """

    def insert_many_data(self, table: str, data: list[dict[str, any]]) -> None:
        with psycopg2.connect(
            host=self.host,
            database=self.which_database(),
            user=self.user,
            password=self.password,
            port=self.port,
        ) as connector:
            with connector.cursor(cursor_factory=DictCursor) as cursor:
                colonnes = ", ".join([f'"{colonne}"' for colonne in data[0].keys()])
                valeurs = ", ".join([f"%({colonne})s" for colonne in data[0].keys()])
                valeurs = "(" + valeurs + ")"
                query = f"INSERT INTO {table} ({colonnes}) VALUES %s;"
                """ self.app_logger.info(
                    msg="SQL", extra={"sql_query": query, "data_query": data[:5]}
                ) """
                execute_values(cur=cursor, sql=query, argslist=data, template=valeurs)
                connector.commit()

    """ Commandes annexes d'informations """

    def colname_data(self, nom_table: str):
        with psycopg2.connect(
            host=self.host,
            database=self.which_database(),
            user=self.user,
            password=self.password,
            port=self.port,
        ) as connector:
            with connector.cursor(cursor_factory=DictCursor) as cursor:
                query = f"SELECT * FROM {nom_table} LIMIT 0"
                cursor.execute(query)
                colonnes_table = [desc[0] for desc in cursor.description]
                return colonnes_table


class SqlMethods:
    def __init__(self, current_app_database: Database):
        self.current_app_database = current_app_database

    def generate_select_clause(self, nom_table: str, colonnes: tuple[str]) -> str:
        if colonnes is not None and type(colonnes) != tuple:
            raise ValueError(
                "Le paramètre colonnes n'est pas renseigné au bon format. tuple[str] attendu"
            )

        colonnes_str = ", ".join(colonnes)
        select_query = f"SELECT {colonnes_str} FROM {nom_table}"
        return select_query

    def generate_delete_clause(self, nom_table: str) -> str:
        select_query = f"DELETE FROM {nom_table}"
        return select_query

    def generate_update_clause(
        self, nom_table: str, data_to_update: dict[str, any]
    ) -> str:
        updated_data_query = ", ".join(
            [f"""{key} = %({key})s""" for key in data_to_update.keys()]
        )
        update_query = f"UPDATE {nom_table} SET {updated_data_query}"
        return update_query

    def generate_insert_clause(
        self, nom_table: str, data_to_insert: dict[str, any]
    ) -> str:
        colonnes = ", ".join([f'"{colonne}"' for colonne in data_to_insert.keys()])
        inserted_data_query = ", ".join([f"%({key})s" for key in data_to_insert.keys()])
        insert_query = (
            f"INSERT INTO {nom_table} ({colonnes}) VALUES ({inserted_data_query})"
        )
        return insert_query

    def generate_condition_clause(self, conditions: tuple[str]) -> str:
        if type(conditions) != tuple:
            raise ValueError(
                "Le paramètre conditions n'est pas renseigné au bon format. tuple[str] attendu"
            )
        conditions_query = " AND ".join(conditions)
        condition_clause = f"WHERE {conditions_query}"
        return condition_clause

    def generate_condition_clause_old(
        self, conditions: list[dict[str, any, str]]
    ) -> str:
        if type(conditions) != list:
            raise ValueError(
                "Le paramètre conditions n'est pas renseigné au bon format. list[dict[str, any]] attendu"
            )

        tmp_conditions = []

        for condition in conditions:
            if not set(["colonne", "valeur"]).issubset(condition.keys()):
                raise KeyError(
                    "Une des clés suivantes n'est pas présente dans l'une de vos conditions: colonne, valeur"
                )

            if type(condition["valeur"]) == list:
                tmp_conditions.append(
                    f"""{condition["colonne"]} {condition["operateur"]} ({", ".join(f"'{valeur}'" for valeur in condition["valeur"])})"""
                )

            if type(condition["valeur"]) == str:

                tmp_conditions.append(
                    f"""{condition["colonne"]} {condition["operateur"]} '{condition["valeur"]}'"""
                )

        conditions_query = " AND ".join(tmp_conditions)
        condition_clause = f"WHERE {conditions_query}"

        return condition_clause

    def generate_orderby_clause(
        self, colonnes: tuple[str], colonnes_orderby: tuple[str]
    ) -> str:
        if type(colonnes_orderby) != tuple:
            raise ValueError(
                "Le paramètre colonne_orderby n'est pas renseigné au bon format. tuple[str] attendu"
            )

        if not set(colonnes_orderby).issubset(colonnes):
            raise ValueError(
                "Le paramètre colonne_orderby doit être un sous-ensemble du paramètre colonnes"
            )

        orderby_str = ", ".join(colonnes_orderby)
        orderby_clause = f"ORDER BY {orderby_str}"

        return orderby_clause

    def query_builder_table(
        self, type_action: str, nom_table: str, colonnes: tuple[dict[str, str]] = None
    ) -> str:
        type_action = type_action.upper()
        actions = ("CREATE", "DROP")

        if type_action not in actions:
            raise ValueError(
                f"type_action doit être une des valeurs suivantes: {actions}"
            )

        if type_action == "CREATE":
            if colonnes is None:
                raise ValueError(
                    """Le paramètre colonnes n'est pas renseigné.
                        Format attendu : tuple[dict[str, str]]. Exemple: [{"nom_colonne":"ma_colonne", "type_colonne": "TEXT"}]"""
                )

            if type(colonnes) is not list:
                raise ValueError(
                    """Le paramètre colonnes n'est pas renseigné au bon format.
                        Format attendu : tuple[dict[str, str]]. Exemple: [{"nom_colonne":"ma_colonne", "type_colonne": "TEXT"}]"""
                )

        if type_action == "DROP":
            return f"DROP TABLE IF EXISTS {nom_table}"

        if type_action == "CREATE":
            query = f"CREATE TABLE IF NOT EXISTS {nom_table} ("

            for colonne in colonnes:
                query += f"""{colonne["nom_colonne"]} {colonne["type_colonne"]}, """

            query = query[:-2] + ")"

            return query

    def query_builder_crud(
        self,
        crud_action: str,
        nom_table: str,
        colonnes: tuple[str] = None,
        data_placeholders: dict[str, any] = None,
        conditions: tuple[dict[str, any, str]] = None,
        colonnes_orderby: tuple[str] = None,
    ) -> str:

        crud_action = crud_action.upper()
        crud_actions = ["SELECT", "INSERT", "UPDATE", "DELETE"]

        if crud_action not in crud_actions:
            raise ValueError(
                f"crud_action doit être une des valeurs suivantes: {crud_actions}"
            )

        if colonnes == ("*",):
            colonnes = self.current_app_database.colname_data(nom_table=nom_table)
            colonnes = tuple(colonnes)

        if crud_action == "SELECT":
            query = self.generate_select_clause(nom_table=nom_table, colonnes=colonnes)

        elif crud_action == "INSERT":
            query = self.generate_insert_clause(
                nom_table=nom_table, data_to_insert=data_placeholders
            )

        elif crud_action == "UPDATE":
            query = self.generate_update_clause(
                nom_table=nom_table, data_to_update=data_placeholders
            )

        elif crud_action == "DELETE":
            query = self.generate_delete_clause(nom_table=nom_table)

        # Ajout des conditions

        if conditions is not None:
            query = query + " " + self.generate_condition_clause(conditions=conditions)

        # Trier les données
        if colonnes_orderby is not None:
            query = (
                query
                + " "
                + self.generate_orderby_clause(
                    colonnes=colonnes, colonnes_orderby=colonnes_orderby
                )
            )

        return query
