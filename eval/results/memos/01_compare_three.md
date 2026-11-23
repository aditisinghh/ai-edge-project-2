# 01_compare_three

**Request:** Compare Loudoun VA, El Paso TX and Grant WA for a 100 MW AI campus. Which should go to diligence first?

**Tool calls (15):**
- `find_county({"name": "Loudoun", "state": "VA"})`
- `find_county({"name": "El Paso", "state": "TX"})`
- `find_county({"name": "Grant", "state": "WA"})`
- `get_county_profile({"county_fips": "51107"})`
- `get_county_profile({"county_fips": "48141"})`
- `get_county_profile({"county_fips": "53025"})`
- `get_grid_queue({"county_fips": "51107"})`
- `get_grid_queue({"county_fips": "48141"})`
- `get_grid_queue({"county_fips": "53025"})`
- `get_known_sites({"county_fips": "51107"})`
- `get_known_sites({"county_fips": "48141"})`
- `get_known_sites({"county_fips": "53025"})`
- `get_live_power_price({"state": "VA"})`
- `get_live_power_price({"state": "TX"})`
- `get_live_power_price({"state": "WA"})`

---

## Recommendation
Take **El Paso, TX** to on-the-ground diligence first. It has the highest model score, the lowest power price and the shortest reported time to online. Run **Grant, WA** in parallel as the close alternative, because its cooling and water profile is better. Deprioritize **Loudoun, VA** for a 100 MW campus: it has the highest power price, the longest queue timeline and a saturated market.

## Comparison
| County | Model score (percentile) | Power ¢/kWh | Population | Data centers (existing / planned) | Grid queue MW |
|---|---|---|---|---|---|
| El Paso, TX | 0.93 (98.0) | 4.90 | 877,858 | 0 / 1 site, 1,000 MW | 1,697 (11 projects) |
| Grant, WA | 0.80 (91.4) | 5.11 | 105,727 | 38 sites, 335 MW / none | 4,550 (19 projects) |
| Loudoun, VA | 0.85 (93.5) | 7.81 | 449,749 | 199 sites, 1,120 MW / 10 sites, 858 MW | 715 (5 projects) |

The model score reflects where developers have built before. It does not certify suitability.

Power prices are the county-level 2024 EIA-861 figures. Live EIA data was unavailable, so the state-level 2024 fallbacks are VA 8.32, TX 6.49 and WA 7.35 ¢/kWh.

## County notes
**El Paso, TX**
- Strengths:
  - It has the lowest power price of the three.
  - Farmland is $2,912/acre, the cheapest of the three.
  - Reported time to online is 2.87 years.
- Red flags:
  - Meta's 1,000 MW campus is under construction. It may absorb El Paso Electric's capacity, and it makes El Paso a competitor for power and labor.
  - It is the hottest of the three: summer max 97.1°F and 2,413 cooling degree days.
  - State water stress is 3.01 of 5.
  - The queue is 1,697 MW, and El Paso Electric is the only utility listed. The oldest request is from 2022.

**Grant, WA**
- Strengths:
  - Power is 5.11 ¢/kWh, and 75% of supply is public power.
  - Cooling need is low, with 653 cooling degree days.
  - State water stress is 0.56 of 5.
  - It has an established cluster, including Sabey's Quincy campus.
  - Land is $5,216/acre.
- Red flags:
  - The queue is 4,550 MW across 19 projects, the oldest from 2017. None have connected and the completion rate is 0.
  - Grant County PUD is the main utility, so large-load availability depends on it.
  - Reported time to online is 2.87 years.

**Loudoun, VA**
- Strengths:
  - It has the deepest ecosystem and workforce, and the smallest queue (715 MW).
- Red flags:
  - Power is the most expensive, at 7.81 ¢/kWh.
  - Median time to online is 4.44 years, and the queue completion rate is 25%.
  - Land is $12,276/acre.
  - Heavy competition: STACK has a permitted 144 MW campus, JK Land has a permitted 300 MW site, and AWS has proposed sites.

## Risks and unknowns
- The data does not show land parcels, substation or transmission capacity, or the utility's ability to serve 100 MW.
- Queue figures are generation and battery requests. They indicate congestion, not available load capacity.
- Site counts differ between sources. The profile shows 199 existing sites in Loudoun and 38 in Grant. The atlas lists 235 operational sites in Loudoun and 48 in Grant. Loudoun's planned MW is 858 in the profile and 498 in the atlas. Public atlases also miss some facilities.
- The data does not cover permitting, local opposition, water rights or tax incentives.

## Next diligence steps
1. Ask El Paso Electric for a load-interconnection study and timeline for 100 MW. Ask how Meta's 1,000 MW affects capacity.
2. Ask Grant County PUD about large-load availability, its queue policy and the energization timeline.
3. In El Paso, assess water supply and options for air-cooled or low-water cooling.
4. In both counties, screen parcels near existing substations and fiber routes.
5. Confirm current industrial tariffs directly with the utilities, since the live EIA feed was unavailable.
6. Keep Loudoun only if the project needs proximity to the Northern Virginia network.

## Sources
- Project 1 county dataset (EIA-861, LBNL, NOAA, USDA, WRI, Census, IM3, Compute Atlas)
- LBNL Queued Up (through 2025)
- IM3 Data Center Atlas and Compute Atlas
- EIA-861 2024 state fallback prices
