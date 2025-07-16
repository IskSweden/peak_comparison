---
title: "Dokumentation"
author: "Isak Skoog"
date: "2025-07-16"
---


# Peak Vergleich Bezug vs Bezug abgeregelt
Dieses Dokument dient den Zweck die Installation, Modifikation und weiterentwickelung des Python Scripts einfacher zu machen

## Inhaltsverzeichnis
1. [Installations Guide](#installations-guide-peak-comparison)
2. [Dokumentation Code](#dokumentation-erlifeld-peaks) \
    2.1 [Input ](#der-input-kommt-via-7-unterschiedlichen-excel-files-rein-diese-sind-folgend) \
    2.2 [Config.py](#configpy) \
    2.3 [Daten aus Excel](#aus-diesen-excel-files-werden-folgende-daten-geladen) \
    2.4 [Loader.py](#loaderpy) \
    2.5 [SRL_loader.py](#srl_loaderpy) \
    2.6 [Berechnungen im Script](#folgende-berechnungen-werden-im-script-ausgeführt) \
    2.7 [Einstieg in main](#einstieg-punkt-im-mainpy) \
    2.8 [Main.py](#mainpy) \
    2.9 [Output des Scripts](#statistik-und-output)
3. [Grafiken](#grafiken)

---

# Installations Guide Peak Comparison

Um dieses Projekt effektiv nutzen, folge bitte genau diesen Schritten:

1. Klicke auf diesen Link: [https://github.com/IskSweden/peak_comparison](https://github.com/IskSweden/peak_comparison) und lade den Source Code als ZIP herunter. Klicke in Github auf den grünen "Code" Knopf und dann auf "Download ZIP"

2. Extrahiere die ZIP Datei und verschiebe den Ordner an einen sicheren Ort (eg. Dokumenten Ordner anstatt Downloads Ordner)

3. Wie du vielleicht merkst fehlt einen Ordner indem man die Excel Dateien hinzufügen kann. Da diese Teils sensitive Daten enthalten, wurde dieser Ordner nicht auf Github publiziert. (Siehe .gitignore). Um das Programm effektiv nutzen zu können, musst du einen Order auf der gleichenen Ebene erstellen wie die `.py` files. Der Ordner sollte genau *data* bennant sein und 7 Excel Dateien enthalten. Die sollten auch korrekt benannt sein.
Also, auf der gleichen Ebene einen Ordner namens *data* erstellen und dann folgende Files reintun:

- 2023_Lastgang_Bezug.xlsx
- 2024_Lastgang_Bezug.xlsx
- 2023_Lastgang_Ruecklieferung.xlsx
- 2024_Lastgang_Ruecklieferung.xlsx
- Kaltband_Eigenverbrauch_2023.xlsx
- Kaltband_Eigenverbrauch_2024.xslx
- 2024_SRL.xlsx

4. Nach dem die korrekten Excel Dateien an den korrekten Platz getan wurden, muss noch eine kleine sache getan werden, sodass das Programm richtig läuft. Dieses Programm hat sogenannte *"Dependancies"*, was nichts mehr als 3-Anbieter Module, für die Verarbeitung von Excel Dateien und die Erstellung von Grafiken. Diese dependancies (Abhängigkeiten) sind in dem Text file "requirements.txt". Um diese Module zu installieren gibt es ein paar einfache Schritte:
   1. Stelle sicher das Python und pip lokal installiert ist. `python --version | pip --version`
   2. Erstelle im Ordner von dem Projekt eine virtuelle Python Umgebung: `python -m venv venv`
   3. Aktiviere diese Umgebung: `source venv/bin/activate`(Auf mac oder linux) | `source venv/Scripts/activate`(auf windows). Jetzt sollte in der Kommand Linie *(venv)* stehen.
   4. Installiere die Abhänigkeiten von dem *requirements.txt* mit `pip install -r requirements.txt`
   5. Jetzt werden die Module heruntergeladen, einfach warten bis es etwas sagt wie "sucessfully installed".
5. Jetzt ist das Programm bereit zum laufen. Um das Programm zu starten einfach `python main.py` eingeben und warten. Der Output kommt in den neu erstellten *output* Ordner.

---

# Dokumentation Peak Vergleich sollte einem Nutzer, Entwickler oder Reviewer die benötigten Informationen geben, sodass man den Code versteht.

---

## Der Input kommt via 7 unterschiedlichen Excel files rein, diese sind folgend  
- 2023 Lastgang Bezug
- 2024 Lastgang Bezug
- 2023 Lastgang Rücklieferung
- 2024 Lastgang Rücklieferung
- 2024 SRL
- 2023 Eigenverbrauch
- 2024 Eigenverbrauch

---

Diese Input Files sollten in dem Order "data" sein, sodass das Programm findet und weiss wo er die Daten herholen sollte.

Die Files, welche das Script nimmt sind im config.py definiert:

### config.py
```python
# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'output'

# Sheet and Column Configs

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


#SRL Control Energy Data (1 file for all months)
SRL_CONFIG = {
    'file': DATA_DIR / '2024_SRL.xlsx',
    'sheet': 'Zeitreihen0h15',
    'sheet_options': {
        'header': 2,
        'usecols': 'A,G,H',
        'names': ['timestamp', 'SRL_pos_kWh', 'SRL_neg_kWh'],
    }
}
```
Das config.py file wurde auf eine Art geschrieben, sodass zwei Arten von Excel Files aktzeptiert werden, da Eigenverbauch und Bezug + Rücklieferung unterschiedlich formatiert sind. 

Rücklieferung und Bezug haben den Sheet Namen "Rohdaten_1" im Excel, und die Colums sind "Zeitpunkt (Beginn der Messung)" und "Wert". Diese Columns sind standardmässig in den Kolumnen A und B, respektiv.

Eigenverbrauch aber, hat die Daten in den Kolumnen A und E mit den namen "DateTimeUTC" und "15min Wert kW". 

Am Schluss werden noch die SRL daten von dem 2024_SRL.xlsx File importiert. Es nimmt an dass das File 2024_SRL.xlsx heisst und auch im data Ordner ist. Es nimmt an dass das Sheet "Zeitreihen0h15" heisst und die Kolumnen A,G und H sind (timestamp, SRL_pos_kWh und SRL_neg_kWh)

---


## Aus diesen Excel files werden folgende Daten geladen:

- Bezug
- Eigenverbrauch
- SRL in roh (welche noch in faktoren umgewandelt werden)
- Rücklieferung / Rückspeisung

Dies wird in zwei unterschiedlichen files gemacht: `loader.py` und `srl_loader.py`

---

### loader.py
```python
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

```
Diese Klasse enhaltet 3 Funktionen, für das Laden des Bezugs, Rücklieferung und Eigenverbrauch. Aber es wird nicht zwischen diesen drei unterschieden, sonder eher durch die unterschiedliche Struktur, welche in dem [config.py](#configpy) definiert ist.

Die SRL Daten werden im File `srl_loader.py` geladen.

---

### srl_loader.py
```python
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

    return monthly_factors

```
Diese Funktion speichert ein Dictionary namen `monthly_factors` welche die Faktoren enthalten für die Rechnung der abgeregelten Bezuges.

In dieser Funktion werden auch die Daten direkt manipuliert mit folgender formel:
$$+SRL + -SRL = Netto$$
$$\frac{Netto}{abs.max.neg} = faktor$$

Mit abs.max.neg wird der absolute höchste negative wert jedes monats (eg. -0.2) gemeint.
Der Faktor ist dann eine Zahl zwischen 0 und 1 (eg. -0.2 = 80% abgeregelt = Faktor 0.8)

---

## Folgende Berechnungen werden im script ausgeführt

Die grundsätzlichen Berechnungen werden im `processor.py` gemacht.

Diese Klasse in `processor.py` hat 2 Hauptfunktionen: 

---

`compute_all`

Diese Funktion hat die Aufgabe, die Rechnungen für den Bezug und den abgeregelten Bezug durchzurechnen.

$Gesamtverbrauch = Bezug + Eigenverbrauch$

$Bezug = Rückspeisung + Eigenverbrauch$

$Bezug Abgeregelt = Gesamtverbrauch - (srlFaktor) * Bezug$

```python
    def compute_all(self):
        df = self.df

        # Gesamtverbrauch = Bezug + Eigenverbrauch
        df['Gesamtverbrauch'] = df['Bezug'] + df['Eigenverbrauch']

        # PV_Bezug = Rueck + Eigenverbrauch
        df['PV_Bezug'] = df['Rueck'] + df['Eigenverbrauch']

        df['month'] = df.index.month.astype(str).str.zfill(2)

        df['curtailment_factor'] = df ['month'].map(self.monthly_factors).fillna(0.2)

        df['Bezug_abgeregelt'] = df['Gesamtverbrauch'] - df['curtailment_factor'] * df['PV_Bezug']

        return df

```

---

`get_monthly_peaks_long_format`

Diese Funktion hat die Aufgabe die data von compute_all zu holen. Danach formattiert es die Daten und werte um, und gestaltet den JSON output so, dass es leserlich ist.

```python
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

```

--- 

Jetzt wurden alle helfer Funktionen und Klassen angeschaut, also bleibt noch der Orchestrator, `main.py`.

In `main.py` werden alle Funktionen logisch und aneinanderhängend ausgeführt, sodass eine volle Pipeline entsteht.

_Start -> Daten aus Excel extrahieren -> Daten verarbeiten -> Daten korrekt speichern -> Grafiken erstellen._

---

## Einstieg Punkt im Main.py

```python
if __name__ == "__main__":
    main()
```

Dies ist eine spezielle Python Funktion, welche dem Interpreter sagt, dass das der Startpunkt von dem Programm ist. Man könnte zwar hier die Logik einbauen, aber das ist unschön.

### main.py

Ich werde das main.py in 3 Teile teilen, sodass es einfacher ist zu verstehen.

---

```python
from loader import ExcelLoader
from processor import ConsumptionProcessor
import config
import os
import json
from plotter import plot_all


def main():
    print("Loading data...")
    loader = ExcelLoader()
    bezug, rueck, eigenv = loader.get_combined_data()
```

Das ist die erste Aufgabe, welche die `main()` Funktion macht.

1. Zuerst initialisiert es die Klasse `ExcelLoader()` aus loader.py als `loader`.
2. Danach definiert es `bezug, rueck, eigenv` als das Resultat von `loader.get_combined_data()`. Dies bedeutet dass die Funktion [get_combined_data()](#loaderpy) aufgerufen wird, und da die Funktion `return bezug, rueck, eigenverbrauch` als return gibt, speichert es diese in respektiver Reihenfolge als die Definitionen hier ab.

---

```python
print("Processing...")
    processor = ConsumptionProcessor(bezug, rueck, eigenv)
    records = processor.get_monthly_peaks_long_format()

    # Stats output
    df_full = processor.compute_all()
```

Nach dem es die rohen Daten aus dem Excel geladet hat und als `bezug, rueck, eigenv` gespeichert wurden, müssen die Daten noch korrekt verarbeitet werden. Das passiert im `main()` direkt danach.

1. Als erstes definiert es `processor` als die Klasse `ConsumptionProcessor(bezug, rueck, eigenv)`. Dazu wird in der `__init__` Funktion noch die SRL Faktoren als `self.monthly_factors` als Resultat von der Funktion [`srl_loader`](#srl_loaderpy) definiert, welches gebraucht wird um die Berechnungen später zu machen.

```python
class ConsumptionProcessor:
    def __init__(self, bezug_df, rueck_df, eigenv_df):
        ...
        ...
        ...
        self.monthly_factors = load_monthly_curtailment_factors()
```

2. Danach definiert es `records` als das Resultat von `processor.get_monthly_peaks_long_format()` welches eine Funktion in der Klasse `ConsumptionProcessor()` ist. Die Funktion [`get_monthly_peaks_long_format()`](#folgende-berechnungen-werden-im-script-ausgeführt) ruft die Funktion `calculate_all` auf und formatiert die Resultate dann zu den monatlichen peaks.
3. Als letztes wird `df_full = processor.compute_all` geruft, um die Rohen verarbeiteten Daten zu haben. Dies wird für den Statistik Output gemacht:

```bash
peak_comparison on master via 🐍 v3.13.5 (.venv)
❯ python main.py
Loading data...
Processing...

Simulation Summary
 • Highest raw Bezug:           2842.50 kW
 • Highest abgeregelt Bezug:   2987.27 kW
 • Minimum Bezug observed:     0.00 kW
 • Average reduction (Δ Bezug): -27.30 kW

SRL-based Curtailment Factors
 • Month 01: 0.624
 • Month 02: 0.832
 • Month 03: 0.564
 • Month 04: 1.000
 • Month 05: 0.835
 • Month 06: 0.833
 • Month 07: 0.744
 • Month 08: 0.546
 • Month 09: 0.984
 • Month 10: 0.631
 • Month 11: 0.709
 • Month 12: 0.635

Max factor: 1.000  |  Min: 0.546  |  Avg: 0.749
JSON export complete: /home/<USER>/Python/peak_comparison/output/monthly_peaks_long.json
Creating plots...
Plots created at in data folder!
```
---
#### Statistik und Output

Als letztes wird im `main.py` einen informativen Output generiert, die Daten werden in einem JSON file gespeichert und es werden mit Hilfe von *matplotlib* Grafiken erstellt. Wie main im Output oben sehen kann.

```python
# General stats
    peak_raw = df_full['Bezug'].max()
    peak_abg = df_full['Bezug_abgeregelt'].max()
    min_raw = df_full['Bezug'].min()
    avg_delta = (df_full['Bezug'] - df_full['Bezug_abgeregelt']).mean()

    print("\nSimulation Summary")
    print(f" • Highest raw Bezug:           {peak_raw:.2f} kW")
    print(f" • Highest abgeregelt Bezug:   {peak_abg:.2f} kW")
    print(f" • Minimum Bezug observed:     {min_raw:.2f} kW")
    print(f" • Average reduction (Δ Bezug): {avg_delta:.2f} kW")

    # Curtailment factor stats
    factors = processor.monthly_factors
    max_factor = max(factors.values())
    min_factor = min(factors.values())
    avg_factor = sum(factors.values()) / len(factors)

    print("\nSRL-based Curtailment Factors")
    for month in sorted(factors.keys()):
        print(f" • Month {month}: {factors[month]:.3f}")

    print(f"\nMax factor: {max_factor:.3f}  |  Min: {min_factor:.3f}  |  Avg: {avg_factor:.3f}")
    

    # Exporting to JSON
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    output_path = config.OUTPUT_DIR / "monthly_peaks_long.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"JSON export complete: {output_path}")

    print("Creating plots...")
    plot_all()
    print(f"Plots created at in data folder!")
```

Hier wird einiges gemacht. Hauptsächlich werden Extrem-Werte, Deltas und Durchschnitte ausgerechnet.
1. Zuerst werden `peak_raw, peak_abg, min_raw` und `avg_delta` definiert und ausgeschrieben.
2. Danach werden die extreme für die SRL gefunden und nach Monat sortiert ausgeschrieben.
3. Als letztes wird mit Hilfe von dem JSON Python Modul ein JSON generiert, welches dann als *"Source of Truth"* für `plotter.py` werden.
4. Und zum schluss wird die funktion `plot_all()` aufgerufen, um die Grafiken zu erstellen. 

---


## Grafiken
Um die Daten gut visuell darzustellen, wird matplotlib genutzt um 7 Grafiken zu erstellen.

Diese und andere Grafiken werden von `plotter.py` generiert und direkt abgespeichert.

```python
import pandas as pd
import matplotlib.pyplot as plt
from config import OUTPUT_DIR
from srl_loader import load_monthly_curtailment_factors

def plot_all():
    json_path = OUTPUT_DIR / "monthly_peaks_long.json"
    df = pd.read_json(json_path)

    df_pivot = df.pivot(index="month", columns="type", values="peak")
    df_delta = df[df["type"] == "Bezug_abgeregelt"][["month", "Delta zu Bezug"]].set_index("month")
    srl_factors = load_monthly_curtailment_factors()

    # Chart 1: Only Bezug
    plt.figure()
    df_pivot["Bezug"].plot(kind="bar", color="#2E86AB", title="Peak Bezug per Month")
    plt.ylabel("kW"); plt.xlabel("Month"); plt.grid(axis="y", linestyle=":")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "plot_1_bezug.png"); plt.close()

    # Chart 2: Only Bezug_abgeregelt
    plt.figure()
    df_pivot["Bezug_abgeregelt"].plot(kind="bar", color="#F28E2B", title="Peak Bezug_abgeregelt per Month")
    plt.ylabel("kW"); plt.xlabel("Month"); plt.grid(axis="y", linestyle=":")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "plot_2_abgeregelt.png"); plt.close()

    # Chart 3: Both Peaks (Stacked)
    plt.figure()
    df_pivot.plot(kind="bar", rot=45, title="Bezug vs. Abgeregelt", color=["#2E86AB", "#F28E2B"])
    plt.ylabel("kW"); plt.xlabel("Month"); plt.grid(axis="y", linestyle=":")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "plot_3_both.png"); plt.close()

    # Chart 4: Delta zu Bezug
    plt.figure()
    df_delta.plot(kind="bar", legend=False, color="#C70039", title="Delta zu Bezug per Month")
    plt.ylabel("Δ kW"); plt.xlabel("Month"); plt.grid(axis="y", linestyle=":")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "plot_4_delta.png"); plt.close()

    # Chart 5: SRL Factors
    plt.figure()
    months = sorted(srl_factors.keys())
    values = [srl_factors[m] for m in months]
    plt.bar(months, values, color="#007545")
    plt.axhline(sum(values)/len(values), linestyle="--", color="gray", label="Ø Avg")
    plt.title("SRL Curtailment Factors per Month")
    plt.ylabel("Factor"); plt.xlabel("Month"); plt.grid(axis="y", linestyle=":")
    plt.tight_layout(); plt.legend()
    plt.savefig(OUTPUT_DIR / "plot_5_srl_factors.png"); plt.close()

    # Chart 6: Everything Together
    plt.figure(figsize=(12, 6))
    df_pivot["Bezug"].plot(label="Bezug", color="#2E86AB", linewidth=2)
    df_pivot["Bezug_abgeregelt"].plot(label="Abgeregelt", color="#F28E2B", linewidth=2)
    df_delta["Delta zu Bezug"].plot(label="Delta", color="#C70039", linestyle="--")
    plt.plot(months, values, label="SRL Factor", color="#007545", marker='o')
    plt.title("All Simulation Signals per Month")
    plt.ylabel("kW / Factor"); plt.xlabel("Month")
    plt.grid(True); plt.legend(); plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "plot_6_all_combined.png")
    plt.close()

    # 7. Line Chart: Bezug vs Abgeregelt (with fill)

    plt.figure(figsize=(10, 5))
    plt.plot(df_pivot.index, df_pivot["Bezug"], label="Bezug", color="#2E86AB", linewidth=2)
    plt.plot(df_pivot.index, df_pivot["Bezug_abgeregelt"], label="Abgeregelt", color="#F28E2B", linewidth=2)

    # Highlight the difference
    plt.fill_between(
        df_pivot.index,
        df_pivot["Bezug"],
        df_pivot["Bezug_abgeregelt"],
        where=(df_pivot["Bezug_abgeregelt"] > df_pivot["Bezug"]),
        interpolate=True,
        color="#C70039",
        alpha=0.3,
        label="Δ Bezug"
    )

    plt.title("Monthly Bezug vs. Abgeregelt (Line Chart)")
    plt.xlabel("Month")
    plt.xticks(rotation=45)
    plt.gca().set_xticks(df_pivot.index[::2])
    plt.ylabel("Peak (kW)")
    plt.grid(True, linestyle=":")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "plot_7_line_bezug_abgeregelt_gap.png")
    plt.close()
```
Hier jede einzelne Grafik zu erklären würde den Rahmen sprengen, aber mehr dazu gibt es auf
[Matplotlib](https://matplotlib.org/).

---


Der volle Source Code ist auf Github verfügbar: [https://github.com/IskSweden/peak_comparison](https://github.com/IskSweden/peak_comparison)
