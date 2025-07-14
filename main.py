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

    print("Processing...")
    processor = ConsumptionProcessor(bezug, rueck, eigenv)
    records = processor.get_monthly_peaks_long_format()

    # Stats output
    df_full = processor.compute_all()

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
    

    # Exporting to CSV
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    output_path = config.OUTPUT_DIR / "monthly_peaks_long.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"JSON export complete: {output_path}")

    print("Creating plots...")
    plot_all()
    print(f"Plots created at in data folder!")
    
if __name__ == "__main__":
    main()
