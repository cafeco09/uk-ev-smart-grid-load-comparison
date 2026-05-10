from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA = Path("data/processed")
OUT = Path("outputs/infographics")
OUT.mkdir(parents=True, exist_ok=True)

base = pd.read_csv(DATA / "like_for_like_sample_base_energy.csv")
peak = pd.read_csv(DATA / "like_for_like_peak_comparison_summary.csv")

def save_bar(df, x, y, title, ylabel, filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df[x], df[y])
    ax.set_title(title, fontsize=16, pad=12)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=0)
    for i, v in enumerate(df[y]):
        ax.text(i, v, f"{v:,.1f}", ha="center", va="bottom", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=220)
    plt.close(fig)

save_bar(
    base,
    "brand_group",
    "sample_annual_gwh",
    "Like-for-like annual electricity demand",
    "GWh/year for 100,000 vehicles",
    "01_annual_gwh_same_100k_vehicles.png",
)

save_bar(
    base,
    "brand_group",
    "annual_kwh_per_vehicle",
    "Annual electricity demand per vehicle",
    "kWh/vehicle/year",
    "02_annual_kwh_per_vehicle.png",
)

fig, ax = plt.subplots(figsize=(11, 6))
plot_df = peak.set_index("charging_profile")[["Tesla", "Non-Tesla BEVs"]]
plot_df.plot(kind="bar", ax=ax)
ax.set_title("Peak-load under identical smart-grid conditions", fontsize=16, pad=12)
ax.set_ylabel("MW during weekday 4pm-10pm peak window")
ax.set_xlabel("")
ax.tick_params(axis="x", rotation=0)
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "03_peak_mw_same_conditions.png", dpi=220)
plt.close(fig)

save_bar(
    peak,
    "charging_profile",
    "Non-Tesla minus Tesla MW",
    "Extra peak load from non-Tesla BEV sample",
    "Extra MW versus Tesla sample",
    "04_extra_peak_mw_non_tesla_minus_tesla.png",
)

save_bar(
    peak,
    "charging_profile",
    "Tesla lower by %",
    "Tesla sample lower load under same conditions",
    "% lower than non-Tesla BEV sample",
    "05_tesla_lower_load_percentage.png",
)

print(f"Saved infographics to {OUT}")
