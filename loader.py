import pandas as pd
import config

class ExcelLoader:
    def __init__(self):
        self.bezug_files = [fp for fp in config.STRUCTURE_TYPE_1['files'] if 'Bezug' in str(fp)]
        self.rueck_files = [fp for fp in config.STRUCTURE_TYPE_1['files'] if 'Rueck' in str(fp)]
        self.eigenverbrauch_files = config.STRUCTURE_TYPE_2['files']

    def load_structure_1(self, filepath):
        sheet = config.STRUCTURE_TYPE_1['sheet']
        options = config.STRUCTURE_TYPE_1['sheet_options']
        df = pd.read_excel(filepath, sheet_name=sheet, **options)
        df.columns = ['timestamp', 'value']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df = df[~df.index.duplicated(keep='first')].copy()
        return df

    def load_structure_2(self, filepath):
        sheet = config.STRUCTURE_TYPE_2['sheet']
        options = config.STRUCTURE_TYPE_2['sheet_options']
        df = pd.read_excel(filepath, sheet_name=sheet, **options)
        df.columns = ['timestamp', 'Eigenverbrauch']
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df = df[~df.index.duplicated(keep='first')].copy()
        return df

    def get_combined_data(self):
        bezug = pd.concat([self.load_structure_1(fp) for fp in self.bezug_files]).sort_index()
        rueck = pd.concat([self.load_structure_1(fp) for fp in self.rueck_files]).sort_index()
        eigenverbrauch = pd.concat([self.load_structure_2(fp) for fp in self.eigenverbrauch_files]).sort_index()
        return bezug, rueck, eigenverbrauch
