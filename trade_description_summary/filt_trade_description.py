import pandas as pd
import os

directory = os.path.dirname("./data/raw/")

# files is for 11 months of 81/82 fiscal year
files = ['2081-082.xlsx','2076-077.xlsx', '2079-080.xlsx', '2077-078.xlsx', '2075-076.xlsx', '2078-079.xlsx', '2073-074.xlsx', '2074-075.xlsx', '2080-081.xlsx', '2072-073.xlsx']
# files_ = [os.path.join(directory, file) for file in files]


data = [["2071/72", "786,191,403", "85,194,754", "-700,996,649", "871,386,157", "9.23", "9.78", "90.22"]]  # Initial row for fiscal year 2071/72

changeperc_data = [["2071/72", "0", "0", "0", "0", "0", "0", "0"]]  # Initial row for percentage change in fiscal year 2071/72

df_col = ["Fiscal Year", "Imports (Rs.in `000)", "Exports (Rs.in `000)", "Trade Deficit (Rs.in `000)", "Total Foreign Trade (Rs.in `000)", "Imports/Exports Ratio (Rs.in `000)", "Exports share to total trade(%)", "Imports share to total trade(%)" ]
for file in files:
    fiscal_year = file.split(".")[0].split("-")  # Extract fiscal year from filename
    # fiscal_year = fiscal_year.split("-")
    next_yr = int(fiscal_year[1])
    fiscal_year = fiscal_year[0] + "/" + str(next_yr)
    print(fiscal_year)
    file = os.path.join(directory, file)

    ftd = pd.read_excel(file, sheet_name=0, header=2)
    ftd = ftd[:7]

    # each year has data of recent year in different position. we only choose the recent year according to year contains in column
    
    if ftd.columns[1].startswith("Imports"):
        ftd_ = pd.read_excel(file, sheet_name=0, header=1)
        cols = [col for col in ftd_.columns if fiscal_year in col]
        print(cols)

        ftd_ = ftd_[:7]
        ftds_ = ftd_[cols]

        try:
            dat = [fiscal_year]
            per_dat = [fiscal_year]
            for i in range(ftds_.shape[0]):
                dat.append(ftds_.iloc[i,0])
                per_dat.append(ftd_.iloc[i,4])

            data.append(dat)
            changeperc_data.append(per_dat)

        except KeyError:
            print("error")

    else:
        cols = [col for col in ftd.columns if fiscal_year in col]
        ftds = ftd[cols]
        print(cols)
        dat = [fiscal_year]
        per_dat = [fiscal_year]
        for i in range(ftd.shape[0]):
            dat.append(ftds.iloc[i,0])
            per_dat.append(ftd.iloc[i,4])
        data.append(dat)
        changeperc_data.append(per_dat)
        

def convert_to_numeric(value):
    if pd.isna(value):
        return value
    if isinstance(value, str):
        # Remove commas if present
        cleaned_value = value.replace(',', '')
        try:
            return cleaned_value
        except ValueError:
            return value
    return value

df = pd.DataFrame(data, columns=df_col).sort_values(by=["Fiscal Year"]).reset_index(drop=True)
for col in df.columns:
    df[col] = df[col].apply(convert_to_numeric)


df.to_excel("trade_2071_082.xlsx", sheet_name="foreign Trade description", index=False)
per_df = pd.DataFrame(changeperc_data, columns=df_col).sort_values(by=["Fiscal Year"]).reset_index(drop=True)
per_df.to_excel("trad_Percechange2072_to_82.xlsx", sheet_name="Foreign Trade description", index=False)
# print(df)
