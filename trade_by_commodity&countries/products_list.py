import pandas as pd
import os
import re

# List Excel files and select the years of interest
directory = os.path.dirname("./data/raw/")
files = ['2081-082.xlsx', '2080-081.xlsx', '2076-077.xlsx', '2079-080.xlsx', '2077-078.xlsx', '2078-079.xlsx']
files_ls = [os.path.join(directory, file) for file in files]

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

def clean_description(desc):
    if pd.isna(desc) or str(desc).lower().strip() in ['nan', 'none', 'null', '']:
        return None
    # Remove punctuation and standardize spacing
    cleaned = re.sub(r'[^\w\s]', '', str(desc).lower()).strip()
    # Convert multiple spaces to single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned if cleaned else None

def get_data_from_excel(file_path, sheet_nbr, header_=2):
    data = pd.read_excel(file_path, sheet_name=sheet_nbr, header=header_)
    for col in data.columns:
        data[col] = data[col].apply(convert_to_numeric)
    
    # Clean descriptions
    desc_col = data.columns[1]
    data[desc_col] = data[desc_col].apply(clean_description)
    
    # Filter out rows with None/NaN descriptions
    data = data[data[desc_col].notna()].reset_index(drop=True)
    
    # Precompute token sets for descriptions
    data['desc_tokens'] = data[desc_col].apply(lambda x: set(re.findall(r'\b\w+\b', str(x).lower())))
    return data

def jaccard_similarity(words1, words2):
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union if union != 0 else 0

def get_import_data_multi_year(datalist, yearlist, threshold=0.75):
    import_rows = []
    ref_df = datalist[0]
    token_sets = [df['desc_tokens'].tolist() for df in datalist]

    for idx, ref_row in ref_df.iterrows():
        words_ref = ref_row['desc_tokens']
        desc_ref = str(ref_row.iloc[1])
        descs = [desc_ref]
        units = [ref_row.iloc[2]]
        quantities = [ref_row.iloc[3]]
        imps = [ref_row.iloc[4]]

        for i in range(1, len(datalist)):
            found = False
            for j, words in enumerate(token_sets[i]):
                if jaccard_similarity(words_ref, words) >= threshold:
                    row = datalist[i].iloc[j]
                    descs.append(str(row.iloc[1]))
                    units.append(row.iloc[2])
                    quantities.append(row.iloc[3])
                    imps.append(row.iloc[4])
                    found = True
                    break
            if not found:
                descs.append(None)
                units.append(None)
                quantities.append(None)
                imps.append(None)

        import_row = {}
        for y, desc, unit, quantity, imp in zip(yearlist, descs, units, quantities, imps):
            import_row[f"{y}_desc"] = desc
            import_row[f"{y}_unit"] = unit
            import_row[f"{y}_quant"] = quantity
            import_row[f"{y}_import"] = imp
        import_rows.append(import_row)

    import_df = pd.DataFrame(import_rows)
    return import_df

# Load all dataframes and precompute tokens
df1 = get_data_from_excel(files_ls[0], sheet_nbr=4)
df2 = get_data_from_excel(files_ls[1], sheet_nbr=4)
df3 = get_data_from_excel(files_ls[2], sheet_nbr=4)
df4 = get_data_from_excel(files_ls[3], sheet_nbr=4)
df5 = get_data_from_excel(files_ls[4], sheet_nbr=4)
df6 = get_data_from_excel(files_ls[5], sheet_nbr=4)
df7 = get_data_from_excel("./data/raw/2074-075.xlsx", sheet_nbr=4, header_=2)
df8 = get_data_from_excel("./data/raw/2075-076.xlsx", sheet_nbr=3, header_=1)

year0 = files[0].split('.')[0].split("_")[0].replace('-', '/')
year1 = files[1].split('.')[0].replace('-', '/')
year2 = files[2].split('.')[0].replace('-', '/')
year3 = files[3].split('.')[0].replace('-', '/')
year4 = files[4].split('.')[0].replace('-', '/')
year5 = files[5].split('.')[0].replace('-', '/')
year6 = "2074/075"
year7 = "2075/076"

datalist = [df1, df2, df3, df4, df5, df6, df7, df8]
yearlist = [year0, year1, year2, year3, year4, year5, year6, year7]

# --- Append missing descriptions to 2081/082 file and add source year and unit ---
desc_col = df1.columns[1]
print(desc_col)

# Get normalized set of descriptions from 2081/082
desc_2081 = set(df1[desc_col].dropna().tolist())
missing_descs_info = []

for i, df in enumerate(datalist[1:], start=1):  # skip df1 (2081/082)
    year = yearlist[i]
    # print(df.head(n=5).iloc[:5, 1:3])
    
    # Get valid descriptions from this dataframe
    valid_descs = df.iloc[:,1].dropna().tolist()
    descs = set(valid_descs)
    
    # Find truly new descriptions that don't exist in 2081/082
    new_descs = descs - desc_2081
    
    for desc in new_descs:
        # Find the unit for this description in the current df
        mask = df.iloc[:,1] == desc
        if mask.any():
            unit_val = df.iloc[:, 2][mask].values[0]
            missing_descs_info.append({'desc': desc, 'source_year': year, 'unit': unit_val})

# Remove duplicates: keep the first year found for each description
unique_missing = {}
for item in missing_descs_info:
    desc = item['desc']
    if desc not in unique_missing and desc is not None:
        unique_missing[desc] = {'source_year': item['source_year'], 'unit': item['unit']}

# Prepare missing rows DataFrame
unit_col = df1.columns[2]
other_cols = [col for col in df1.columns if col not in [desc_col, unit_col, 'desc_tokens']]

# Create DataFrame only if there are missing descriptions
if unique_missing:
    missing_rows = pd.DataFrame({
        desc_col: list(unique_missing.keys()),
        unit_col: [v['unit'] for v in unique_missing.values()],
        'source_year': [v['source_year'] for v in unique_missing.values()]
    })
    
    # Add other columns with NA values
    for col in other_cols:
        if col != 'source_year':
            missing_rows[col] = pd.NA
    
    # Add desc_tokens for consistency
    missing_rows['desc_tokens'] = missing_rows[desc_col].apply(
        lambda x: set(re.findall(r'\b\w+\b', str(x).lower())) if x is not None else set()
    )
    
    # Add source_year column to df1 for consistency
    if 'source_year' not in df1.columns:
        df1['source_year'] = '2081/082'
    
    # Append missing rows to df1
    df1_extended = pd.concat([df1, missing_rows], ignore_index=True)
else:
    # If no missing descriptions, just add source_year
    df1_extended = df1.copy()
    if 'source_year' not in df1_extended.columns:
        df1_extended['source_year'] = '2081/082'

# Save or print the result
df1_extended.to_excel("2081-082_extended1.xlsx", index=False)
print(f"Extended dataset created with {len(df1_extended)} products ({len(df1)} original + {len(df1_extended) - len(df1)} added).")