import pandas as pd
from datetime import datetime, timedelta
import requests
from configparser import ConfigParser


def get_config(section, key):
    parser = ConfigParser()
    parser.read("config.ini")  # Ensure this path is correct
    return parser.get(section, key)


def obtenir_token():
    client_id = get_config("Pole_Emploi", "CLIENT_ID")
    client_secret = get_config("Pole_Emploi", "CLIENT_SECRET")
    url_token = get_config("Pole_Emploi", "TOKEN_URL")
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


def get_job_offer_by_sector_date(access_token, sector, minDate, maxDate):
    url = get_config("Pole_Emploi", "JOB_OFFERS_URL")
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


import os


def save_monthly_job_offers(df, access_token):
    """
    Fetches the latest job offers for the last month, checks if they exist in the main CSV,
    and if not, adds them.

    Parameters:
    df: DataFrame containing the existing job offers.
    access_token: str, access token for the API.
    """
    # Generate dates for the last month
    last_month_start, last_month_end = next(generate_last_n_months(1))

    # Name of the monthly file
    monthly_file_name = (
        f"data/monthly_job_offers_{last_month_start}_to_{last_month_end}.csv"
    )

    # If monthly file does not exist, create it and fetch data
    if not os.path.exists(monthly_file_name):
        monthly_df = pd.DataFrame()  # Create an empty DataFrame for monthly data
        for sector in range(1, 100):  # Assuming sector range is from 1 to 99
            formatted_sector = f"{sector:02}"
            job_offers = get_job_offer_by_sector_date(
                access_token, formatted_sector, last_month_start, last_month_end
            )
            if job_offers and "resultats" in job_offers:
                df_temp = pd.json_normalize(job_offers["resultats"])
                df_temp["Secteur"] = sector  # Add sector information
                df_temp["Date"] = (
                    f"{last_month_start} to {last_month_end}"  # Add date range information
                )
                monthly_df = pd.concat([monthly_df, df_temp], ignore_index=True)

        # Save the monthly data if it's not empty
        if not monthly_df.empty:
            monthly_df.to_csv(monthly_file_name, index=False)

    # Now check and update the master CSV
    if os.path.exists(monthly_file_name):
        new_data_df = pd.read_csv(monthly_file_name)
        # Concatenate new data with old data and drop duplicates
        updated_df = (
            pd.concat([df, new_data_df]).drop_duplicates().reset_index(drop=True)
        )
        # Save the updated data back to the main CSV
        updated_df.to_csv("data/concatenated_offers.csv", index=False)


# Assuming existing_df is your loaded DataFrame from 'concatenated_offers.csv'
existing_df = pd.read_csv("data/concatenated_offers.csv")
access_token = (
    obtenir_token()
)  # Ensure you have your client_id and client_secret passed here
save_monthly_job_offers(existing_df, access_token)
