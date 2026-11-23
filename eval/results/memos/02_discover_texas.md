# 02_discover_texas

**Request:** Where should we look for our next campus in Texas? We want industrial power under 7 cents.

**Tool calls (17):**
- `rank_counties({"state": "TX", "max_price_cents": 7, "top_n": 5})`
- `get_live_power_price({"state": "TX"})`
- `get_county_profile({"county_fips": "48141"})`
- `get_county_profile({"county_fips": "48157"})`
- `get_county_profile({"county_fips": "48039"})`
- `get_county_profile({"county_fips": "48167"})`
- `get_county_profile({"county_fips": "48303"})`
- `get_grid_queue({"county_fips": "48141"})`
- `get_grid_queue({"county_fips": "48157"})`
- `get_grid_queue({"county_fips": "48039"})`
- `get_grid_queue({"county_fips": "48167"})`
- `get_grid_queue({"county_fips": "48303"})`
- `get_known_sites({"county_fips": "48141"})`
- `get_known_sites({"county_fips": "48157"})`
- `get_known_sites({"county_fips": "48039"})`
- `get_known_sites({"county_fips": "48167"})`
- `get_known_sites({"county_fips": "48303"})`

---

## Recommendation
Advance **Lubbock** and **Galveston** to on-the-ground diligence. Both are under 7¢, have no known data center competitors, and have moderate queues. Keep **El Paso** as a benchmark market, since Meta is building 1,000 MW there. Treat **Brazoria** as the weakest option because its interconnection queue is heavy.

## Comparison
| County | Model score (percentile) | Power ¢/kWh | Population | Data centers (existing / planned) | Grid queue MW |
|---|---|---|---|---|---|
| El Paso | 0.93 (98.0) | 4.90 | 877,858 | 0 / 1 (1,000 MW, under construction) | 1,697 |
| Fort Bend | 0.93 (97.7) | 6.12* | 975,191 | 0 / 0 | 3,604 |
| Brazoria | 0.85 (93.6) | 6.04 | 419,080 | 0 / 1 (300 MW, proposed) | 13,316 |
| Galveston | 0.83 (92.5) | 5.87 | 372,207 | 0 / 0 | 3,112 |
| Lubbock | 0.83 (92.3) | 6.04 | 328,906 | 0 / 0 | 992 |

*Fort Bend's price is the state average, not a county figure.

**Power prices are the 2024 EIA-861 fallback, not live EIA data.** Live data was unavailable. The Texas statewide figure is 6.49¢.

The model score reflects where developers have built before. It doesn't show that a county is suitable.

## County notes
**El Paso**
- Cheapest power at 4.90¢. Its grid region is West, with El Paso Electric as the utility, so it is not in ERCOT.
- Meta's 1,000 MW campus is under construction, so expect competition for power and labor. The median time from queue request to operation is 2.87 years.
- Water stress is 3.01 of 5 (Texas state average). Summer max temperature is 97.1°F.

**Fort Bend**
- Population growth since 2020 is 18.35%. Farmland is $4,398/acre, a proxy for land cost.
- The power price is a state-average proxy, so confirm the real tariff. The queue is 3,604 MW (17 projects, mostly batteries), and the median time to online is 3.52 years.

**Brazoria**
- Land is available and there is a 300 MW CleanSpark proposal. Farmland is $5,440/acre.
- The queue is the heaviest in the set: 13,316 MW across 64 projects. The oldest request dates from 2017, and the median time to online is 4.4 years.

**Galveston**
- Power is 5.87¢, and there are no known data centers.
- Farmland is $15,245/acre, so land is likely the costliest of the five. The county has only 983 km² of land. The queue is 3,112 MW, and the median time to online is 3.8 years.

**Lubbock**
- Lowest queue (992 MW, 7 projects) and lowest cooling degree days (1,825). Farmland is $2,673/acre, which suggests cheap land.
- The median time to online is 4.65 years, the longest of the five.
- The data conflicts on grid region. The profile says SPP, and the queue tool says ERCOT but lists SPS as the utility. Resolve this first, because it affects pricing and interconnection.

## Risks and unknowns
- The data has no parcel availability, substation or transmission capacity, or large-load interconnection timelines. The queue figures show generation and battery congestion, not available capacity.
- It also has no permitting, zoning, local opposition, or water rights data. Water stress is a state-level score.
- Public atlases miss some facilities. "No known data centers" is not proof there are none.
- The prices are 2024 figures. They aren't contract rates.

## Next diligence steps
1. Confirm Lubbock's grid region and utility (SPS or Lubbock Power & Light, versus ERCOT).
2. Request large-load interconnection studies and the timeline for 100+ MW from each utility.
3. Check Fort Bend's actual tariff and the utility serving it.
4. Screen parcels of 200+ acres near high-voltage substations in Lubbock and Galveston.
5. Check Meta's El Paso load against local capacity.
6. Review water sourcing and local permitting climate in each county.

## Sources
Project 1 county dataset (EIA-861, LBNL Queued Up through 2025, NOAA, USDA, WRI, Census, IM3, Compute Atlas). IM3 Data Center Atlas and Compute Atlas for sites. The EIA-861 2024 fallback for power price.
