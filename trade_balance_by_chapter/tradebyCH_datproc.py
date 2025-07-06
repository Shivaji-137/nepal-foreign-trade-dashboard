import pandas as pd
import os
import re

# List Excel files and select the two years of interest
directory = os.path.dirname("./data/raw/")
files = ['2076-077.xlsx', '2079-080.xlsx', '2077-078.xlsx','2078-079.xlsx', '2080-081.xlsx', "2081-082.xlsx"]
files = [os.path.join(directory, file) for file in files]
print(files)

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
    data = data.dropna()
    return data


def jaccard_similarity(words1, words2):
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union if union != 0 else 0

def get_import_data_multi_year(datalist, yearlist, threshold=0.75):
    import_rows = []

    ref_df = datalist[-1]

    for idx, ref_row in ref_df.iterrows():
        desc_ref = str(ref_row.iloc[1])
        words_ref = set(re.findall(r'\b\w+\b', desc_ref.lower()))
        descs = [desc_ref]
        imps = [ref_row.iloc[2]]
        expts = [ref_row.iloc[3]]

        # For each subsequent year, try to find a matching product
        for i in range(1, len(datalist)):
            found = False
            for _, row in datalist[i].iterrows():
                desc = str(row.iloc[1])
                words = set(re.findall(r'\b\w+\b', desc.lower()))
                if jaccard_similarity(words_ref, words) >= threshold:
                    descs.append(desc)
                    imps.append(row.iloc[2])
                    expts.append(row.iloc[3])
                    found = True
                    break
            if not found:
                descs.append(None)
                imps.append(None)
                expts.append(None)

        # Build row with description and import value for each year
        import_row = {}
        for y, desc, imp, expt in zip(yearlist, descs, imps, expts):
            import_row[f"{y}_desc"] = desc
            import_row[f"{y}_import"] = imp
            import_row[f"{y}_export"] = expt
        import_rows.append(import_row)

    import_df = pd.DataFrame(import_rows)
    return import_df


df1 = get_data_from_excel(files[0], sheet_nbr=1)
df2 = get_data_from_excel(files[1], sheet_nbr=1)
df3 = get_data_from_excel(files[2], sheet_nbr=1)
df4 = get_data_from_excel(files[3], sheet_nbr=1)
df5 = get_data_from_excel(files[4], sheet_nbr=1)
df11 = get_data_from_excel(files[-1], sheet_nbr=1)

df6 = get_data_from_excel("./data/raw/2071-072.xlsx", sheet_nbr=0, header_=0)
year6 = "2071/072"
df7 = get_data_from_excel("./data/raw/2074-075.xlsx", sheet_nbr=2, header_=2)
year7 = "2074/075"

df8 = get_data_from_excel("./data/raw/2072-073.xlsx", sheet_nbr=1, header_=1)
year8 = "2072/073"
df9 = get_data_from_excel("./data/raw/2073-074.xlsx", sheet_nbr=1, header_=1)
year9 = "2073/074"
df10 = get_data_from_excel("./data/raw/2075-076.xlsx", sheet_nbr=1, header_=1)
year10 = "2075/076"

year1 = files[0].split('.')[0].replace('-', '/')
year2 = files[1].split('.')[0].replace('-', '/')
year3 = files[2].split('.')[0].replace('-', '/')
year4 = files[3].split('.')[0].replace('-', '/')
year5 = files[4].split('.')[0].replace('-', '/')   
year11 = files[-1].split('.')[0].replace('-', '/') 

# Rearrange in chronological order
datalist = [df6, df8, df9, df7, df10, df1, df3, df4, df2, df5, df11]
yearlist = ["2071/072", "2072/073", "2073/074", "2074/075", "2075/076", 
           "2076/077", "2077/078", "2078/079", "2079/080", "2080/081", "2081/082"]

# Verify all years are properly represented
print("Years to process:", yearlist)

import_df = get_import_data_multi_year(datalist, yearlist)

# Create a new dataframe with properly ordered columns
imports = pd.DataFrame()

# Use the first description column for product names
descs = [col for col in import_df.columns if col.endswith('_desc')]
imports["Products"] = import_df[descs[0]].apply(lambda x: x.lower() if isinstance(x, str) else x)

# Add import/export columns in chronological order
for year in yearlist:
    if f"{year}_import" in import_df.columns:
        imports[f"{year}_import"] = import_df[f"{year}_import"]
    if f"{year}_export" in import_df.columns:
        imports[f"{year}_export"] = import_df[f"{year}_export"]

print(imports.head())
imports.to_excel("import_data.xlsx", index=False)



