# config.py

import os

# Define the base directory where your Excel files are located
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Assumes config.py is in the same directory as your script
DATA_DIR = os.path.join(BASE_DIR, 'data') # Example: a 'data' folder next to your script

# --- Configuration for Excel Files ---

# --- Structure Type 1 Configuration: "Bezug" and "Rücklieferung" files ---
# This structure applies to 4 files: bezug_*.xlsx and ruecklieferung_*.xlsx
STRUCTURE_TYPE_1_NAME = "BezugRuecklieferungData"
STRUCTURE_TYPE_1_FILES = [
    os.path.join(DATA_DIR, '2023_Lastgang_Bezug.xlsx'),
    os.path.join(DATA_DIR, '2023_Lastgang_Ruecklieferung.xlsx'),
    os.path.join(DATA_DIR, '2024_Lastgang_Bezug.xlsx.xlsx'),
    os.path.join(DATA_DIR, '2024_Lastgang_Rueklieferung.xlsx'),
]

STRUCTURE_TYPE_1_SHEETS = {
    'Rohdaten_1': {
        'header': 0, # Assuming the first row contains column headers
        'usecols': "A:B", # Specify column A and B
        'names': ["Zeitpunkt (Beginn der Messung)", "Wert"] # Explicitly name columns if 'header' isn't perfect
    }
}

STRUCTURE_TYPE_1_COLUMNS = {
    "Zeitpunkt (Beginn der Messung)": {'dtype': 'datetime64[ns]'},
    "Wert": {'dtype': 'float64'},
}


# --- Structure Type 2 Configuration: "Eigenverbrauch" files ---
# This structure applies to 2 files: eigenverbrauch_*.xlsx
STRUCTURE_TYPE_2_NAME = "EigenverbrauchData"
STRUCTURE_TYPE_2_FILES = [
    os.path.join(DATA_DIR, 'Kaltband_Eigenverbrauch_2023.xlsx'),
    os.path.join(DATA_DIR, 'Kaltband_Eigenverbrauch_2024.xlsx'),
]

STRUCTURE_TYPE_2_SHEETS = {
    'Sheet1': {
        'header': 0, # Assuming the first row contains column headers
        'usecols': "A,E", # Specify column A and E
        'names': ["DateTimeUTC", "15min Wert kW"] # Explicitly name columns if 'header' isn't perfect
    }
}

STRUCTURE_TYPE_2_COLUMNS = {
    "DateTimeUTC": {'dtype': 'datetime64[ns]'},
    "15min Wert kW": {'dtype': 'float64'},
}


#  General Settings
EXCEL_ENGINE = 'openpyxl' # or 'xlrd' (for .xls), 'odf' (for .ods) - 'openpyxl' is common for .xlsx
MISSING_DATA_REPLACEMENT = None # e.g., 0, 'N/A', or specific fillna strategy

# Placeholder for Calculations
CALCULATIONS_CONFIG = {
    STRUCTURE_TYPE_1_NAME: [],
    STRUCTURE_TYPE_2_NAME: []
}

#  Validation Settings 
VALIDATION_SETTINGS = {
    'strict_column_names': True, # If True, will raise error if column names don't match exactly
    'strict_data_types': True,   # If True, will attempt to enforce dtypes and raise error on failure
    'log_validation_errors': True, # Log errors instead of raising immediately
    'output_error_file': os.path.join(BASE_DIR, 'validation_errors.log')
}