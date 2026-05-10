# Tesla vs Non-Tesla BEVs: Like-for-like UK smart-grid load

This repo compares **Tesla BEVs** and **non-Tesla BEVs** under identical smart-grid conditions.

The purpose is to remove the misleading effect of total fleet size and ask:

> If both groups had the same number of vehicles, same mileage and same charging behaviour, which vehicle mix would place more load on the power grid?

## Main result

Controlled sample:

- 100,000 Tesla BEVs
- 100,000 non-Tesla BEVs
- 8,900 miles per vehicle per year
- Same weekday 4pm–10pm peak window
- Same smart-charging profiles
- Same peak-shifting behaviour

Only the **vehicle-mix efficiency** differs.

| Group | Weighted efficiency | Annual kWh/vehicle | Annual GWh for 100k vehicles |
|---|---:|---:|---:|
| Tesla | 26.8 kWh/100 miles | 2,383 | 238.3 |
| Non-Tesla BEVs | 31.9 kWh/100 miles | 2,837 | 283.7 |

## Smart-grid peak comparison

| Charging profile | Tesla MW | Non-Tesla MW | Extra non-Tesla MW | Tesla lower by |
|---|---:|---:|---:|---:|
| Smart/off-peak | 12.6 | 15.0 | 2.4 | 16.0% |
| Central smart-grid proxy | 28.9 | 34.5 | 5.5 | 16.0% |
| Unmanaged/high peak | 51.1 | 60.9 | 9.7 | 16.0% |

## Interpretation

Under identical owner behaviour and smart-grid assumptions, the non-Tesla BEV sample draws around **16% more power** than the Tesla sample.

This does **not** prove Tesla owners charge at better times. It isolates the vehicle-mix efficiency effect.

## Folder structure

```text
tesla_vs_non_tesla_smart_grid_repo/
├── README.md
├── requirements.txt
├── data/
│   └── processed/
├── docs/
│   ├── METHODOLOGY.md
│   └── SOURCES_AND_LIMITATIONS.md
├── outputs/
│   ├── infographics/
│   └── tables/
└── src/
    ├── build_like_for_like_model.py
    └── make_infographics.py
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/build_like_for_like_model.py
python src/make_infographics.py
```

## Infographics

The infographic outputs are saved in:

```text
outputs/infographics/
```
