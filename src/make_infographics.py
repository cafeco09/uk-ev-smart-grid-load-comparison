from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA = Path("data/processed")
OUT = Path("outputs/infographics")
TABLES = Path("outputs/tables")

OUT.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

annual = pd.read_csv(DATA / "01_like_for_like_annual_energy.csv")
peak = pd.read_csv(DATA / "02_like_for_like_peak_load_scenarios.csv")

annual.to_csv(TABLES / "annual_energy_comparison_table.csv", index=False)
peak.to_csv(TABLES / "smart_grid_peak_comparison_table.csv", index=False)

annual_long = annual.melt(
    id_vars=["brand_group"],
    var_name="metric",
    value_name="value"
)
annual_long.to_csv(DATA / "03_annual_energy_long_form.csv", index=False)

peak_long = peak.melt(
    id_vars=["charging_profile"],
    var_name="metric",
    value_name="value"
)
peak_long.to_csv(DATA / "04_peak_load_long_form.csv", index=False)

def save_current_fig(filename_stem: str):
    plt.savefig(OUT / f"{filename_stem}.png", dpi=240, bbox_inches="tight")
    plt.savefig(OUT / f"{filename_stem}.svg", bbox_inches="tight")
    plt.close()

def add_bar_labels(ax, fmt="{:,.1f}"):
    for container in ax.containers:
        ax.bar_label(container, labels=[fmt.format(v) for v in container.datavalues], padding=4, fontsize=10)

# 00 Summary infographic
tesla = annual[annual["brand_group"] == "Tesla"].iloc[0]
non = annual[annual["brand_group"] == "Non-Tesla BEVs"].iloc[0]
central = peak[peak["charging_profile"] == "Central smart-grid proxy"].iloc[0]

fig, ax = plt.subplots(figsize=(14, 8))
ax.axis("off")

ax.text(0.03, 0.92, "Tesla vs Non-Tesla BEVs: Like-for-like UK smart-grid load",
        fontsize=24, fontweight="bold")
ax.text(0.03, 0.86,
        "Controlled sample: 100,000 vehicles each · 8,900 miles/year · same charging behaviour · weekday 4pm–10pm peak window",
        fontsize=13)

ax.text(0.03, 0.75, "Not an endorsement of Tesla", fontsize=16, fontweight="bold")
ax.text(0.03, 0.70,
        "A controlled comparison showing how efficient engineering can reduce energy demand.",
        fontsize=14)

cards = [
    ("Annual demand", f"Tesla: {tesla['sample_annual_gwh']:.1f} GWh/year", f"Non-Tesla: {non['sample_annual_gwh']:.1f} GWh/year"),
    ("Per vehicle", f"Tesla: {tesla['annual_kwh_per_vehicle']:,.0f} kWh/year", f"Non-Tesla: {non['annual_kwh_per_vehicle']:,.0f} kWh/year"),
    ("Central peak", f"Tesla: {central['Tesla']:.1f} MW", f"Non-Tesla: {central['Non-Tesla BEVs']:.1f} MW"),
    ("Main result", "Tesla load is ~16% lower", "when behaviour is held constant"),
]

y = 0.58
for label, left, right in cards:
    ax.text(0.06, y, label, fontsize=14, fontweight="bold")
    ax.text(0.35, y, left, fontsize=14)
    ax.text(0.62, y, right, fontsize=14)
    y -= 0.13

ax.text(0.03, 0.06,
        "Interpretation: total grid load depends on fleet size and owner behaviour. "
        "This controlled model isolates vehicle-mix efficiency only.",
        fontsize=11)

save_current_fig("00_summary_infographic")

# 01 Annual GWh
fig, ax = plt.subplots(figsize=(9, 6))
ax.bar(annual["brand_group"], annual["sample_annual_gwh"])
ax.set_title("Like-for-like annual electricity demand", fontsize=16, pad=12)
ax.set_ylabel("GWh/year for 100,000 vehicles")
ax.set_xlabel("")
add_bar_labels(ax)
save_current_fig("01_annual_energy_comparison")

# 02 Per vehicle kWh
fig, ax = plt.subplots(figsize=(9, 6))
ax.bar(annual["brand_group"], annual["annual_kwh_per_vehicle"])
ax.set_title("Annual electricity demand per vehicle", fontsize=16, pad=12)
ax.set_ylabel("kWh/vehicle/year")
ax.set_xlabel("")
add_bar_labels(ax, fmt="{:,.0f}")
save_current_fig("02_per_vehicle_energy_comparison")

# 03 Peak load scenario comparison
fig, ax = plt.subplots(figsize=(11, 6))
peak_plot = peak.set_index("charging_profile")[["Tesla", "Non-Tesla BEVs"]]
peak_plot.plot(kind="bar", ax=ax)
ax.set_title("Peak-load under identical smart-grid conditions", fontsize=16, pad=12)
ax.set_ylabel("MW during weekday 4pm–10pm peak window")
ax.set_xlabel("")
ax.tick_params(axis="x", rotation=0)
add_bar_labels(ax)
save_current_fig("03_peak_load_scenario_comparison")

# 04 Extra peak load
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(peak["charging_profile"], peak["Non-Tesla minus Tesla MW"])
ax.set_title("Extra peak load from non-Tesla BEV sample", fontsize=16, pad=12)
ax.set_ylabel("Extra MW versus Tesla sample")
ax.set_xlabel("")
ax.tick_params(axis="x", rotation=0)
add_bar_labels(ax)
save_current_fig("04_extra_peak_load_non_tesla")

# 05 Percentage difference
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(peak["charging_profile"], peak["Tesla lower by %"])
ax.set_title("Tesla sample lower load under same conditions", fontsize=16, pad=12)
ax.set_ylabel("% lower than non-Tesla BEV sample")
ax.set_xlabel("")
ax.tick_params(axis="x", rotation=0)
add_bar_labels(ax)
save_current_fig("05_tesla_lower_load_percentage")

print(f"Updated datasets saved to: {DATA}")
print(f"Updated charts saved to: {OUT}")
