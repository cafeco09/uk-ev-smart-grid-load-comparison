# Tesla vs Non-Tesla BEVs: Like-for-like UK smart-grid load

This repository contains a controlled UK smart-grid simulation comparing **Tesla BEVs** and **non-Tesla BEVs** under identical conditions.

The purpose is to remove the misleading effect of total fleet size and ask:

> If both groups had the same number of vehicles, same mileage and same charging behaviour, which vehicle mix would place more load on the power grid?

This is **not an endorsement of Tesla**. The research question is about whether efficient engineering can reduce annual energy demand and peak-period grid pressure when EVs scale.

---

## Project summary

Controlled sample:

- 100,000 Tesla BEVs
- 100,000 non-Tesla BEVs
- 8,900 miles per vehicle per year
- Same weekday 4pm–10pm peak window
- Same charging behaviour
- Same smart-charging profiles and peak-shifting assumptions

Only the **weighted vehicle-mix efficiency** differs.

---

## Main result

| Group | Weighted efficiency | Annual kWh/vehicle | Annual GWh for 100k vehicles |
|---|---:|---:|---:|
| Tesla | 26.8 kWh/100 miles | 2,383 | 238.3 |
| Non-Tesla BEVs | 31.9 kWh/100 miles | 2,837 | 283.7 |

Under identical owner behaviour and smart-grid assumptions, the non-Tesla BEV sample draws around **16% more power** than the Tesla sample.

This does **not** prove Tesla owners charge at better times. It isolates the vehicle-mix efficiency effect.

---

## Smart-grid peak comparison

| Charging profile | Tesla MW | Non-Tesla MW | Extra non-Tesla MW | Tesla lower by |
|---|---:|---:|---:|---:|
| Smart/off-peak | 12.6 | 15.0 | 2.4 | 16.0% |
| Central smart-grid proxy | 28.9 | 34.5 | 5.5 | 16.0% |
| Unmanaged/high peak | 51.1 | 60.9 | 9.7 | 16.0% |

---

## Actual public data sources

The processed dataset in this repository is derived from public vehicle and charging-policy sources, combined with transparent modelling assumptions.

| Input | Source | Website | How it was used |
|---|---|---|---|
| UK BEV make/model fleet structure | Department for Transport / DVLA vehicle licensing data files | https://www.gov.uk/government/statistical-data-sets/vehicle-licensing-statistics-data-files | Used the make/model vehicle structure from `df_VEH0120_UK`, which provides vehicles by licence status, body type, make, generic model, model, fuel and quarter. |
| UK vehicle licensing context | GOV.UK vehicle licensing statistics tables | https://www.gov.uk/government/statistical-data-sets/vehicle-licensing-statistics-data-tables | Used as the official vehicle licensing statistics context and cross-reference for UK registered/licensed vehicles. |
| Annual BEV mileage assumption | RAC Foundation motoring FAQs, based on DfT National Travel Survey table NTS0901 | https://www.racfoundation.org/motoring-faqs/mobility | Used the public BEV average annual mileage assumption of 8,900 miles/year. |
| UK smart charging policy context | GOV.UK smart charge point regulations guidance | https://www.gov.uk/guidance/regulations-electric-vehicle-smart-charge-points | Used to justify modelling smart charging as a grid-management mechanism. |
| UK smart charge point legislation | The Electric Vehicles (Smart Charge Points) Regulations 2021 | https://www.legislation.gov.uk/ukdsi/2021/9780348228434 | Used for the weekday peak-period framing and smart-charge-point regulatory context. |
| EV weighted efficiency fallback | HMRC Advisory Fuel Rates | https://www.gov.uk/guidance/advisory-fuel-rates | Used as a public benchmark for EV weighted efficiency where needed. HMRC lists weighted electric-car efficiency in miles/kWh in its advisory electric-rate calculation. |
| Model-specific efficiency layer | Processed model assumptions in this repository | [`data/processed/05_model_assumptions.csv`](data/processed/05_model_assumptions.csv) | Weighted Tesla and non-Tesla kWh/100-mile values were used in the controlled comparison. These are modelled/processed values, not private charging telemetry. |

---

## Dataset in this repo

The actual processed dataset behind the charts is included in this repository.

| Dataset | Link |
|---|---|
| Data dictionary | [`data/processed/00_data_dictionary.csv`](data/processed/00_data_dictionary.csv) |
| Annual energy comparison | [`data/processed/01_like_for_like_annual_energy.csv`](data/processed/01_like_for_like_annual_energy.csv) |
| Peak-load scenarios | [`data/processed/02_like_for_like_peak_load_scenarios.csv`](data/processed/02_like_for_like_peak_load_scenarios.csv) |
| Annual energy long form | [`data/processed/03_annual_energy_long_form.csv`](data/processed/03_annual_energy_long_form.csv) |
| Peak-load long form | [`data/processed/04_peak_load_long_form.csv`](data/processed/04_peak_load_long_form.csv) |
| Model assumptions | [`data/processed/05_model_assumptions.csv`](data/processed/05_model_assumptions.csv) |

---

## Final charts

The final chart outputs are stored in:

[`outputs/infographics/`](outputs/infographics/)

![Summary infographic](outputs/infographics/00_summary_infographic.png)

Additional chart outputs:

| Chart | Link |
|---|---|
| Annual energy comparison | [`outputs/infographics/01_annual_energy_comparison.png`](outputs/infographics/01_annual_energy_comparison.png) |
| Per-vehicle energy comparison | [`outputs/infographics/02_per_vehicle_energy_comparison.png`](outputs/infographics/02_per_vehicle_energy_comparison.png) |
| Peak-load scenario comparison | [`outputs/infographics/03_peak_load_scenario_comparison.png`](outputs/infographics/03_peak_load_scenario_comparison.png) |
| Extra peak load from non-Tesla sample | [`outputs/infographics/04_extra_peak_load_non_tesla.png`](outputs/infographics/04_extra_peak_load_non_tesla.png) |
| Tesla lower-load percentage | [`outputs/infographics/05_tesla_lower_load_percentage.png`](outputs/infographics/05_tesla_lower_load_percentage.png) |

---

## Methodology

The model uses a controlled like-for-like sample.

Instead of comparing the real total Tesla fleet with the real total non-Tesla fleet, it normalises both groups to the same sample size:

```text
100,000 vehicles each
