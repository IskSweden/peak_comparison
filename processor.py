import pandas as pd
from srl_loader import load_monthly_curtailment_factors


class ConsumptionProcessor:
    def __init__(self, bezug_df, rueck_df, eigenv_df):
        # Prepare base dataframe
        self.df = pd.DataFrame(index=bezug_df.index)
        self.df['Bezug'] = bezug_df['value']

        # Align Rueck with Bezug
        rueck_df = rueck_df[~rueck_df.index.duplicated(keep='first')]
        self.df['Rueck'] = rueck_df['value'].reindex(self.df.index, method='nearest')

        # Merge Eigenverbrauch with timestamp
        eigenv_df = eigenv_df[~eigenv_df.index.duplicated(keep='first')].sort_index().reset_index()
        eigenv_df.columns = ['eigen_time', 'Eigenverbrauch']
        self.df = self.df.reset_index().rename(columns={'index': 'timestamp'}).sort_values('timestamp')
        self.df = pd.merge_asof(
            self.df,
            eigenv_df,
            left_on='timestamp',
            right_on='eigen_time',
            direction='nearest'
        ).drop(columns=['eigen_time']).set_index('timestamp')

        self.monthly_factors = load_monthly_curtailment_factors()


    def compute_all(self):
        df = self.df

        # Gesamtverbrauch = Bezug + Eigenverbrauch
        df['Gesamtverbrauch'] = df['Bezug'] + df['Eigenverbrauch']

        # PV_Bezug = Rueck + Eigenverbrauch
        df['PV_Bezug'] = df['Rueck'] + df['Eigenverbrauch']

        df['month'] = df.index.month.astype(str).str.zfill(2)

        df['curtailment_factor'] = df ['month'].map(self.monthly_factors).fillna(0.2)

        df['Bezug_abgeregelt'] = df['Gesamtverbrauch'] + 1 * df['Eigenverbrauch']

        return df

    def get_monthly_peaks_long_format(self):
        df = self.compute_all()

        # Monthly peaks
        monthly = df.resample('ME').agg({
            'Bezug': 'max',
            'Bezug_abgeregelt': 'max'
        })

        # Convert to long format
        records = []
        for month, row in monthly.iterrows():
            month_str = month.strftime('%Y-%m')
            raw = round(row['Bezug'], 2)
            abg = round(row['Bezug_abgeregelt'], 2)
            delta = round(abg - raw, 2)

            records.append({
                "month": month_str,
                "type": "Bezug",
                "peak": raw,
                })
            records.append({
                "month": month_str,
                "type": "Bezug_abgeregelt",
                "peak": abg,
                "Delta zu Bezug": delta
                })

        return records
