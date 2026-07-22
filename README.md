# Global Bank Income Structure — IMF Financial Soundness Indicators (2000-2025)

A cross-country analysis of **Interest Margin to Gross Income** — the share of a bank's
income that comes from lending margins rather than fees, commissions, or trading — across
145 countries and 25 years, using IMF/World Bank Financial Soundness Indicator data.

**[Live dashboard on Tableau Public → link here once published]**

## What this measures

`Interest Margin to Gross Income = Net Interest Income / Gross Income`, expressed as a
percentage. A high ratio means a country's banking sector leans heavily on the traditional
"borrow low, lend high" business and is structurally exposed to interest-rate risk; a lower
ratio means banks earn more from fees and trading, which diversifies income but introduces
different volatility. It's tracked by the IMF as a **Core Financial Soundness Indicator**
because it's a direct read on how exposed a country's banking system is to margin
compression.

## Data source

- **Indicator data:** IMF Financial Soundness Indicators (Core FSI), series `FSI99_CFSI`,
  distributed via the World Bank / IMF joint data portal
  ([data.imf.org/en/datasets/IMF.STA:FSIC](https://data.imf.org/en/datasets/IMF.STA:FSIC)).
- **Region / income classification:** World Bank Country and Lending Groups, FY2026
  ([datahelpdesk.worldbank.org](https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups)).

## Cleaning & standardization process

The raw export has 31 columns (mostly constant metadata) and reports the same indicator at
three different frequencies — Annual, Quarterly, and Monthly — for the same country-years.

Before combining them, I checked whether the "Annual" value was an average of that year's
quarters. It wasn't — it was identical to the Q4 (and December) value every time. This
indicator is reported as a **year-to-date cumulative figure** (Q1 = first quarter, Q2 = first
half, Q3 = nine months, Q4 = full year = "Annual"), so averaging the four quarters would have
been mathematically wrong. Instead, `scripts/clean_fsi_data.py` standardizes each
country-year using a priority rule: reported Annual value first, else the Q4 quarterly value,
else the December monthly value — collapsing three overlapping series into one clean
observation per country per year with no double-counting.

Further steps:
- Dropped 2026 (no country has a complete year yet — only partial Q1/early-month data).
- Dropped 8 countries with fewer than 8 years of history (not enough to plot a trend).
- Flagged (not deleted) 2 statistical outliers — Ireland 2010 (-294%) and Estonia 2010
  (+101%) — both real banking-crisis distortions where gross income collapsed toward zero,
  kept in the data but flagged so a map or chart color scale isn't wrecked by them.

`scripts/add_region_income.py` then merges in World Bank region and income-group
classifications by country name (143 of 145 countries matched; Anguilla and Montserrat are
UK overseas territories the World Bank doesn't classify).

**Final dataset:** `data/IMF_FSI_interest_margin_with_region.csv` — 2,346 rows, 145 countries,
2000-2025, zero missing values in the core fields, one row per country-year.

| column | description |
|---|---|
| `country` | Country/economy name (World Bank naming convention) |
| `year` | Calendar year |
| `interest_margin_to_gross_income_pct` | Standardized annual value (%) |
| `source` | Which raw series the annual figure came from |
| `is_extreme_value` | Flags crisis-driven outliers (\|value\| > 100%) |
| `region` | World Bank region (7 categories) |
| `income_group` | World Bank income classification (4 categories) |

## Key findings

- *(fill in once the dashboard is finished — e.g. which regions/income groups rely most on
  interest margin, how the 2008-2010 crisis shows up across Europe, any post-2020 trend)*

## Tools

Python (pandas) for cleaning and standardization, Tableau for visualization.

## Reproduce it

```bash
pip install pandas openpyxl
python scripts/clean_fsi_data.py       # -> data/IMF_FSI_interest_margin_cleaned.csv
python scripts/add_region_income.py    # -> data/IMF_FSI_interest_margin_with_region.csv
```
