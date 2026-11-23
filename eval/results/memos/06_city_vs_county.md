# 06_city_vs_county

**Request:** How does St. Louis, Missouri look for a data center?

**Tool calls (1):**
- `find_county({"name": "St. Louis", "state": "Missouri"})`

---

"St. Louis, Missouri" matches two separate jurisdictions in our data:

1. **St. Louis County, MO** (FIPS 29189), the large suburban county surrounding the city.
2. **St. Louis (independent city), MO** (FIPS 29510), the city itself, which is legally separate from the county.

They differ in land availability, utilities, permitting and power context, so I don't want to guess. Which one do you want screened? I can also run both side by side.
