# 07_resolved_ambiguity (no tools)

# Site-Screening Memo: Washington County, Oregon (50 MW)

**Caveat:** I have no live data access. All figures come from memory (roughly 2023-2025) and are approximate. Items marked **[verify]** need confirmation before any decision.

## Recommendation

**Conditional proceed, for a latency- or interconnect-sensitive 50 MW deployment only.** Washington County (the Hillsboro cluster) is a mature, network-rich Pacific Northwest market with good free-cooling hours and no state sales tax. It is not a low-cost-power or fast-power market. For a 50 MW build, advance only if:

1. PGE confirms a firm service path of 50 MW or more within about 30-36 months, ideally from an existing or planned substation with headroom.
2. A parcel already zoned industrial and inside the UGB is under control, or can be bought, at an acceptable price.
3. The post-2025 large-load tariff (Oregon HB 3546, the "POWER Act") leaves the all-in energy cost acceptable **[verify]**.

If the workload is bulk training or cost-driven capacity, Eastern Oregon (Morrow/Umatilla) is likely the better first choice.

## Comparison table

| Factor | Washington Co. (Hillsboro) | Morrow/Umatilla Co. | Crook Co. (Prineville) | Wasco Co. (The Dalles) |
|---|---|---|---|---|
| Population | ~600,000 | ~12,000 (Morrow); ~80,000 (Umatilla) | ~26,000 | ~26,000 |
| Primary utility | PGE (Forest Grove and Cornelius have municipal utilities) | Umatilla Electric Co-op, Port of Morrow, PGE (Boardman) | Pacific Power, Central Electric Co-op | Northern Wasco PUD, Wasco Electric Co-op, Pacific Power |
| Indicative industrial power price | ~7-9¢/kWh **[verify]** | ~4-6¢/kWh **[verify]** | ~5-7¢/kWh **[verify]** | ~4-6¢/kWh, hydro-influenced **[verify]** |
| Anchor data center presence | Digital Realty, Flexential, Aligned, Stack, Meta (Forest Grove), AWS, Google; several hundred MW total | AWS (multiple campuses) | Meta, Apple | Google |
| Power availability for 50 MW | Tight; multi-year, with large-load pipeline competition | Better, but transmission upgrades are common | Moderate | Moderate, constrained by hydro and BPA allocation |
| Network and latency | Best in Oregon: dense fiber, subsea cable backhaul, Portland metro | Good long-haul, limited metro | Moderate | Good, with a Google-driven fiber corridor |
| Land | Scarce, expensive, UGB-limited | Abundant, cheap | Available | Limited |
| Water and cooling | Mild climate, good free cooling; water politically sensitive | Dry, hot summers; water-rights scrutiny | Good climate | Good climate |
| Talent and labor | Deepest (Intel, Portland metro) | Thin | Thin | Thin |

## County notes

**Market profile.** Washington County is the western Portland metro. Hillsboro (population ~110,000) is the center of the data center cluster. It sits alongside Intel's Ronler Acres campus and a large semiconductor and fiber ecosystem. Several transpacific subsea cable systems backhaul through the Oregon coast to Hillsboro **[verify specific systems]**. This makes it a strong interconnection and edge-to-cloud location.

**Power.** PGE serves most of the county. Hillsboro's data center load is already substantial, and PGE has publicly described a multi-GW large-load interest pipeline across its territory **[verify current figure]**. For a 50 MW load, the likely path is a 115 kV or dedicated-substation service, and lead times for transformers and substation work can drive timelines to 3 years or more. I cannot cite a specific queue MW figure for the county; request this from PGE directly. Oregon's 2025 POWER Act creates a separate rate class for large loads (roughly 20 MW and above) intended to prevent cost-shifting to residential customers. Expect longer-term contract commitments and possible collateral or minimum-take terms **[verify]**.

**Incentives and tax.** Oregon has no sales tax. Enterprise zone abatements (typically 3-5 years of property tax exemption on new equipment) have historically been used in Hillsboro. Their continued availability for data centers has been under legislative and local scrutiny **[verify]**.

**Water and sustainability.** Hillsboro draws on the Joint Water Commission and is building out the Willamette Water Supply System. Community and regulatory attention to data center water use is rising. Favor air-cooled or closed-loop designs, and expect reporting expectations.

**Hazards.** The Cascadia Subduction Zone is the major seismic concern, and design should follow high seismic criteria. Wildfire smoke affects air filtration and operations in late summer. Flood risk is parcel-specific along the Tualatin River.

## Risks and unknowns

- **Power timing and cost** are the largest risks. Utility capacity, queue position, and tariff terms are unconfirmed.
- **Land availability.** Few large industr
