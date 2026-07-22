import pandas as pd

# World Bank Country and Lending Groups (FY2026), region + income classification
# Source: https://datahelpdesk.worldbank.org/knowledgebase/articles/906519
REGION = {}
INCOME = {}

def add(region, names):
    for n in names:
        REGION[n] = region

add("East Asia and Pacific", [
    "American Samoa","Korea, Rep.","Papua New Guinea","Australia","Lao PDR","Philippines",
    "Brunei Darussalam","Macao SAR, China","Samoa","Cambodia","Malaysia","Singapore",
    "China","Marshall Islands","Solomon Islands","Fiji","Micronesia, Fed. Sts.","Taiwan, China",
    "French Polynesia","Mongolia","Thailand","Guam","Myanmar","Timor-Leste",
    "Hong Kong SAR, China","Nauru","Tonga","Indonesia","New Caledonia","Tuvalu",
    "Japan","New Zealand","Vanuatu","Kiribati","Northern Mariana Islands","Viet Nam",
    "Korea, Dem. People's Rep.","Palau",
])
add("Europe and Central Asia", [
    "Albania","Gibraltar","Norway","Andorra","Greece","Poland","Armenia","Greenland","Portugal",
    "Austria","Hungary","Romania","Azerbaijan","Iceland","Russian Federation","Belarus","Ireland",
    "San Marino","Belgium","Isle of Man","Serbia","Bosnia and Herzegovina","Italy","Slovak Republic",
    "Bulgaria","Kazakhstan","Slovenia","Channel Islands","Kosovo","Spain","Croatia","Kyrgyz Republic",
    "Sweden","Cyprus","Latvia","Switzerland","Czechia","Liechtenstein","Tajikistan","Denmark",
    "Lithuania","Türkiye","Estonia","Luxembourg","Turkmenistan","Faroe Islands","Moldova","Ukraine",
    "Finland","Monaco","United Kingdom","France","Montenegro","Uzbekistan","Georgia","Netherlands",
    "Germany","North Macedonia",
])
add("Latin America and the Caribbean", [
    "Antigua and Barbuda","Curacao","Paraguay","Argentina","Dominica","Peru","Aruba",
    "Dominican Republic","Puerto Rico","Bahamas, The","Ecuador","Sint Maarten (Dutch part)",
    "Barbados","El Salvador","St. Kitts and Nevis","Belize","Grenada","St. Lucia","Bolivia",
    "Guatemala","St. Martin (French part)","Brazil","Guyana","St. Vincent and the Grenadines",
    "British Virgin Islands","Haiti","Suriname","Cayman Islands","Honduras","Trinidad and Tobago",
    "Chile","Jamaica","Turks and Caicos Islands","Colombia","Mexico","Uruguay","Costa Rica",
    "Nicaragua","Venezuela, RB","Cuba","Panama","Virgin Islands (U.S.)",
])
add("Middle East, North Africa, Afghanistan and Pakistan", [
    "Afghanistan","Jordan","Qatar","Algeria","Kuwait","Saudi Arabia","Bahrain","Lebanon",
    "Syrian Arab Republic","Djibouti","Libya","Tunisia","Egypt, Arab Rep.","Malta",
    "United Arab Emirates","Iran, Islamic Rep.","Morocco","West Bank and Gaza","Iraq","Oman",
    "Yemen, Rep.","Israel","Pakistan",
])
add("North America", ["Bermuda", "Canada", "United States"])
add("South Asia", ["Bangladesh", "India", "Nepal", "Bhutan", "Maldives", "Sri Lanka"])
add("Sub-Saharan Africa", [
    "Angola","Ethiopia","Niger","Benin","Gabon","Nigeria","Botswana","Gambia, The","Rwanda",
    "Burkina Faso","Ghana","Sao Tome and Principe","Burundi","Guinea","Senegal","Cabo Verde",
    "Guinea-Bissau","Seychelles","Cameroon","Kenya","Sierra Leone","Central African Republic",
    "Lesotho","Somalia","Chad","Liberia","South Africa","Comoros","Madagascar","South Sudan",
    "Congo, Dem. Rep.","Malawi","Sudan","Congo, Rep","Mali","Tanzania","Cote d'Ivoire","Mauritania",
    "Togo","Equatorial Guinea","Mauritius","Uganda","Eritrea","Mozambique","Zambia","Eswatini",
    "Namibia","Zimbabwe",
])

def add_income(level, names):
    for n in names:
        INCOME[n] = level

add_income("Low income", [
    "Afghanistan","Korea, Dem. People's Rep","Somalia","Burkina Faso","Liberia","South Sudan",
    "Burundi","Madagascar","Sudan","Central African Republic","Malawi","Syrian Arab Republic",
    "Chad","Mali","Togo","Congo, Dem. Rep","Mozambique","Uganda","Eritrea","Niger","Yemen, Rep.",
    "Gambia, The","Rwanda","Guinea-Bissau","Sierra Leone",
])
add_income("Lower-middle income", [
    "Angola","India","Papua New Guinea","Bangladesh","Jordan","Philippines","Benin","Kenya",
    "Sao Tome and Principe","Bhutan","Kiribati","Senegal","Bolivia","Kyrgyz Republic",
    "Solomon Islands","Cambodia","Lao PDR","Sri Lanka","Cameroon","Lebanon","Tajikistan",
    "Comoros","Lesotho","Tanzania","Congo, Rep.","Mauritania","Timor-Leste","Cote d'Ivoire",
    "Micronesia, Fed. Sts.","Tunisia","Djibouti","Morocco","Uzbekistan","Egypt, Arab Rep.",
    "Myanmar","Vanuatu","Eswatini","Namibia","Viet Nam","Ghana","Nepal","West Bank and Gaza",
    "Guinea","Nicaragua","Zambia","Haiti","Nigeria","Zimbabwe","Honduras","Pakistan",
])
add_income("Upper-middle income", [
    "Albania","Equatorial Guinea","Moldova","Algeria","Fiji","Mongolia","Argentina","Gabon",
    "Montenegro","Armenia","Georgia","North Macedonia","Azerbaijan","Grenada","Paraguay",
    "Belarus","Guatemala","Peru","Belize","Indonesia","Samoa","Bosnia and Herzegovina",
    "Iran, Islamic Rep.","Serbia","Botswana","Iraq","South Africa","Brazil","Jamaica","St. Lucia",
    "Cabo Verde","Kazakhstan","St. Vincent and the Grenadines","China","Kosovo","Suriname",
    "Colombia","Libya","Thailand","Cuba","Malaysia","Tonga","Dominica","Maldives","Türkiye",
    "Dominican Republic","Marshall Islands","Turkmenistan","Ecuador","Mauritius","Tuvalu",
    "El Salvador","Mexico","Ukraine",
])
add_income("High income", [
    "American Samoa","Gibraltar","Panama","Andorra","Greece","Poland","Antigua and Barbuda",
    "Greenland","Portugal","Aruba","Guam","Puerto Rico","Australia","Guyana","Qatar","Austria",
    "Hong Kong SAR, China","Romania","Bahamas, The","Hungary","Russian Federation","Bahrain",
    "Iceland","San Marino","Barbados","Ireland","Saudi Arabia","Belgium","Isle of Man","Seychelles",
    "Bermuda","Israel","Singapore","British Virgin Islands","Italy","Sint Maarten (Dutch part)",
    "Brunei Darussalam","Japan","Slovak Republic","Bulgaria","Korea, Rep.","Slovenia","Canada",
    "Kuwait","Spain","Cayman Islands","Latvia","St. Kitts and Nevis","Channel Islands",
    "Liechtenstein","St. Martin (French part)","Chile","Lithuania","Sweden","Costa Rica",
    "Luxembourg","Switzerland","Croatia","Macao SAR, China","Taiwan, China","Curacao","Malta",
    "Trinidad and Tobago","Cyprus","Monaco","Turks and Caicos Islands","Czechia","Netherlands",
    "United Arab Emirates","Denmark","New Caledonia","United Kingdom","Estonia","New Zealand",
    "United States","Faroe Islands","Northern Mariana Islands","Uruguay","Finland","Norway",
    "Virgin Islands (U.S.)","France","Oman","French Polynesia","Palau","Germany","Panama",
])

# Aliases: names in our IMF/FSI file that differ slightly from the WB list spelling
ALIASES = {
    "Vietnam": "Viet Nam",
    "Somalia, Federal Republic of": "Somalia",
    "Congo, Dem. Rep.": "Congo, Dem. Rep.",   # already matches; kept for clarity
    "Cote d'Ivoire": "Cote d'Ivoire",
    "Congo, Rep.": "Congo, Rep",  # WB source page omits the trailing period
}

df = pd.read_csv("../data/IMF_FSI_interest_margin_cleaned.csv")

def lookup(country, table):
    key = ALIASES.get(country, country)
    return table.get(key)

df["region"] = df["country"].apply(lambda c: lookup(c, REGION))
df["income_group"] = df["country"].apply(lambda c: lookup(c, INCOME))

matched = df["region"].notna().sum()
total = len(df)
unmatched_countries = sorted(df.loc[df["region"].isna(), "country"].unique())

print(f"Matched {matched:,}/{total:,} rows ({df.loc[df['region'].notna(),'country'].nunique()} of "
      f"{df['country'].nunique()} countries).")
print("Unmatched countries (no WB region/income classification found):", unmatched_countries)

out_csv = "../data/IMF_FSI_interest_margin_with_region.csv"
df.to_csv(out_csv, index=False)

print(f"Wrote {out_csv}  ({df.shape[0]} rows, {df.shape[1]} columns)")
