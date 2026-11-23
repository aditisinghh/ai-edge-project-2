"""Build the agent's knowledge base from the Project 1 repository.

    python scripts/build_knowledge_base.py --p1 ../datacenter-siting

Writes (all committed, ~2 MB total):
  data/counties.csv        one row per contiguous-US county: Project 1 model score, rank, drivers,
                           and the county facts the agent quotes (power price, population, climate,
                           water, land, grid queue, existing / planned data centers)
  data/sites.csv           known data center sites (IM3 Atlas + Compute Atlas) with county FIPS
  data/queue_projects.csv  active generation/storage interconnection requests (LBNL Queued Up)
"""
import argparse
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
KEY = "county_fips"

DRIVERS = {  # feature -> (label when it raises the score, label when it lowers it)
    "log_pop_density": ("dense population", "sparse population"),
    "log_population": ("large workforce", "small workforce"),
    "pop_growth_pct": ("fast-growing", "shrinking population"),
    "summer_max_temp_f": ("sun-belt growth market", "cool summers"),
    "annual_mean_temp_f": ("warm climate", "cool climate"),
    "cooling_degree_days_est": ("high cooling need", "low cooling need"),
    "elec_price_industrial": ("pricier power", "cheaper power"),
    "log_land_value_per_acre": ("near a metro (high land value)", "cheap land"),
    "log_land_area_km2": ("room to build", "small county"),
    "water_drought_score": ("drought risk", "low drought risk"),
    "water_stress_score": ("water stress", "low water stress"),
    "log_queue_active_n": ("active grid queue", "quiet grid queue"),
    "queue_completion_rate": ("grid projects get built", "grid projects often withdraw"),
    "n_utilities": ("several utilities", "single utility"),
}


def name_key(s: pd.Series) -> pd.Series:
    s = s.fillna("").map(lambda x: unicodedata.normalize("NFKD", str(x)).encode("ascii", "ignore").decode()).str.lower()
    s = s.str.replace(r"\b(county|parish|borough|census area|municipality)\b", " ", regex=True)
    s = s.str.replace(r"\bst\.?\s", "saint ", regex=True)
    return s.str.replace(r"[^a-z]", "", regex=True)


def drivers(feats: pd.DataFrame, coef: pd.Series) -> pd.Series:
    """Top 3 factors pushing each county's score up, from the Project 1 logistic model (standardised)."""
    cols = [c for c in coef.index if c in feats.columns and c in DRIVERS]
    z = (feats[cols] - feats[cols].mean()) / feats[cols].std()
    contrib = z * coef[cols]
    out = []
    for _, row in contrib.iterrows():
        top = row.sort_values(ascending=False)
        labels = [DRIVERS[f][0] if z.loc[row.name, f] > 0 else DRIVERS[f][1] for f in top.index[:3] if top[f] > 0]
        out.append("; ".join(labels))
    return pd.Series(out, index=feats.index)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p1", default="../datacenter-siting", help="path to the Project 1 repo")
    p1 = Path(ap.parse_args().p1)
    DATA.mkdir(exist_ok=True)

    f = pd.read_csv(p1 / "data/processed/features.csv", dtype={KEY: str})
    pred = pd.read_csv(p1 / "results/predictions.csv", dtype={KEY: str})[[KEY, "best_model_score"]]
    coef = pd.read_csv(p1 / "results/logistic_coefficients.csv", index_col=0)["coefficient_per_sd"]
    f = f.merge(pred, on=KEY)
    region_cols = [c for c in f.columns if c.startswith("region_")]
    f["grid_region"] = f[region_cols].idxmax(axis=1).str.replace("region_", "")

    c = pd.DataFrame({
        KEY: f[KEY], "county": f["county_name"], "state": f["state"],
        "model_score": f["best_model_score"].round(4),
        "score_percentile": (f["best_model_score"].rank(pct=True) * 100).round(1),
        "national_rank": f["best_model_score"].rank(ascending=False, method="min").astype(int),
        "state_rank": f.groupby("state")["best_model_score"].rank(ascending=False, method="min").astype(int),
        "drivers": drivers(f, coef),
        "has_data_center": f["has_data_center"], "existing_sites": f[["n_sites_im3", "n_sites_ca_operational"]].max(axis=1).astype(int),
        "existing_mw": f["mw_operational"].round(1), "pipeline_sites": f["n_sites_pipeline"].astype(int),
        "pipeline_mw": f["mw_pipeline"].round(1),
        "industrial_price_cents": f["elec_price_industrial"].round(2), "price_is_state_average": f["elec_price_industrial_imputed"],
        "n_utilities": f["n_utilities"], "share_public_power": f["share_public_power"].round(2),
        "population": f["population"].round(0).astype("Int64"), "pop_density_per_km2": (f["population"] / f["land_area_km2"]).round(1),
        "pop_growth_pct_since_2020": f["pop_growth_pct"].round(2), "land_area_km2": f["land_area_km2"].round(0),
        "summer_max_temp_f": f["summer_max_temp_f"].round(1), "cooling_degree_days": f["cooling_degree_days_est"].round(0),
        "water_stress_0to5_state": f["water_stress_score"].round(2), "drought_risk_0to5_state": f["water_drought_score"].round(2),
        "farmland_value_per_acre": f["land_value_per_acre"].round(0),
        "queue_active_mw": f["queue_active_mw"].round(0), "queue_active_projects": f["queue_active_n"].astype(int),
        "queue_connected_mw": f["queue_operational_mw"].round(0), "queue_completion_rate": f["queue_completion_rate"].round(3),
        "queue_years_to_online": f["queue_years_to_online"].round(2), "grid_region": f["grid_region"],
    })
    c.sort_values(KEY).to_csv(DATA / "counties.csv", index=False)

    # Known sites
    lookup = dict(zip(zip(c["state"], name_key(c["county"])), c[KEY]))
    im3 = pd.read_csv(p1 / "data/raw/im3_data_center_atlas.csv")
    im3 = pd.DataFrame({KEY: im3["state_id"].astype(int).astype(str).str.zfill(2) + im3["county_id"].astype(int).astype(str).str.zfill(3),
                        "name": im3["name"], "operator": im3["operator"], "status": "operational", "mw": np.nan,
                        "sqft": im3["sqft"], "source": "IM3 Data Center Atlas"})
    ca = pd.read_csv(p1 / "data/raw/compute_atlas_facilities.csv")
    ca = ca[ca["facility_type"] == "data_center"]
    ca = pd.DataFrame({KEY: [lookup.get((s, k)) for s, k in zip(ca["state"], name_key(ca["county"]))],
                       "name": ca["name"], "operator": ca["operator"], "status": ca["status"],
                       "mw": ca["capacity_operational_mw"].fillna(ca["capacity_planned_mw"]), "sqft": np.nan,
                       "source": "Compute Atlas"})
    sites = pd.concat([im3, ca]).dropna(subset=[KEY])
    sites.to_csv(DATA / "sites.csv", index=False)

    # Active interconnection queue
    q = pd.read_excel(p1 / "data/raw/lbnl_ix_queue_thru2025.xlsx", sheet_name="03. Complete Queue Data", header=1)
    q = q[q["q_status"].isin(["active", "suspended"]) & q["fips_code"].notna()]
    q = pd.DataFrame({KEY: q["fips_code"].astype(int).astype(str).str.zfill(5), "project_type": q["type_clean"],
                      "mw": pd.to_numeric(q["mw_1"], errors="coerce").clip(lower=0), "request_year": q["q_year"],
                      "status": q["q_status"], "phase": q["IA_phase_clean"], "region": q["region"], "utility": q["utility"]})
    q.to_csv(DATA / "queue_projects.csv", index=False)
    for p in ["counties.csv", "sites.csv", "queue_projects.csv"]:
        print(f"{p:20s} {pd.read_csv(DATA / p).shape}  {(DATA / p).stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
