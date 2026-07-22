import pandas as pd
import numpy as np

SRC = "../data/raw/IMF_FSIC_FSI99_CFSI.csv"

# ---------------------------------------------------------------------------
# STEP 1 — Load only the columns we actually need.
# The raw IMF SDMX export has 31 columns, most of them constant metadata
# (unit type, database id, derivation type, etc.) that carry no analytical
# value for this single-indicator file. We keep only what varies.
# ---------------------------------------------------------------------------
cols = ["REF_AREA_LABEL", "FREQ_LABEL", "TIME_PERIOD", "OBS_VALUE"]
df = pd.read_csv(SRC, usecols=cols)
df = df.rename(columns={
    "REF_AREA_LABEL": "country",
    "FREQ_LABEL": "freq",
    "TIME_PERIOD": "period",
    "OBS_VALUE": "value",
})
print(f"[1] Loaded {len(df):,} raw rows, {df['country'].nunique()} countries.")

# ---------------------------------------------------------------------------
# STEP 2 — Extract the calendar year from three different period formats:
#   Annual:    "2011"
#   Quarterly: "2010-Q1"
#   Monthly:   "2001-M03"
# and also extract the sub-period (quarter/month number) so we can find
# the year-end observation later.
# ---------------------------------------------------------------------------
def parse_period(row):
    p, f = row["period"], row["freq"]
    if f == "Annual":
        return int(p), None
    if f == "Quarterly":
        y, q = p.split("-Q")
        return int(y), int(q)
    if f == "Monthly":
        y, m = p.split("-M")
        return int(y), int(m)
    return None, None

df[["year", "subperiod"]] = df.apply(parse_period, axis=1, result_type="expand")
print(f"[2] Parsed year/sub-period for all rows.")

# ---------------------------------------------------------------------------
# STEP 3 — Understand *why* there are 3 frequencies per country before
# blindly averaging them. Investigation (done interactively first) showed
# that for any given country-year, the Annual value is IDENTICAL to the
# Q4 quarterly value, and Q4 quarterly is identical to the December (M12)
# monthly value. That's because this FSI is an income-statement ratio
# reported on a year-to-date cumulative basis: Q1 = first quarter only,
# Q2 = first half cumulative, Q3 = first 9 months cumulative, Q4 = full
# year cumulative = the "Annual" figure. So the three frequencies are not
# independent measurements to be averaged — they are the SAME underlying
# cumulative series sampled at different checkpoints in the year.
#
# Standardization rule (priority order per country-year):
#   1. Use the reported Annual value if it exists.
#   2. Else use the Quarterly Q4 value (year-end cumulative == annual).
#   3. Else use the Monthly M12 value (December cumulative == annual).
#   4. Else: no full-year observation exists yet (e.g. current in-progress
#      year) -> leave that country-year out of the standardized panel.
# ---------------------------------------------------------------------------
annual = df[df["freq"] == "Annual"][["country", "year", "value"]].copy()
annual["source"] = "Annual (reported)"

q4 = df[(df["freq"] == "Quarterly") & (df["subperiod"] == 4)][["country", "year", "value"]].copy()
q4["source"] = "Quarterly Q4 (year-end)"

m12 = df[(df["freq"] == "Monthly") & (df["subperiod"] == 12)][["country", "year", "value"]].copy()
m12["source"] = "Monthly M12 (year-end)"

# Priority stack: keep Annual first; for country-years missing from Annual,
# fill from Q4; for those still missing, fill from M12.
combined = pd.concat([annual, q4, m12], ignore_index=True)
combined = combined.sort_values("source", key=lambda s: s.map({
    "Annual (reported)": 0, "Quarterly Q4 (year-end)": 1, "Monthly M12 (year-end)": 2
}))
standardized = combined.drop_duplicates(subset=["country", "year"], keep="first").copy()
standardized = standardized.sort_values(["country", "year"]).reset_index(drop=True)

print(f"[3] Standardized to one full-year observation per country-year: {len(standardized):,} rows.")
print(standardized["source"].value_counts())

# ---------------------------------------------------------------------------
# STEP 4 — Drop the current in-progress year. 2026 only has partial data
# (Q1 / M01-M05) for any country in this file, which under our rule means
# no country actually has a *complete* 2026 figure yet — confirm and drop.
# ---------------------------------------------------------------------------
before = len(standardized)
standardized = standardized[standardized["year"] < 2026]
print(f"[4] Dropped {before - len(standardized)} incomplete-year rows (2026 in progress).")

# ---------------------------------------------------------------------------
# STEP 5 — Flag (not delete) statistical outliers. This ratio is a
# percentage that normally sits between 0-100, but during banking crises
# (Ireland 2010, Estonia 2009, Lebanon 2020) gross income collapses toward
# zero and the ratio swings far outside that range. These are real events,
# not data errors, so we keep them and just flag them — useful both for a
# "crisis years" callout in the dashboard and so a map/chart color scale
# isn't wrecked by a handful of extreme values.
# ---------------------------------------------------------------------------
standardized["is_extreme_value"] = standardized["value"].abs() > 100

# ---------------------------------------------------------------------------
# STEP 6 — Coverage filter. A country with only 2-3 years of history can't
# support a trend chart. Keep countries with at least 8 distinct years so
# every series shown on the dashboard can actually tell a "change over
# time" story.
# ---------------------------------------------------------------------------
years_per_country = standardized.groupby("country")["year"].nunique()
keep_countries = years_per_country[years_per_country >= 8].index
before_c = standardized["country"].nunique()
standardized = standardized[standardized["country"].isin(keep_countries)]
print(f"[5] Kept {standardized['country'].nunique()} of {before_c} countries with >= 8 years of history.")

# ---------------------------------------------------------------------------
# STEP 7 — Final tidy output, one row per country-year, ready to load
# straight into Tableau / Power BI as the fact table.
# ---------------------------------------------------------------------------
standardized["year"] = standardized["year"].astype(int)
standardized["interest_margin_to_gross_income_pct"] = standardized["value"].round(2)
standardized = standardized.rename(columns={"value": "_value_raw"})
standardized = standardized[[
    "country", "year", "interest_margin_to_gross_income_pct", "source", "is_extreme_value"
]].sort_values(["country", "year"]).reset_index(drop=True)

out_path = "../data/IMF_FSI_interest_margin_cleaned.csv"
standardized.to_csv(out_path, index=False)
print(f"[6] Wrote cleaned file: {out_path}  ({len(standardized):,} rows, "
      f"{standardized['country'].nunique()} countries, "
      f"{standardized['year'].min()}-{standardized['year'].max()})")
print(standardized.head(10).to_string(index=False))
