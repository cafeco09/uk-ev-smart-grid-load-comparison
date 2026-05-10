# Methodology

## Research question

Can we compare the load on the UK power/smart grid from Tesla BEVs versus non-Tesla BEVs under the same conditions?

## Controlled design

To make the comparison fair, the model fixes:

- Fleet size
- Annual mileage
- Charging window
- Smart-charging assumptions
- Peak-shifting assumptions

The only varying factor is weighted vehicle-mix efficiency.

## Sample

Each group is normalised to:

```text
100,000 vehicles
```

Annual mileage is fixed at:

```text
8,900 miles per vehicle per year
```

## Energy formula

```text
annual_kWh_per_vehicle = annual_miles × kWh_per_100_miles / 100
sample_annual_GWh = annual_kWh_per_vehicle × sample_vehicles / 1,000,000
```

## Peak-load formula

```text
daily_MWh = annual_GWh × 1000 / 365

net_peak_share =
  evening_peak_energy_share_before_shift
  × (1 - smart_charging_share × peak_shift_effectiveness)

peak_MW = daily_MWh × net_peak_share / peak_window_hours
```

## Charging profiles

| Profile | Interpretation |
|---|---|
| Smart/off-peak | Most flexible charging shifted away from peak |
| Central smart-grid proxy | Mixed charging behaviour |
| Unmanaged/high peak | More energy lands in the peak window |

## What this proves

It shows the effect of vehicle-mix efficiency under controlled charging assumptions.

## What this does not prove

It does not prove that real Tesla owners charge at better or worse times than non-Tesla owners. That would require private brand-level charging telemetry, which is not publicly available.
