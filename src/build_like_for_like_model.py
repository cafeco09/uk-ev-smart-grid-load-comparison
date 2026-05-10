from pathlib import Path
import pandas as pd

OUTPUT = Path("data/processed")
OUTPUT.mkdir(parents=True, exist_ok=True)

SAMPLE_VEHICLES = 100_000
ANNUAL_MILES = 8_900

# Weighted efficiency values from the UK real-fleet model mix.
# Tesla and non-Tesla use the same sample size and mileage.
data = [
    {
        "brand_group": "Tesla",
        "sample_vehicles": SAMPLE_VEHICLES,
        "annual_miles_per_vehicle": ANNUAL_MILES,
        "weighted_kwh_per_100_miles": 26.7748,
    },
    {
        "brand_group": "Non-Tesla BEVs",
        "sample_vehicles": SAMPLE_VEHICLES,
        "annual_miles_per_vehicle": ANNUAL_MILES,
        "weighted_kwh_per_100_miles": 31.8751,
    },
]

base = pd.DataFrame(data)
base["annual_kwh_per_vehicle"] = (
    base["annual_miles_per_vehicle"] * base["weighted_kwh_per_100_miles"] / 100
)
base["sample_annual_gwh"] = (
    base["annual_kwh_per_vehicle"] * base["sample_vehicles"] / 1_000_000
)
base["sample_daily_mwh"] = base["sample_annual_gwh"] * 1000 / 365
base["avg_continuous_mw"] = base["sample_annual_gwh"] * 1000 / 8760

profiles = pd.DataFrame([
    {
        "charging_profile": "Smart/off-peak",
        "evening_peak_energy_share_before_shift": 0.20,
        "smart_charging_share": 0.60,
        "peak_shift_effectiveness": 0.70,
    },
    {
        "charging_profile": "Central smart-grid proxy",
        "evening_peak_energy_share_before_shift": 0.35,
        "smart_charging_share": 0.40,
        "peak_shift_effectiveness": 0.60,
    },
    {
        "charging_profile": "Unmanaged/high peak",
        "evening_peak_energy_share_before_shift": 0.50,
        "smart_charging_share": 0.20,
        "peak_shift_effectiveness": 0.30,
    },
])

PEAK_WINDOW_HOURS = 6
rows = []

for _, b in base.iterrows():
    for _, p in profiles.iterrows():
        net_peak_share = p["evening_peak_energy_share_before_shift"] * (
            1 - p["smart_charging_share"] * p["peak_shift_effectiveness"]
        )
        peak_mw = b["sample_daily_mwh"] * net_peak_share / PEAK_WINDOW_HOURS
        rows.append({
            "brand_group": b["brand_group"],
            "sample_vehicles": SAMPLE_VEHICLES,
            "charging_profile": p["charging_profile"],
            "peak_window": "Weekday 4pm-10pm",
            "estimated_peak_load_mw": peak_mw,
        })

scenarios = pd.DataFrame(rows)
peak_summary = scenarios.pivot(
    index="charging_profile",
    columns="brand_group",
    values="estimated_peak_load_mw"
).reset_index()

peak_summary["Non-Tesla minus Tesla MW"] = (
    peak_summary["Non-Tesla BEVs"] - peak_summary["Tesla"]
)
peak_summary["Tesla lower by %"] = (
    1 - peak_summary["Tesla"] / peak_summary["Non-Tesla BEVs"]
) * 100

base.to_csv(OUTPUT / "like_for_like_sample_base_energy.csv", index=False)
scenarios.to_csv(OUTPUT / "like_for_like_smart_grid_peak_scenarios.csv", index=False)
peak_summary.to_csv(OUTPUT / "like_for_like_peak_comparison_summary.csv", index=False)

print(base.round(3).to_string(index=False))
print()
print(peak_summary.round(3).to_string(index=False))
