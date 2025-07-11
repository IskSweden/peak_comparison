from loader import ExcelLoader
from processor import ConsumptionProcessor
import config
import os
import json

def main():
    print("Loading data...")
    loader = ExcelLoader()
    bezug, rueck, eigenv = loader.get_combined_data()

    print("Processing...")
    processor = ConsumptionProcessor(bezug, rueck, eigenv)
    records = processor.get_monthly_peaks_long_format()

    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    output_path = config.OUTPUT_DIR / "monthly_peaks_long.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"JSON export complete: {output_path}")

if __name__ == "__main__":
    main()
