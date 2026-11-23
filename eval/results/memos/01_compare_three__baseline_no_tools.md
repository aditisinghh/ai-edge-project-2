# 01_compare_three (no tools)

# Site-Screening Memo: 100 MW AI Campus
**Candidates:** Loudoun County, VA · El Paso County, TX · Grant County, WA

*Drafted from memory with no live data access. Figures are approximate and dated to my knowledge (roughly 2024-25). Treat every number as a hypothesis to verify, especially tariffs, queue data, and local rules, which are changing fast in all three markets.*

---

## 1. Recommendation

**Send Grant County, WA to diligence first, with El Paso running as a parallel challenger. Deprioritize Loudoun unless latency or an existing powered shell is a hard requirement.**

- **Grant:** It has by far the cheapest power (hydro, roughly 3 ¢/kWh versus 7-10 ¢ elsewhere) and a cool, dry climate suited to efficient cooling. It also has a proven data center ecosystem around Quincy, Moses Lake and Ephrata. The gating question is whether Grant PUD can commit 100 MW on your timeline. The PUD has had more load requests than it can serve, so this should be answered in the first 2-3 weeks.
- **El Paso:** This is the best fallback and may be the better primary if Grant says no or quotes a long delay. Meta's announced roughly 1 GW campus (2024) shows El Paso Electric (EPE) is willing to serve very large load. Land and entitlements are easier than in Loudoun. The risks are that 100 MW is about 5% of EPE's system peak, it needs new generation or transmission, and EPE is outside ERCOT.
- **Loudoun:** It has the deepest fiber and ecosystem but the worst combination of power timing, land cost, and entitlement friction. That is hard to justify for AI training or batch workloads that don't need Ashburn adjacency.

**Decision hinge:** If the workload is latency-insensitive (training, batch inference), power cost and speed dominate and Grant or El Paso wins. If it is latency-sensitive inference or needs dense interconnection, Loudoun's premium may be justified, but only with energized capacity already in hand.

---

## 2. Comparison table

| Factor | Loudoun, VA | El Paso, TX | Grant, WA |
|---|---|---|---|
| Population (county) | ~420-430k | ~865k | ~99-100k |
| Utility / market | Dominion (plus NOVEC in parts), PJM | El Paso Electric, WECC (not ERCOT) | Grant PUD (public hydro), BPA/Western Interconnection |
| Indicative industrial power price* | ~7-9 ¢/kWh, rising with new large-load rate class | ~7-10 ¢/kWh | ~2.5-4 ¢/kWh |
| Annual energy cost at 100 MW, 80% LF (~700 GWh) | ~$50-63M | ~$50-70M | ~$18-28M |
| Existing data center base | Largest in world, ~4+ GW operating in N. Virginia, 200+ facilities in Loudoun | Small today; Meta ~1 GW campus announced; Project Jupiter (Doña Ana, NM) nearby | Established: Microsoft, Sabey, Vantage, others in Quincy/Moses Lake/Ephrata |
| Grid / queue signal | Dominion has reported tens of GW of contracted or requested data center load; new large-load service often cited at multi-year waits (~2027-2030+) | No ERCOT-style public queue; 100 MW is ~5% of EPE peak (~2 GW); likely needs new resources | PUD has reported requests well above available capacity (order of 1 GW+); constrained, with selective approvals |
| Land / entitlement | By-right approval ended in 2025 (special exception now needed); land very expensive | Generally favorable; large tracts available | Industrial land available but limited near substations; moderate |
| Fiber / latency | Best in the US | Weak to major hubs (Dallas ~600 mi); some cross-border routes | Moderate; ~150-200 mi to Seattle/Portland routes |
| Water / cooling | Reclaimed water program; humid summers | Arid; reliance on reclaimed water; hot summers | Cool, dry climate; Columbia River; Quincy has reuse infrastructure |
|
