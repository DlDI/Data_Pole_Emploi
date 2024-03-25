# README for Data_Pole_Emploi Streamlit Application

## Overview

This Streamlit application is specifically designed for the Data_Pole_Emploi project, aiming to assist in processing job applications. It efficiently matches job seekers' CVs with the most suitable job offers from Pôle Emploi, leveraging advanced NLP (Natural Language Processing) techniques.

## Setup and Installation

### Prerequisites

- Python 3.x installed on your local system.
- Access to a terminal or command prompt.

### Steps

1. **Clone or download the project repository.**
2. **Navigate to the Streamlit application directory:**
   ```bash
   cd path/to/streamlit_app_poc
   ```
3. **Install necessary Python packages:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure paths:**
   - Open `config.ini` in a text editor.
   - Update `PDF_PATH` under `[PATHS]` with the directory containing your PDF files.
   - Update `MODEL_PATH` with the full path to your Word2Vec model file.

### Running the Application

Execute the following command within the Streamlit application directory:

```bash
streamlit run main.py
```

Navigate to the displayed URL in your web browser to interact with the application.

## Application Usage

- **Uploading Your CV:** Use the sidebar option to upload your CV in PDF format.
- **Processing Your CV:** The application will analyze your CV to extract competencies.
- **Job Matching:** Based on extracted competencies, the system will match and display relevant job offers from Pôle Emploi.

## Application Structure

- `app/`: Main application directory with Python scripts.
   - `components.py`: Streamlit components for UI enhancements.
   - `data_processing.py`: Functions for data preprocessing and analysis.
   - `main.py`: Central script that runs the Streamlit application.
   - `model.py`: Implements the NLP model and matching algorithms.
   - `utils.py`: Contains auxiliary functions for general utilities.
- `notebooks/`: Contains Jupyter notebooks for data exploration and model testing.
- `requirements.txt`: Lists all dependencies necessary to run the application.
- `config.ini`: Configuration file for setting paths and other variables.
- `rome_catalog.json`: Catalog for job competencies and roles.

## Feature Highlights

- **Interactive Interface:** Easy-to-use interface for uploading and analyzing CVs.
- **Advanced Matching:** Utilizes state-of-the-art NLP techniques for accurate job matching.
- **PDF Processing:** Extracts text directly from PDFs for analysis.

## Contributing

We welcome contributions! Please check out our contributing guidelines for more information on how to get involved.

## License

This project is licensed under the MIT License. Refer to the `LICENSE` file for more information.
