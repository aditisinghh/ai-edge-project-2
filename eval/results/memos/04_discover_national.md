# 04_discover_national

**Request:** Give me five counties anywhere in the US with no data center yet that look most like proven sites, and at least 200,000 people.

**Tool calls (19):**
- `rank_counties({"top_n": 5, "min_population": 200000, "exclude_existing": true, "sort_by": "model_score"})`
- `get_county_profile({"county_fips": "53011"})`
- `get_county_profile({"county_fips": "04019"})`
- `get_county_profile({"county_fips": "36081"})`
- `get_county_profile({"county_fips": "53035"})`
- `get_county_profile({"county_fips": "04021"})`
- `get_grid_queue({"county_fips": "53011"})`
- `get_grid_queue({"county_fips": "04019"})`
- `get_grid_queue({"county_fips": "36081"})`
- `get_grid_queue({"county_fips": "53035"})`
- `get_grid_queue({"county_fips": "04021"})`
- `get_known_sites({"county_fips": "53011"})`
- `get_known_sites({"county_fips": "04019"})`
- `get_known_sites({"county_fips": "36081"})`
- `get_known_sites({"county_fips": "53035"})`
- `get_known_sites({"county_fips": "04021"})`
- `get_live_power_price({"state": "WA"})`
- `get_live_power_price({"state": "AZ"})`
- `get_live_power_price({"state": "NY"})`

---

## Recommendation
Advance **Clark, WA** and **Pinal, AZ** to on-the-ground diligence. Clark has low power cost and mild climate, with no known data center competition. Pinal has the most proven developer interest. Keep **Pima, AZ** and **Kitsap, WA** as second tier. Deprioritize **Queens, NY**, where power costs 29.76¢/kWh. The model score reflects where developers have built before, not certainty of suitability.

## Comparison
| County | Model score (percentile) | Power ¢/kWh | Population | Data centers (existing / planned) | Grid queue MW |
|---|---|---|---|---|---|
| Clark, WA | 0.982 (99.7) | 6.04 | 532,119 | 0 / 0 | 308 |
| Pima, AZ | 0.977 (99.7) | 10.01 | 1,074,685 | 0 / 3 (2,100 MW) | 4,875 |
| Queens, NY | 0.971 (99.5) | 29.76 | 2,358,182 | 0 / 0 | 331 |
| Kitsap, WA | 0.969 (99.4) | 9.02 | 283,374 | 0 / 0 | 585 |
| Pinal, AZ | 0.960 (99.2) | 7.72 | 539,380 | 0 / 6 (1,520 MW) | 10,581 |

Power prices are 2024 EIA-861 county figures. Live EIA data was unavailable and the state lookups returned the 2024 fallback.

## County notes
**Clark, WA**
- Strengths: cheapest power of the five, summer max temp 79.1°F, 5.7% population growth since 2020, 100% public power, and no known data center competition.
- Red flags: the queue completion rate is 0.2 and the median time to online is 2.87 years. The queue includes a 286 MW gas project.

**Pima, AZ**
- Strengths: farmland is $504/acre and the pipeline shows developer interest. That includes Project Blue (600 MW, under construction) and Luckett Road (1,500 MW, proposed).
- Red flags: Project Blue is already under construction, so "no data center yet" may not hold for long. Water stress is 3.75 of 5 (state average). Summer max temp is 100.4°F. The queue is 4,875 MW with a 0.042 completion rate.

**Queens, NY**
- Strengths: large workforce and population density.
- Red flags: power is 29.76¢/kWh, farmland is $113,746/acre, and the median time to online is 4.96 years. Population fell 1.96% since 2020. Its score comes from metro proxies, so I don't see a practical hyperscale site here.

**Kitsap, WA**
- Strengths: cool climate (75.8°F summer max, 112 cooling degree days) and 75% public power.
- Red flags: power is 9.02¢/kWh and farmland is $50,663/acre. The 585 MW queue has a 0.0 completion rate.

**Pinal, AZ**
- Strengths: power is 7.72¢/kWh, population grew 26.6% since 2020, and 89% is public power. Operators include EdgeCore (720 MW, permitted) and Ryan Companies (permitted and proposed).
- Red flags: the queue is the largest at 10,581 MW across 46 projects, with a 3.34-year median to online. Water stress is 3.75 of 5 (state average) and summer max temp is 101.6°F. Several competitors are ahead of us, and one project (La Osa) was cancelled.

## Risks and unknowns
- The data doesn't cover parcels, substation or transmission capacity, or large-load interconnection timelines. The queue shows generator congestion, not available capacity.
- It also doesn't cover permitting, local opposition, or water rights. Water scores are state averages, not county figures.
- Public atlases miss some facilities, so "no data center" is not confirmed.

## Next diligence steps
1. Ask Clark Public Utilities (the county's public power provider) about large-load availability and timelines. I'm inferring the provider from the 100% public power share, so confirm it.
2. Ask the Pinal utilities (APS, SRP, TEP, WAPA) about large-load capacity, and review the permitted EdgeCore and Ryan sites for competing demand.
3. Screen parcels and zoning in Clark and Pinal.
4. Check water sourcing and rights in Pinal and Pima.
5. Confirm Project Blue's status and neighboring load in Pima.
6. Test local sentiment and moratorium risk in all shortlisted counties.

## Sources
Project 1 county dataset (EIA-861, LBNL, NOAA, USDA, WRI, Census, IM3, Compute Atlas); LBNL Queued Up (through 2025); IM3 Data Center Atlas and Compute Atlas; EIA-861 2024 fallback for state prices.
