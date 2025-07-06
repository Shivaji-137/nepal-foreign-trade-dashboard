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
    import_rows = []

    ref_df = datalist[0]

    for idx, ref_row in ref_df.iterrows():
        office_ref = str(ref_row.iloc[1])
        words_ref = set(re.findall(r'\b\w+\b', office_ref.lower()))
        offices = [office_ref]
        
        imps = [ref_row.iloc[2]]
        imps_share = [ref_row.iloc[3]]
        expts = [ref_row.iloc[4]]
        expts_share = [ref_row.iloc[5]]

        # For each subsequent year, try to find a matching product
        for i in range(1, len(datalist)):
            found = False
            for _, row in datalist[i].iterrows():
                office = str(row.iloc[1])
                words = set(re.findall(r'\b\w+\b', office.lower()))
                if jaccard_similarity(words_ref, words) >= threshold:
                    offices.append(office)
                    imps.append(row.iloc[2])
                    imps_share.append(row.iloc[3])
                    expts.append(row.iloc[4])
                    expts_share.append(row.iloc[5])
                    found = True
                    break
            if not found:
                offices.append(None)
                imps.append(None)
                imps_share.append(None)
                expts.append(None)
                expts_share.append(None)

        # Build row with description and import value for each year
        import_row = {}
        for y, office, imp, imp_share, expt, expt_share in zip(yearlist, offices, imps, imps_share, expts, expts_share):
            import_row[f"{y}_office"] = office
            import_row[f"{y}_import"] = imp
            import_row[f"{y}_import_share"] = imp_share
            import_row[f"{y}_export"] = expt
            import_row[f"{y}_export_share"] = expt_share
        import_rows.append(import_row)

    import_df = pd.DataFrame(import_rows)
    return import_df

# Define sheet name for newer files
sheet_nbr76_81 = "9_Customswise_Trade"

# Define file information in descending order with correct sheet references
file_info = [
    {"path": "./data/raw/2081-082.xlsx", "sheet_nbr": sheet_nbr76_81, "header": 2, "year": "2081/082"},
    {"path": "./data/raw/2080-081.xlsx", "sheet_nbr": sheet_nbr76_81, "header": 2, "year": "2080/081"},
    {"path": "./data/raw/2079-080.xlsx", "sheet_nbr": sheet_nbr76_81, "header": 2, "year": "2079/080"},
    {"path": "./data/raw/2078-079.xlsx", "sheet_nbr": sheet_nbr76_81, "header": 2, "year": "2078/079"},
    {"path": "./data/raw/2077-078.xlsx", "sheet_nbr": sheet_nbr76_81, "header": 2, "year": "2077/078"},
    {"path": "./data/raw/2076-077.xlsx", "sheet_nbr": sheet_nbr76_81, "header": 2, "year": "2076/077"},
    {"path": "./data/raw/2075-076.xlsx", "sheet_nbr": 6, "header": 2, "year": "2075/076"},
    {"path": "./data/raw/2074-075.xlsx", "sheet_nbr": 1, "header": 2, "year": "2074/075"},
    {"path": "./data/raw/2073-074.xlsx", "sheet_nbr": 5, "header": 2, "year": "2073/074"},
    {"path": "./data/raw/2072-073.xlsx", "sheet_nbr": 5, "header": 1, "year": "2072/073"},
]

# Load data in descending order
datalist = []
yearlist = []

for file in file_info:
    df = get_data_from_excel(file["path"], sheet_nbr=file["sheet_nbr"], header_=file["header"])
    datalist.append(df)
    yearlist.append(file["year"])

# Process the data
import_df = get_import_data_multi_year(datalist, yearlist)

imports = pd.DataFrame()
cols = [col for col in import_df.columns if col.endswith('_import') or col.endswith('_export') or col.endswith('_import_share') or col.endswith('_export_share')]
descs = [col for col in import_df.columns if col.endswith('_office')]

# Use most recent year for office names
imports["Custom_offices"] = import_df[f"{yearlist[0]}_office"]  
for col in cols:
    imports[col] = import_df[col]

imports.to_excel("./data/filtered_data/customoffice_trade_allyr.xlsx", index=False)



