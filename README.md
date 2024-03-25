# Data_Pole_Emploi Project README

## Overview
This is a Data Science for Business project focused on leveraging data from Pole Emploi. The objective is to develop a data-driven solution that addresses specific business needs by retrieving data through APIs, analyzing, and exploiting this data to create predictive models, and finally, industrializing these models for real-world applications.

## How to Run the Proof of Concept (POC)

1. **Setting up the Streamlit Application:**
   - Navigate to the `streamlit_app_poc` directory.
   - Install the required packages using the following command:
     ```bash
     pip install -r requirements.txt
     ```
   - Download the pre-trained Word2Vec model from the following link: [FastText French Vector](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.fr.300.bin.gz).
   
2. **Running the Application:**
   - Inside the `streamlit_app_poc` directory, run the following command to start the Streamlit application:
     ```bash
     streamlit run main.py
     ```

For more details check the streamlit_app_poc/readme.md

## Resources
For resources and further understanding, refer to the `notebooks` directory. This contains Jupyter notebooks used for loading and analyzing data and testing models. It provides a comprehensive guide through the data processing and model evaluation phases of the project.

## Tasks (Travail à faire)

### Objective (Objectif):
Develop a complete Data Science project in a business context from start to finish.

### Sub-Objectives (Sous-objectifs):
- Retrieve data from an API.
- Understand and analyze the data to make it actionable.
- Define a business need that the data can address.
- Create a predictive model.
- Industrialize the model for practical application.
- Present the results in a professional setting.

## Structure
- `data`: Contains the offers retrieved from the Pole Emploi API.
- `notebooks`: Contains Jupyter notebooks for data processing and analysis, and for testing the models.
- `services`: Contains Python scripts like `data_processing.py` for data processing.
- `streamlit_app_poc`: Contains the proof of concept of our project in Streamlit.

## Requirements
- Python 3.x
- Libraries as listed in `requirements.txt`
- FastText French Vector for model training.

## Contribution
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
