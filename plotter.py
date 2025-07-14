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
