import pandas as pd
import os
import re

# List Excel files and select the years of interest
directory = os.path.dirname("./data/raw/")
files = ['2081-082.xlsx','2080-081.xlsx', '2076-077.xlsx', '2079-080.xlsx', '2077-078.xlsx', '2078-079.xlsx']
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

def get_data_from_excel(file_path, sheet_nbr, header_=2):
    data = pd.read_excel(file_path, sheet_name=sheet_nbr, header=header_)
    for col in data.columns:
        data[col] = data[col].apply(convert_to_numeric)
    return data

def normalize_desc(desc):
    # Lowercase, remove extra spaces, strip
    return re.sub(r'\s+', ' ', str(desc)).strip().lower()

def get_import_data_multi_year(datalist, yearlist):
    import_rows = []
    ref_df = datalist[0]

    # Build lookup dictionaries for each dataframe using normalized description
    lookup_dicts = []
    for df in datalist:
        for _, row in df.iterrows():
            print(row)
            break
        lookup = {normalize_desc(row[1]): row for _, row in df.iterrows()}
        lookup_dicts.append(lookup)

    for idx, ref_row in ref_df.iterrows():
        desc_ref_norm = normalize_desc(ref_row.iloc[1])
        descs = [ref_row.iloc[1]]
        units = [ref_row.iloc[2]]
        quantities = [ref_row.iloc[3]]
        imps = [ref_row.iloc[4]]

        for i in range(1, len(datalist)):
            row = lookup_dicts[i].get(desc_ref_norm)
            if row is not None:
                descs.append(row.iloc[1])
                units.append(row.iloc[2])
                quantities.append(row.iloc[3])
                imps.append(row.iloc[4])
            else:
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

# Load all dataframes
df1 = get_data_from_excel(files_ls[0], sheet_nbr=4)
df2 = get_data_from_excel(files_ls[1], sheet_nbr=4)
df3 = get_data_from_excel(files_ls[2], sheet_nbr=4)
df4 = get_data_from_excel(files_ls[3], sheet_nbr=4)
df5 = get_data_from_excel(files_ls[4], sheet_nbr=4)
df6 = get_data_from_excel("./data/raw/2074-075.xlsx", sheet_nbr=4, header_=2)
df7 = get_data_from_excel("./data/raw/2075-076.xlsx", sheet_nbr=3, header_=1)

year1 = files[0].split('.')[0].split("_")[0].replace('-', '/')
year2 = files[1].split('.')[0].replace('-', '/')
year3 = files[2].split('.')[0].replace('-', '/')
year4 = files[3].split('.')[0].replace('-', '/')
year5 = files[4].split('.')[0].replace('-', '/')
year6 = "2074/075"
year7 = "2075/076"
print(year1)
datalist = [df1, df2, df3, df4, df5, df6, df7]
yearlist = [year1, year2, year3, year4, year5, year6, year7]

print(df1.shape)
import_df = get_import_data_multi_year(datalist, yearlist)

imports = pd.DataFrame()
cols = [col for col in import_df.columns if col.endswith('_quant') or col.endswith('_import')]

print(import_df.head())
imports["Product"] = import_df[f"{year1}_desc"]
imports["Unit"] = import_df[f"{year1}_unit"]
for col in cols:
    imports[col] = import_df[col]
imports.to_excel("imp_commoditydata.xlsx", index=False)




"Coffee husks and skins,coffee substitutes containing coffee in any proportion"
"Coffee husks and skins,coffee substitutes  containing coffee in any proportion"