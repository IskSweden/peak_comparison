import os
from pathlib import Path

# === Base Paths ===
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'output'

# === Sheet and Column Configs ===

# Bezug + Rücklieferung files (4 files)
STRUCTURE_TYPE_1 = {
    'name': 'BezugRuecklieferungData',
    'files': [
        DATA_DIR / '2023_Lastgang_Bezug.xlsx',
        DATA_DIR / '2023_Lastgang_Ruecklieferung.xlsx',
        DATA_DIR / '2024_Lastgang_Bezug.xlsx',
        DATA_DIR / '2024_Lastgang_Ruecklieferung.xlsx',
    ],
    'sheet': 'Rohdaten_1',
    'sheet_options': {
        'header': 0,
        'usecols': 'A:B',
        'names': ['Zeitpunkt (Beginn der Messung)', 'Wert'],
    },
    'columns': {
        'Zeitpunkt (Beginn der Messung)': {'dtype': 'datetime64[ns]'},
        'Wert': {'dtype': 'float64'},
    }
}

# PV-Produktion / Eigenverbrauch files (2 files)
STRUCTURE_TYPE_2 = {
    'name': 'EigenverbrauchData',
    'files': [
        DATA_DIR / 'Kaltband_Eigenverbrauch_2023.xlsx',
        DATA_DIR / 'Kaltband_Eigenverbrauch_2024.xlsx',
    ],
    'sheet': 'Sheet1',
    'sheet_options': {
        'header': 0,
        'usecols': 'A,E',
        'names': ['DateTimeUTC', '15min Wert kW'],
    },
    'columns': {
        'DateTimeUTC': {'dtype': 'datetime64[ns]'},
        '15min Wert kW': {'dtype': 'float64'},
    }
}
