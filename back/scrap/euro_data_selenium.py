from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import datetime

from config import app_database, app_sql


# Configurer les options du navigateur
def scrap_from_france_24():
    options = Options()
    options.headless = (
        True  # Exécuter en mode headless pour ne pas ouvrir de fenêtre de navigateur
    )

    # Initialiser le driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    # URL de la page L'Équipe à scraper
    url = "https://www.france24.com/fr/euro-2024-calendrier-et-resultats"
    driver.get(url)

    # Attendre que la page soit complètement chargée
    driver.implicitly_wait(10)

    # Accepter les cookies
    driver.find_element(By.CSS_SELECTOR, "#didomi-notice-disagree-button").click()

    # Extraire les informations des matchs à partir du 29 juin 2024
    matches = []
    elements = driver.find_elements(By.TAG_NAME, "table")

    phases = ["1ère journée", "2éme journée", "3éme journée", "Phase éliminatoire"]

    # Dictionnaire pour traduire les mois français en anglais
    mois_francais = {
        "juin": "June",
        "juillet": "July",
    }

    for i in range(len(elements)):
        element = elements[i]
        phase = phases[i]
        rows = element.find_elements(By.TAG_NAME, "tbody")
        for row in rows:
            if phase == "Phase éliminatoire":
                cells = row.find_elements(By.TAG_NAME, "td")
                # print(len(cells))
                if len(cells) == 1:
                    match_date = cells[0].text
                    match_date = match_date.split(" ")[1:]
                    match_date = " ".join(match_date)
                    # Traduire le mois en anglais
                    for fr, en in mois_francais.items():
                        match_date = match_date.replace(fr, en)
                    match_date = datetime.datetime.strptime(match_date, "%d %B %Y")
                    print(match_date)
                else:
                    heure = datetime.datetime.strptime(cells[0].text, "%H:%M").time()
                    team1 = cells[1].text
                    score_team1 = cells[3].text
                    score_team2 = cells[5].text
                    team2 = cells[7].text

                    match_info = {
                        "date_match": match_date,
                        "heure_match": heure,
                        "equipe_a": team1,
                        "equipe_b": team2,
                        "score_a": score_team1,
                        "score_b": score_team2,
                        # "phase": phase,
                    }
                    print(match_info)
                    matches.append(match_info)

    query = app_sql.generate_insert_clause("matchs", matches[0])
    queries = [(query, matche) for matche in matches]
    app_database.execute_queries(queries=queries)

    # Fermer le driver
    driver.quit()
