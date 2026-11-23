# 03_two_candidates

**Request:** We're choosing between Fort Bend County, Texas and DeKalb County, Georgia. Which one first, and why?

**Tool calls (10):**
- `find_county({"name": "Fort Bend", "state": "Texas"})`
- `find_county({"name": "DeKalb", "state": "Georgia"})`
- `get_live_power_price({"state": "Texas"})`
- `get_live_power_price({"state": "Georgia"})`
- `get_county_profile({"county_fips": "48157"})`
- `get_grid_queue({"county_fips": "48157"})`
- `get_known_sites({"county_fips": "48157"})`
- `get_county_profile({"county_fips": "13089"})`
- `get_grid_queue({"county_fips": "13089"})`
- `get_known_sites({"county_fips": "13089"})`

---

## Recommendation
**Advance Fort Bend County, TX first.** It has the higher model score (97.7th vs 96.4th percentile) and lower power prices (6.12 vs 7.09 ¢/kWh). Its land is far cheaper (farmland proxy $4,398 vs $99,639 per acre). DeKalb is a reasonable second, but its land cost and price are worse. Neither county has a known data center, so neither has a competitor to benchmark against.

## Comparison
| County | Model score (percentile) | Power ¢/kWh | Population | Data centers (existing / planned) | Grid queue MW |
|---|---|---|---|---|---|
| Fort Bend, TX | 0.926 (97.7; national rank 72, state rank 9) | 6.12* | 975,191 | 0 / 0 | 3,604 (17 projects) |
| DeKalb, GA | 0.906 (96.4; national rank 112, state rank 3) | 7.09 | 774,394 | 0 / 0 | 0 |

*The profile flags Fort Bend's price as a state average, not a county-specific figure.

The model score reflects where developers have built before. It doesn't show that a site is suitable.

## County notes
**Fort Bend, TX (ERCOT)**
- Strengths: lower power price. Population grew 18.35% since 2020. Land is cheap by the farmland proxy. Public power share is 0.84.
- Red flags: the 3,604 MW queue is 2,652.6 MW battery and 951.4 MW solar, and the oldest request dates from 2019. The queue signals grid congestion, not available capacity. Median time from request to operation is 3.52 years, and the queue completion rate is 0.5. Cooling load is heavier (3,252 cooling degree days, 94.2°F summer max). State water stress is 3.01 of 5.

**DeKalb, GA (Southeast)**
- Strengths: no active interconnection requests. Cooling load is lighter (1,718 cooling degree days, 89.1°F summer max). State water stress is lower (1.92). Population density is high (1,117 per km²).
- Red flags: land is expensive (about $99.6k per acre, farmland proxy). Power costs more. Population growth since 2020 is only 1.3%. Land area is small (693 km² vs 2,233). Median time to online is 4.15 years, and that figure comes from regional data. Three utilities serve the county, so utility selection is a diligence item.

## Risks and unknowns
- The data has no parcel availability, zoning, substation or transmission capacity, or large-load interconnection timelines.
- It also has nothing on water rights, local opposition, or permitting.
- Fort Bend's price is a state average. DeKalb's is county-level.
- The queue data covers generation and batteries, not load.
- Farmland value is only a rough proxy for land cost.

## Next diligence steps
1. Ask CenterPoint, or whichever utility serves Fort Bend, for large-load interconnection timelines and substation headroom. Do the same with the DeKalb utilities.
2. Screen for parcels of 100+ acres near transmission in both counties. DeKalb's small, dense footprint may limit this.
3. Check the local zoning and permitting climate, and any moratorium or opposition history.
4. Get a water-supply and cooling-strategy review for Fort Bend.
5. Get county-level tariff quotes to replace the state-average price.

## Sources
- **Power prices:** the 2024 EIA-861 fallback. Live EIA data was unavailable, so these are not live prices. The state figures are 6.49 ¢/kWh for TX and 7.17 for GA. The comparison table uses the county-profile prices instead.
- **Other data:** Project 1 county dataset (EIA-861, LBNL, NOAA, USDA, WRI, Census, IM3, Compute Atlas), LBNL Queued Up (through 2025), and the IM3 and Compute Atlas data center atlases.
