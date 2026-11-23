"""Tools the site-selection agent can call.

Every tool returns a JSON-serialisable dict. Numbers come straight from the data or an API, never
from the language model, and every result says where it came from (`source`) so the memo can cite it.

Tools
  find_county            resolve a county name (+ optional state) to a FIPS code; lists matches if ambiguous
  get_county_profile     the Project 1 model score, rank and drivers, plus the county's key facts
  rank_counties          discover candidates: top-scoring counties matching filters (state, price, population)
  get_grid_queue         active interconnection requests in the county (LBNL Queued Up), by fuel type
  get_known_sites        existing and planned data centers in the county (IM3 Atlas, Compute Atlas)
  get_live_power_price   latest monthly industrial electricity price for a state from the EIA API
                         (falls back to the 2024 annual figure if there is no EIA key or the API fails)
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
KEY = "county_fips"
MODEL_NOTE = ("Score = Project 1 model's probability that a county looks like counties hosting data centers "
              "(L1-logistic, spatial cross-validation; each state scored by a model that never saw it). "
              "It reflects where developers HAVE built, not a guarantee of suitability.")
STATES = {"AL", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
          "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR",
          "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"}
STATE_NAMES = {"alabama": "AL", "arizona": "AZ", "arkansas": "AR", "california": "CA", "colorado": "CO", "connecticut": "CT",
               "delaware": "DE", "district of columbia": "DC", "florida": "FL", "georgia": "GA", "idaho": "ID", "illinois": "IL",
               "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
               "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO", "montana": "MT",
               "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
               "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
               "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
               "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
               "alaska": "AK", "hawaii": "HI"}


@lru_cache(maxsize=1)
def counties() -> pd.DataFrame:
    df = pd.read_csv(DATA / "counties.csv", dtype={KEY: str})
    df["_key"] = df["county"].map(_norm)
    return df


@lru_cache(maxsize=1)
def sites() -> pd.DataFrame:
    return pd.read_csv(DATA / "sites.csv", dtype={KEY: str})


@lru_cache(maxsize=1)
def queue() -> pd.DataFrame:
    return pd.read_csv(DATA / "queue_projects.csv", dtype={KEY: str})


def _norm(name: str) -> str:
    s = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\b(county|parish|borough|census area|municipality)\b", " ", s)
    s = re.sub(r"\bst\.?\s", "saint ", s)
    return re.sub(r"[^a-z]", "", s)


def _state(state: str | None) -> str | None:
    if not state:
        return None
    s = state.strip()
    return s.upper() if len(s) == 2 else STATE_NAMES.get(s.lower(), s.upper())


def _clean(d: dict) -> dict:
    """Make pandas/numpy values JSON-friendly."""
    out = {}
    for k, v in d.items():
        if k.startswith("_"):
            continue
        if pd.isna(v) if not isinstance(v, (list, dict, str)) else False:
            out[k] = None
        elif hasattr(v, "item"):
            out[k] = v.item()
        else:
            out[k] = v
    return out


def _is_city(fips: str) -> bool:
    """Independent cities (VA, MD, MO, NV) have county codes 510+ and share names with counties."""
    return fips[:2] in {"51", "24", "29", "32"} and int(fips[2:]) >= 510


# ----------------------------------------------------------------------------------------------
def find_county(name: str, state: str | None = None) -> dict:
    st = _state(state)
    if st in {"AK", "HI"}:
        return {"status": "unsupported", "message": f"{st} is outside our data (contiguous US + DC only)."}
    if st and st not in STATES:
        return {"status": "not_found", "message": f"Unknown state '{state}'."}
    df = counties()
    hits = df[df["_key"] == _norm(name)]
    if st:
        hits = hits[hits["state"] == st]
    if hits.empty:  # partial match as a fallback
        hits = df[df["_key"].str.contains(_norm(name), regex=False)]
        if st:
            hits = hits[hits["state"] == st]
    if hits.empty:
        return {"status": "not_found", "message": f"No county matching '{name}'" + (f" in {st}" if st else "") + "."}
    matches = [{"county_fips": r[KEY], "county": r["county"] + (" (independent city)" if _is_city(r[KEY]) else ""),
                "state": r["state"]} for _, r in hits.iterrows()]
    if len(matches) > 1:
        return {"status": "ambiguous", "message": f"{len(matches)} counties match; ask which state or pick one.",
                "matches": matches[:40]}
    return {"status": "ok", **matches[0]}


def get_county_profile(county_fips: str) -> dict:
    df = counties()
    row = df[df[KEY] == str(county_fips).zfill(5)]
    if row.empty:
        return {"status": "not_found", "message": f"No county with FIPS {county_fips}. Use find_county first."}
    r = _clean(row.iloc[0].to_dict())
    r["counties_in_state"] = int((df["state"] == r["state"]).sum())
    return {"status": "ok", "profile": r, "model_note": MODEL_NOTE,
            "units": {"industrial_price_cents": "cents/kWh (2024 EIA-861, utility-weighted)",
                      "water_stress_0to5_state": "WRI Aqueduct score, state average (0 low - 5 extremely high)",
                      "drought_risk_0to5_state": "WRI Aqueduct score, state average",
                      "farmland_value_per_acre": "USD per acre, USDA 2022 (proxy for land cost)",
                      "queue_years_to_online": "median years from request to operation (county if >=3 projects, else regional)"},
            "source": "Project 1 county dataset (EIA-861, LBNL, NOAA, USDA, WRI, Census, IM3, Compute Atlas)"}


def rank_counties(state: str | None = None, max_price_cents: float | None = None, min_population: int | None = None,
                  exclude_existing: bool = True, top_n: int = 10, sort_by: str = "model_score") -> dict:
    df = counties()
    st = _state(state)
    if st:
        if st not in STATES:
            return {"status": "unsupported", "message": f"'{state}' is not in our data (contiguous US + DC)."}
        df = df[df["state"] == st]
    if max_price_cents is not None:
        df = df[df["industrial_price_cents"] <= max_price_cents]
    if min_population is not None:
        df = df[df["population"] >= min_population]
    if exclude_existing:
        df = df[df["has_data_center"] == 0]
    if sort_by not in {"model_score", "industrial_price_cents"}:
        sort_by = "model_score"
    df = df.sort_values(sort_by, ascending=sort_by != "model_score").head(max(1, min(int(top_n), 25)))
    if df.empty:
        return {"status": "no_results", "message": "No counties match these filters. Loosen a constraint."}
    cols = [KEY, "county", "state", "model_score", "score_percentile", "industrial_price_cents", "population",
            "has_data_center", "pipeline_sites", "pipeline_mw", "drivers"]
    return {"status": "ok", "filters": {"state": st, "max_price_cents": max_price_cents, "min_population": min_population,
                                        "exclude_existing": exclude_existing, "sort_by": sort_by},
            "counties": [_clean(r) for r in df[cols].to_dict("records")], "model_note": MODEL_NOTE,
            "source": "Project 1 county dataset"}


def get_grid_queue(county_fips: str) -> dict:
    fips = str(county_fips).zfill(5)
    if counties()[counties()[KEY] == fips].empty:
        return {"status": "not_found", "message": f"No county with FIPS {county_fips}."}
    q = queue()[queue()[KEY] == fips]
    if q.empty:
        return {"status": "ok", "active_projects": 0, "active_mw": 0,
                "message": "No active interconnection requests in this county.", "source": "LBNL Queued Up (through 2025)"}
    by_type = q.groupby("project_type")["mw"].agg(["count", "sum"]).sort_values("sum", ascending=False)
    return {"status": "ok", "active_projects": int(len(q)), "active_mw": round(float(q["mw"].sum()), 1),
            "by_type": [{"type": t, "projects": int(r["count"]), "mw": round(float(r["sum"]), 1)} for t, r in by_type.iterrows()],
            "oldest_request_year": int(q["request_year"].min()) if q["request_year"].notna().any() else None,
            "grid_region": q["region"].mode().iat[0], "utilities": sorted(q["utility"].dropna().unique().tolist())[:5],
            "note": "These are power plants/batteries waiting to connect: a sign of grid activity and congestion, "
                    "not available capacity for a new large load.",
            "source": "LBNL Queued Up (through 2025)"}


def get_known_sites(county_fips: str, limit: int = 15) -> dict:
    fips = str(county_fips).zfill(5)
    s = sites()[sites()[KEY] == fips]
    if s.empty:
        return {"status": "ok", "count": 0, "message": "No known data centers (operating or planned) in public atlases.",
                "source": "IM3 Data Center Atlas, Compute Atlas"}
    counts = s["status"].value_counts().to_dict()
    planned = s[s["status"].isin(["proposed", "permitted", "under_construction"])]
    show = pd.concat([planned, s.drop(planned.index)]).head(limit)
    return {"status": "ok", "count": int(len(s)), "by_status": counts,
            "planned_mw": round(float(planned["mw"].sum()), 1),
            "examples": [_clean(r) for r in show[["name", "operator", "status", "mw", "source"]].to_dict("records")],
            "note": "Public atlases miss some facilities; absence here is not proof of no data center.",
            "source": "IM3 Data Center Atlas, Compute Atlas"}


def get_live_power_price(state: str) -> dict:
    st = _state(state)
    if st not in STATES:
        return {"status": "unsupported", "message": f"'{state}' is not a supported state."}
    key = os.getenv("EIA_API_KEY")
    fallback = counties()[counties()["state"] == st]["industrial_price_cents"].median()
    fb = {"status": "fallback", "state": st, "industrial_price_cents": round(float(fallback), 2), "period": "2024 annual",
          "source": "EIA-861 2024 (median of county figures) - live EIA data unavailable"}
    if not key:
        return {**fb, "message": "No EIA_API_KEY set; using 2024 figure."}
    try:
        import requests
        r = requests.get("https://api.eia.gov/v2/electricity/retail-sales/data/", timeout=20, params={
            "api_key": key, "frequency": "monthly", "data[0]": "price", "facets[stateid][]": st,
            "facets[sectorid][]": "IND", "sort[0][column]": "period", "sort[0][direction]": "desc", "length": 12})
        r.raise_for_status()
        rows = r.json()["response"]["data"]
        if not rows:
            return {**fb, "message": "EIA returned no rows; using 2024 figure."}
        last12 = [float(x["price"]) for x in rows if x.get("price") is not None]
        return {"status": "ok", "state": st, "industrial_price_cents": float(rows[0]["price"]), "period": rows[0]["period"],
                "trailing_12mo_avg_cents": round(sum(last12) / len(last12), 2) if last12 else None,
                "source": "EIA Open Data API v2, electricity/retail-sales (industrial, monthly)"}
    except Exception as e:  # network/API problems must not crash the agent
        return {**fb, "message": f"EIA API error ({type(e).__name__}); using 2024 figure."}


# ----------------------------------------------------------------------------------------------
FUNCTIONS = {f.__name__: f for f in [find_county, get_county_profile, rank_counties, get_grid_queue,
                                      get_known_sites, get_live_power_price]}

SCHEMAS = [
    {"name": "find_county", "description": "Resolve a US county name to its 5-digit FIPS code. Always call this before other county tools. "
     "Returns status 'ambiguous' with a list of matches when the name exists in several states.",
     "input_schema": {"type": "object", "properties": {
         "name": {"type": "string", "description": "County name, e.g. 'Loudoun' or 'St. Louis'"},
         "state": {"type": "string", "description": "State name or 2-letter code, if known"}}, "required": ["name"]}},
    {"name": "get_county_profile", "description": "Project 1 model score (0-1), national and state rank, top drivers, and key facts "
     "for one county: industrial power price, population, climate, water stress, farmland value, grid queue summary, "
     "existing and planned data centers.",
     "input_schema": {"type": "object", "properties": {"county_fips": {"type": "string"}}, "required": ["county_fips"]}},
    {"name": "rank_counties", "description": "Find candidate counties: the top-scoring counties that match filters. Use for open-ended "
     "requests ('where should we look in Texas?'). By default excludes counties that already host a data center.",
     "input_schema": {"type": "object", "properties": {
         "state": {"type": "string"}, "max_price_cents": {"type": "number", "description": "Max industrial price, cents/kWh"},
         "min_population": {"type": "integer"}, "exclude_existing": {"type": "boolean", "default": True},
         "top_n": {"type": "integer", "default": 10, "description": "1-25"},
         "sort_by": {"type": "string", "enum": ["model_score", "industrial_price_cents"]}}}},
    {"name": "get_grid_queue", "description": "Active power-plant and battery interconnection requests in a county (LBNL Queued Up), "
     "by fuel type, with the oldest request year and utilities. Indicates grid activity/congestion.",
     "input_schema": {"type": "object", "properties": {"county_fips": {"type": "string"}}, "required": ["county_fips"]}},
    {"name": "get_known_sites", "description": "Existing, under-construction, permitted and proposed data centers in a county from "
     "public atlases, with operators and MW where known. Shows competition and developer interest.",
     "input_schema": {"type": "object", "properties": {"county_fips": {"type": "string"},
                                                        "limit": {"type": "integer", "default": 15}}, "required": ["county_fips"]}},
    {"name": "get_live_power_price", "description": "Latest monthly industrial electricity price for a STATE from the EIA API "
     "(cents/kWh) and its trailing 12-month average. Returns status 'fallback' with the 2024 figure if live data is unavailable.",
     "input_schema": {"type": "object", "properties": {"state": {"type": "string"}}, "required": ["state"]}},
]


def run_tool(name: str, args: dict) -> str:
    """Execute a tool by name and return its JSON result (errors become JSON too, never exceptions)."""
    fn = FUNCTIONS.get(name)
    if fn is None:
        return json.dumps({"status": "error", "message": f"Unknown tool {name}"})
    try:
        return json.dumps(fn(**(args or {})), default=str)
    except TypeError as e:
        return json.dumps({"status": "error", "message": f"Bad arguments for {name}: {e}"})
    except Exception as e:  # noqa: BLE001
        return json.dumps({"status": "error", "message": f"{name} failed: {type(e).__name__}: {e}"})
