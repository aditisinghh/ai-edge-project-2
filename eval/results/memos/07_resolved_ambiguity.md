# 07_resolved_ambiguity

**Request:** Screen Washington County, Oregon for a 50 MW facility.

**Tool calls (5):**
- `find_county({"name": "Washington", "state": "Oregon"})`
- `get_county_profile({"county_fips": "41067"})`
- `get_grid_queue({"county_fips": "41067"})`
- `get_known_sites({"county_fips": "41067"})`
- `get_live_power_price({"state": "OR"})`

---

## Recommendation
Advance Washington County, OR to on-the-ground diligence, but only if the team can confirm 50 MW of deliverable power. The county looks like proven data center territory: it is in the 95.2th percentile on the model score, with a cool climate and a large workforce. It is also crowded, and the data says nothing about whether the grid can serve a new 50 MW load.

## Comparison
| County | Model score (percentile) | Power ¢/kWh | Population | Data centers (existing / planned) | Grid queue MW |
|---|---|---|---|---|---|
| Washington, OR | 0.879 (95.2) | 8.72 county; 8.7 state | 611,708 | 23 / 7 sites, 226 MW planned (profile) | 1,300 active (5 battery projects) |

National rank is 149, and state rank is 2 of 36 counties.

## County notes
- **Strengths**
  - Summer max temperature is 77.8°F and cooling degree days are 143, so cooling load should be low.
  - Population density is 326.1 per km², population growth since 2020 is 1.89%, and the labor pool is large.
  - Existing sites total 308.3 MW, which shows an established ecosystem.
  - Public power share is 0.67 across 3 utilities. The queue data lists Portland General Electric.
  - Farmland value is $22,445 per acre (USDA 2022). It is only a rough proxy for land cost.
- **Red flags**
  - Competition is heavy. Named proposed or under-construction projects include Crane PDX01 (76 MW) and PDX02 (48 MW), STACK Hillsboro (75 MW), Flexential Hillsboro 6 (27 MW), CoreSite, Digital Realty, Hines and QTS. These developers will compete for the same power and land.
  - The grid queue is 1,300 MW, all batteries, and the oldest request is from 2021. The tool says this signals congestion, not available capacity. Median time from request to operation is 2.87 years, and the queue completion rate is 0.5.
  - The state water stress score is 2.22 of 5 and the drought risk score is 1.55 of 5. Both are state averages, not county figures.
  - The data sources disagree on counts. The profile shows 23 existing sites and 7 pipeline sites. The site atlas lists 50 entries: 42 operational, 5 proposed, 2 under construction and 1 permitted. Treat the counts as approximate.

## Risks and unknowns
- The model score reflects where developers have built before. It does not guarantee suitability.
- The data has no parcel availability, zoning, or land pricing beyond the farmland proxy.
- It has no substation or feeder capacity, no PGE or other utility load-service timeline, and no information on whether 50 MW can be served.
- It does not cover permitting, local opposition, or water rights or cooling-water sourcing.
- Power prices are not live. The EIA live feed was unavailable, so the state figure (8.7¢) is the 2024 fallback. The county figure (8.72¢) is the 2024 EIA-861 utility-weighted value.

## Next diligence steps
1. Ask the serving utility for a load-service study and a realistic energization date for 50 MW. Use a written response, not the queue data.
2. Identify specific parcels and check zoning, the utility's substation proximity, and whether competitor projects have already claimed nearby capacity.
3. Check local permitting, water and cooling approach, and community sentiment toward data centers.
4. Reconcile the site counts against local planning records, and confirm the live industrial tariff.
5. Run a power-cost comparison with the state's #1 county or other Pacific Northwest alternatives. I can run that screen if you want it.

## Sources
- Project 1 county dataset, which draws on EIA-861, LBNL, NOAA, USDA, WRI, Census and IM3.
- LBNL Queued Up (through 2025).
- IM3 Data Center Atlas and Compute Atlas.
- EIA-861 2024 fallback for the state power price.
