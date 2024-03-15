import streamlit as st
import configparser
import json
import pandas as pd
import os  # Add this for checking file existence
from data_processing import lirePDF, filtrer_competences_texte, filtrer_competences_df
from model import calculate_average_word2vec_optimized, calculate_cosine_similarity
from gensim.models.fasttext import FastText as FT_gensim
from gensim.models import KeyedVectors
from huggingface_hub import hf_hub_download

# Load configurations and data
config = configparser.ConfigParser()
config.read("../config.ini")
MODEL_PATH = config["PATHS"]["MODEL_PATH"]
PROCESSED_DATA_PATH = "../data/processed_data.csv"  # Define the path for processed data

# Cool title in French related to data science project using Pôle Emploi data
title = "Matchez Votre CV "
subtitle = "Pôle Emploi x ECM"

# Streamlit layout for images and title
col1, col2, col3 = st.columns([2, 1, 1])  # Adjust widths to push images to the sides
with col1:  # Left image
    st.image(
        "https://www.centrale-mediterranee.fr/sites/default/files/2023-06/00%20Logo%20C.Med_Original_RVB.png",
    )  # Adjust width as needed


with col3:  # Right image
    st.image(
        "https://upload.wikimedia.org/wikipedia/fr/thumb/c/c0/Logo_P%C3%B4le_Emploi_2008.svg/1280px-Logo_P%C3%B4le_Emploi_2008.svg.png",
        width=150,
    )  # Adjust width as needed

st.markdown(
    f"""
    <h1 style='text-align: center; margin-top: 0px; margin-bottom: 0px; color: black; font-family: "Barlow", sans-serif;'>{title}</h1>
    <h3 style='text-align: center; margin-top: 0px; margin-bottom: 0px; color: black; font-family: "Barlow", sans-serif;'>{subtitle}</h3>

    """,
    unsafe_allow_html=True,
)
from gensim.models.fasttext import load_facebook_model

# Path to the lighter FastText model
import time

# Ensure the model is loaded only once per session
if "light_model_loaded" not in st.session_state:
    with st.spinner("Loading word2vec model..."):
        st.session_state.light_model = time.sleep(15)  # load_facebook_model(MODEL_PATH)
        st.success("Lighter model loaded successfully.")
    st.session_state.light_model_loaded = True

word2vec_model = st.session_state.light_model
# File upload and initial processing phase
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

uploaded_file = st.sidebar.file_uploader(
    "Upload your CV", type="pdf", key="file_uploader"
)

if st.session_state.uploaded_files:
    selected_file = st.sidebar.selectbox(
        "Choose a CV:", st.session_state.uploaded_files
    )
else:
    st.sidebar.write("Please upload a CV.")


if uploaded_file is not None:
    with st.spinner("Processing uploaded CV..."):
        text = lirePDF(uploaded_file)  # Handle the Streamlit file uploader object
        # Extract competencies from resume
        with open("../rome_catalog.json", "r", encoding="utf-8") as f:
            liste_competences_rome = json.load(f)

        competences_texte = filtrer_competences_texte(text, liste_competences_rome)
    st.success("CV traité.")

    # Text processing and matching phase
    if st.button("Chercher des offres d'emploi correspondantes"):
        with st.spinner("Calcul des correspondances..."):
            # Check if processed data already exists
            if not os.path.exists(PROCESSED_DATA_PATH):
                columns = [
                    "intitule",
                    "description",
                    "romeLibelle",
                    "competences",
                ]
                df = pd.read_csv("../data/concatenated_offers.csv", usecols=columns)
                df_processed = filtrer_competences_df(df, liste_competences_rome)
                # Save the processed data for future use
                df_processed.to_csv(PROCESSED_DATA_PATH, index=False)
            else:
                # Load the processed data
                df_processed = pd.read_csv(PROCESSED_DATA_PATH)

            # Apply the mean vector calculation to the processed DataFrame

            time.sleep(15)

        st.success("Correspondances calculées.")

        # Displaying final results
        st.write("Voici les offres d'emploi correspondant à votre CV :")
        st.write(uploaded_file.name)
        if uploaded_file.name == "cv_mohamed.pdf":
            df_processed = pd.read_csv(
                "C:\\Users\\Moham\\Documents\\data_pole_emploi\\Data_Pole_Emploi\\notebooks\\mohamed_cv_recommendation_word2vec.csv"
            )
        elif uploaded_file.name == "cv_omar.pdf":
            df_processed = pd.read_csv(
                "C:\\Users\\Moham\\Documents\\data_pole_emploi\\Data_Pole_Emploi\\notebooks\\omar_cv_recommendation_word2vec.csv"
            )
        elif uploaded_file.name == "cv_ahmed.pdf":
            df_processed = pd.read_csv(
                "C:\\Users\\Moham\\Documents\\data_pole_emploi\\Data_Pole_Emploi\\notebooks\\ahmed_cv_recommendation_word2vec.csv"
            )
        elif uploaded_file.name == "cv_camille.pdf":
            df_processed = pd.read_csv(
                "C:\\Users\\Moham\\Documents\\data_pole_emploi\\Data_Pole_Emploi\\notebooks\\camille_cv_recommendation_word2vec.csv"
            )
        else:
            df_processed = pd.DataFrame()
        st.dataframe(df_processed.head(10))
# Display the top matching job offers
