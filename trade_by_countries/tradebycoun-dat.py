import pandas as pd
import os
import re

def convert_to_numeric(value):
    if pd.isna(value):
        return value
    if isinstance(value, str):
        cleaned_value = value.replace(',', '')
        try:
            return float(cleaned_value)
        except ValueError:
            return value
    return value

def get_data_from_excel(file_path, sheet_nbr, header_=2):
    data = pd.read_excel(file_path, sheet_name=sheet_nbr, header=header_)
    for col in data.columns:
        data[col] = data[col].apply(convert_to_numeric)
    # data = data.dropna()
    return data

def jaccard_similarity(words1, words2):
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union if union != 0 else 0

def get_import_data_multi_year(datalist, yearlist, threshold=1):
    all_countries = set()
    for df in datalist:
        countries = df.iloc[:, 1].dropna().astype(str).tolist()
        all_countries.update(countries)
    
    import_rows = []
    for country_ref in sorted(all_countries):
        words_ref = set(re.findall(r'\b\w+\b', country_ref.lower()))
        
        # Initialize data for this country
        countries = []
        imps = []
        expts = []
        
        # Check each year's data for this country
        for i, df in enumerate(datalist):
            found = False
            for _, row in df.iterrows():
                country = str(row.iloc[1])
                words = set(re.findall(r'\b\w+\b', country.lower()))
                if jaccard_similarity(words_ref, words) >= threshold:
                    countries.append(country)
                    imps.append(row.iloc[2])
                    expts.append(row.iloc[3])
                    found = True
                    break
            if not found:
                countries.append(None)
                imps.append(None)
                expts.append(None)
        
        import_row = {}
        for y, country, imp, expt in zip(yearlist, countries, imps, expts):
            import_row[f"{y}_country"] = country
            import_row[f"{y}_import"] = imp
            import_row[f"{y}_export"] = expt
        import_rows.append(import_row)

    import_df = pd.DataFrame(import_rows)
    return import_df

file_info = [
    {"path": "./data/raw/2081-082.xlsx", "sheet_nbr": 2, "header": 2, "year": "2081/082"},
    {"path": "./data/raw/2080-081.xlsx", "sheet_nbr": 2, "header": 2, "year": "2080/081"},
    {"path": "./data/raw/2079-080.xlsx", "sheet_nbr": 2, "header": 2, "year": "2079/080"},
    {"path": "./data/raw/2078-079.xlsx", "sheet_nbr": 2, "header": 2, "year": "2078/079"},
    {"path": "./data/raw/2077-078.xlsx", "sheet_nbr": 2, "header": 2, "year": "2077/078"},
    {"path": "./data/raw/2076-077.xlsx", "sheet_nbr": 2, "header": 2, "year": "2076/077"},
    {"path": "./data/raw/2075-076.xlsx", "sheet_nbr": 2, "header": 2, "year": "2075/076"},
    {"path": "./data/raw/2074-075.xlsx", "sheet_nbr": 3, "header": 2, "year": "2074/075"},
    {"path": "./data/raw/2073-074.xlsx", "sheet_nbr": 2, "header": 2, "year": "2073/074"},
    {"path": "./data/raw/2072-073.xlsx", "sheet_nbr": 2, "header": 1, "year": "2072/073"},
    {"path": "./data/raw/2071-072.xlsx", "sheet_nbr": 1, "header": 1, "year": "2071/072"}
]

datalist = []
yearlist = []

for file in file_info:
    df = get_data_from_excel(file["path"], sheet_nbr=file["sheet_nbr"], header_=file["header"])
    datalist.append(df)
    yearlist.append(file["year"])

# Process the data
import_df = get_import_data_multi_year(datalist, yearlist)

# Find all unique country names across all years
all_countries = set()
for col in import_df.columns:
    if col.endswith('_country'):
        # Add all non-null country names to the set
        all_countries.update(import_df[col].dropna().unique())

imports = pd.DataFrame()
imports["Countries"] = sorted(list(all_countries))

# For each country, find its import/export data across all years
for col in [c for c in import_df.columns if c.endswith('_import') or c.endswith('_export')]:
    year_prefix = col.split('_')[0]
    country_col = f"{year_prefix}_country"
    
    # Initialize the column with NaN values
    imports[col] = pd.NA
    
    # Map data from the corresponding country column
    for idx, country in enumerate(imports["Countries"]):
        # Find rows where this country appears in that year
        matching_rows = import_df[import_df[country_col] == country]
        if not matching_rows.empty:
            imports.at[idx, col] = matching_rows[col].values[0]

# Save the results
imports.to_excel("./data/filtered_data/impexp_countrydata.xlsx", index=False)



