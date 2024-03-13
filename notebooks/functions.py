# This file is used to store all the functions so that they can be used in the notebooks

import requests
import pandas as pd
from datetime import datetime, timedelta
import seaborn as sns
import plotly.express as px


def obtenir_token(client_id, client_secret):
    url_token = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api_offresdemploiv2 o2dsoffre",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url_token, data=auth_data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erreur lors de la requête : {response.text}")
    else:
        data = response.json()
        return data["access_token"]


def rechercher_offres_month_year_keyword(token, mot_cle, mois, annee, nb_offres=10):
    url_offres = "https://api.emploi-store.fr/partenaire/offresdemploi/v2/offres/search"
    headers = {"Authorization": f"Bearer {token}"}
    debut_mois = f"{annee}-{mois:02d}-01T00:00:00Z"
    fin_mois = f"{annee}-{mois:02d}-30T00:00:00Z"
    params = {
        "motsCles": mot_cle,
        "range": f"0-{nb_offres-1}",
        "minCreationDate": debut_mois,
        "maxCreationDate": fin_mois,
    }
    response = requests.get(url_offres, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur lors de la requête : {response.text}")


def get_job_offers_by_keyword(access_token, key_word):
    url = "https://api.emploi-store.fr/partenaire/offresdemploi/v2/offres/search"
    params = {"motsCles": key_word}
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_job_offer_by_sector_date(access_token, sector, minDate, maxDate):
    url = "https://api.emploi-store.fr/partenaire/offresdemploi/v2/offres/search"
    params = {
        "secteurActivite": sector,
        "minDate": minDate,
        "maxDate": maxDate,
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, params=params)
    try:
        return response.json()
    except:
        pass


def get_job_offer_by_sector(access_token, sector):
    url = "https://api.emploi-store.fr/partenaire/offresdemploi/v2/offres/search"
    params = {
        "secteurActivite": sector,
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, params=params)
    try:
        return response.json()
    except:
        pass


# Function to generate date ranges for the last 12 months
def generate_last_n_months(n):
    today = datetime.now()
    for month_back in range(1, n + 1):
        start_month = today - timedelta(days=30 * month_back)
        end_month = (start_month + timedelta(days=30)).strftime("%Y-%m-%d")
        start_month = start_month.strftime("%Y-%m-%d")
        yield start_month, end_month


def generate_data_all_sectors_last_n_months(df, access_token, n=12):
    """
    Function to generate data for all sectors for the last n months
    
    Parameters:
    df: DataFrame
    access_token: str
    n: int

    Returns:
    DataFrame
    """
    for start_month, end_month in generate_last_n_months(n=12):
        print(f"Recherche pour la période : {start_month} à {end_month}")
        for sector in range(1, 100):
            formatted_sector = f"{sector:02}"
            job_offers = get_job_offer_by_sector_date(
                access_token, formatted_sector, start_month, end_month
            )

            if job_offers and "resultats" in job_offers:
                df_temp = pd.json_normalize(job_offers["resultats"])
                df_temp["Secteur"] = sector  # Add sector information
                df_temp["Date"] = (
                    f"{start_month} to {end_month}"  # Add date range information
                )
                df = pd.concat([df, df_temp], ignore_index=True)
            else:
                print(
                    f"Pas de données trouvées ou erreur pour le secteur : {formatted_sector} entre {start_month} et {end_month}"
                )
    return df
