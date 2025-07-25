# srl_loader.py
from config import SRL_CONFIG
import pandas as pd


def load_monthly_curtailment_factors() -> dict:
    filepath = SRL_CONFIG['file']
    sheet = SRL_CONFIG['sheet']
    options = SRL_CONFIG['sheet_options']

    df = pd.read_excel(filepath, sheet_name=sheet, **options)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d.%m.%Y %H:%M")
    df = df.dropna(subset=["SRL_neg_kWh"])
    df = df[df['SRL_neg_kWh'] < 0]
    df['SRL_netto_kWh'] = df['SRL_pos_kWh'] + df['SRL_neg_kWh']

    monthly_factors = {}
    for month, group in df.groupby(df['timestamp'].dt.month):
        min_neg_abs = group['SRL_neg_kWh'].abs().max()
        if min_neg_abs == 0:
            continue
        group['SRL_normiert'] = group['SRL_netto_kWh'] / min_neg_abs
        max_norm = group['SRL_normiert'].max()
        monthly_factors[f"{month:02d}"] = round(max_norm, 4)

        clamped_value = min(max_norm, 1.0)

        monthly_factors[f"{month:02d}"] = round(clamped_value, 4)

    return monthly_factors
