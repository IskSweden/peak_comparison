import pandas as pd

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

    def compute_all(self):
        df = self.df

        # Gesamtverbrauch = Bezug + Eigenverbrauch
        df['Gesamtverbrauch'] = df['Bezug'] + df['Eigenverbrauch']

        # PV_Bezug = Rueck + Eigenverbrauch
        df['PV_Bezug'] = df['Rueck'] + df['Eigenverbrauch']

        # Bezug_abgeregelt = Gesamt - 20% of PV-BEZUG

        # change to variable depending on negative value of SRL. (1(-x))

        df['Bezug_abgeregelt'] = df['Gesamtverbrauch'] - 0.2 * df['PV_Bezug']

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
            records.append({ "month": month_str, "type": "Bezug", "peak": round(row['Bezug'], 2) })
            records.append({ "month": month_str, "type": "Bezug_abgeregelt", "peak": round(row['Bezug_abgeregelt'], 2) })

        return records
