# 14_eight_counties

**Request:** Screen these for a 200 MW campus: Loudoun VA, Prince William VA, Maricopa AZ, Pinal AZ, Dallas TX, El Paso TX, Grant WA, Douglas WA.

**Tool calls (36):**
- `find_county({"name": "Loudoun", "state": "VA"})`
- `find_county({"name": "Prince William", "state": "VA"})`
- `find_county({"name": "Maricopa", "state": "AZ"})`
- `find_county({"name": "Pinal", "state": "AZ"})`
- `find_county({"name": "Dallas", "state": "TX"})`
- `find_county({"name": "El Paso", "state": "TX"})`
- `find_county({"name": "Grant", "state": "WA"})`
- `find_county({"name": "Douglas", "state": "WA"})`
- `get_live_power_price({"state": "VA"})`
- `get_live_power_price({"state": "AZ"})`
- `get_live_power_price({"state": "TX"})`
- `get_live_power_price({"state": "WA"})`
- `get_county_profile({"county_fips": "51107"})`
- `get_county_profile({"county_fips": "51153"})`
- `get_county_profile({"county_fips": "04013"})`
- `get_county_profile({"county_fips": "04021"})`
- `get_county_profile({"county_fips": "48113"})`
- `get_county_profile({"county_fips": "48141"})`
- `get_county_profile({"county_fips": "53025"})`
- `get_county_profile({"county_fips": "53017"})`
- `get_grid_queue({"county_fips": "51107"})`
- `get_grid_queue({"county_fips": "51153"})`
- `get_grid_queue({"county_fips": "04013"})`
- `get_grid_queue({"county_fips": "04021"})`
- `get_grid_queue({"county_fips": "48113"})`
- `get_grid_queue({"county_fips": "48141"})`
- `get_grid_queue({"county_fips": "53025"})`
- `get_grid_queue({"county_fips": "53017"})`
- `get_known_sites({"county_fips": "51107"})`
- `get_known_sites({"county_fips": "51153"})`
- `get_known_sites({"county_fips": "04013"})`
- `get_known_sites({"county_fips": "04021"})`
- `get_known_sites({"county_fips": "48113"})`
- `get_known_sites({"county_fips": "48141"})`
- `get_known_sites({"county_fips": "53025"})`
- `get_known_sites({"county_fips": "53017"})`

---

## Recommendation
Advance **Pinal AZ**, **Dallas TX** and **Grant WA** to on-the-ground diligence. Keep **El Paso TX** as an alternate. Pinal offers the best mix of score, land cost and time to power. Dallas has the shortest interconnection timeline. Grant has low power cost, cool climate and low water stress. Deprioritize Loudoun, Prince William and Maricopa, where median time to online is long and competition is heavy. Douglas has the cheapest power, but it is small and has the lowest score.

## Comparison
| County | Model score (percentile) | Power ¢/kWh | Population | Data centers (existing / planned) | Grid queue MW |
|---|---|---|---|---|---|
| Loudoun VA | 0.85 (93.5) | 7.81 | 449,749 | 199 / 10 | 715 |
| Prince William VA | 0.92 (97.5) | 7.81 | 502,966 | 58 / 4 | 670 |
| Maricopa AZ | 0.997 (100) | 7.57 | 4,689,558 | 54 / 20 | 29,032 |
| Pinal AZ | 0.96 (99.2) | 7.72 | 539,380 | 0 / 6 | 10,581 |
| Dallas TX | 0.97 (99.6) | 6.58 | 2,661,397 | 15 / 5 | 1,472 |
| El Paso TX | 0.93 (98.0) | 4.90 | 877,858 | 0 / 1 | 1,697 |
| Grant WA | 0.80 (91.4) | 5.11 | 105,727 | 38 / 0 | 4,550 |
| Douglas WA | 0.71 (85.8) | 3.86 | 46,473 | 13 / 2 | 5,020 |

Power prices are the **2024 EIA-861 county figures**. Live EIA data was unavailable, so the state tool returned the 2024 fallback (VA 8.32, AZ 9.90, TX 6.49, WA 7.35). The model score reflects where developers have built before, not suitability.

## County notes
- **Pinal:** No existing data centers and 1,520 MW planned, including EdgeCore's 720 MW permitted campus. Farmland is $2,148/acre and median time to online is 3.34 years. Red flags: the 10,581 MW queue, state water stress of 3.75, and one cancelled site.
- **Dallas:** The shortest time to online of the eight (1.45 years) and a 44% queue completion rate, in ERCOT. Red flags: land at $8,455/acre and dense, with STACK's 500 MW campus under construction. The atlas lists 745 planned MW, against 2,545 MW in the profile.
- **Grant:** 5.11¢, with 653 cooling degree days and state water stress of 0.56. The local utility is Grant PUD. Red flags: 4,550 MW queued, none connected, and a mature market with 335 MW existing.
- **El Paso:** The lowest price among the large metros (4.90¢) and $2,912/acre land. Red flag: Meta's 1,000 MW campus is under construction and may absorb El Paso Electric capacity.
- **Douglas:** The cheapest power (3.86¢), with public power and a cool climate. Red flags: the lowest score, a population of only 46,473, and 13 MW planned. The queue lists Puget Sound Energy, although the profile shows 100% public power, so verify the serving utility.
- **Loudoun / Prince William:** Dominion territory with 4.44 years median to online. Loudoun has 1,120 existing MW and 858 MW in the pipeline. Prince William has 682 MW in the pipeline. Both are crowded and have high land cost (about $12.3k/acre).
- **Maricopa:** The top-ranked county nationally, but median time to online is 6.58 years. It has 5,490 MW planned, a 29,032 MW queue, and the highest cooling load (3,760 cooling degree days).

## Risks and unknowns
- The queue figures are generation and storage waiting to connect. They do not show capacity available for a 200 MW load.
- The data has no parcel availability, substation or transmission capacity, or large-load tariff terms.
- It also has no permitting, zoning, local opposition or water-rights information. Water stress is a state average.
- Atlas counts differ from profile counts, and the atlases miss some facilities.

## Next diligence steps
1. Ask Pinal's utilities (APS, SRP, TEP), Oncor/CenterPoint in Dallas, and Grant PUD for 200 MW load-study timelines and tariffs.
2. Shortlist 2–3 parcels of at least the size needed in each advanced county, and check zoning and water sourcing.
3. Check Meta's El Paso load against El Paso Electric's available capacity before deciding on the alternate.
4. Confirm the serving utility in Douglas before keeping it on the list.
5. Rerun the power prices once live EIA data is available.

## Sources
Project 1 county dataset (EIA-861 2024, LBNL Queued Up through 2025, NOAA, USDA, WRI, Census), IM3 Data Center Atlas, Compute Atlas, and EIA 2024 state fallback prices.
