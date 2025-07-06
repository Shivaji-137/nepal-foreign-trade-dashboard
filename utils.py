import pandas as pd
import streamlit as st

#.............................loading data ................................
@st.cache_data
def load_summary_data():
    data = "./data/filtered_data/trade_2071_082.xlsx"
    dat = pd.read_excel(data)
    return dat

@st.cache_data
def load_growth_data():
    data = "./data/filtered_data/trad_Percechange2072_to_82.xlsx"
    dat = pd.read_excel(data)
    return dat

@st.cache_data
def load_product_data():
    data = "./data/filtered_data/impexp_Productdata.xlsx"
    dat = pd.read_excel(data)
    return dat

@st.cache_data
def load_country_data():
    data = "./data/filtered_data/impexp_countrydata.xlsx"
    dat = pd.read_excel(data)
    return dat

@st.cache_data
def load_commodity_data(selected_year):
    year = selected_year.replace("/", "-")
    data = f"./data/raw/{year}.xlsx"
    imp_dat = pd.read_excel(data, sheet_name="5_Imports_By_Commodity", header=2)
    exp_dat = pd.read_excel(data, sheet_name="7_Exports_By_Commodity", header=2)
    return imp_dat, exp_dat

@st.cache_data
def load_custom_office_data():
    data = "./data/filtered_data/customoffice_trade_allyr.xlsx"
    dat = pd.read_excel(data)
    return dat

@st.cache_data
def load_commodity_country_data(selected_year):
    year = selected_year.replace("/", "-")
    data = f"./data/raw/{year}.xlsx"
    imp_dat = pd.read_excel(data, sheet_name="4_Imports_By_Commodity_Partner", header=2)
    exp_dat = pd.read_excel(data, sheet_name="6_Exports_By_Commodity_Partner", header=2)
    return imp_dat, exp_dat


#............................preparing data ................................

def prepare_search_data(product_data, keys=None):
    # Extract fiscal years from column names
    fiscal_years = []
    import_values = []
    export_values = []
    total_trade = []
    trade_balance = []
    imports_share = []
    exports_share = []

    if keys == "custom":
        columns = product_data.columns
        fiscal_years_set = set()
        for col in columns:
            if '_import' in col or '_export' or '_import_share' or '_export_share' in col:
                fiscal_year = col.split('_')[0]
                fiscal_years_set.add(fiscal_year)
        
        fiscal_years_list = sorted(list(fiscal_years_set))
        
        # Extract values for each fiscal year
        for year in fiscal_years_list:
            import_col = f"{year}_import"
            export_col = f"{year}_export"
            import_share_col = f"{year}_import_share"
            export_share_col = f"{year}_export_share"
            
            if import_col in columns and export_col and import_share_col and export_share_col in columns:
                import_val = product_data[import_col].values[0]*1000
                export_val = product_data[export_col].values[0]*1000
                import_share_val = product_data[import_share_col].values[0]
                export_share_val = product_data[export_share_col].values[0]
                
                fiscal_years.append(year)
                import_values.append(import_val)
                export_values.append(export_val)
                imports_share.append(import_share_val)
                exports_share.append(export_share_val)
        return fiscal_years, import_values, export_values, imports_share, exports_share
    
    else:
        columns = product_data.columns
        fiscal_years_set = set()
        for col in columns:
            if '_import' in col or '_export' in col:
                fiscal_year = col.split('_')[0]
                fiscal_years_set.add(fiscal_year)
        
        fiscal_years_list = sorted(list(fiscal_years_set))
        
        # Extract values for each fiscal year
        for year in fiscal_years_list:
            import_col = f"{year}_import"
            export_col = f"{year}_export"
            
            if import_col in columns and export_col in columns:
                import_val = product_data[import_col].values[0]*1000
                export_val = product_data[export_col].values[0]*1000
                
                fiscal_years.append(year)
                import_values.append(import_val)
                export_values.append(export_val)
                total_trade.append(import_val + export_val)

                trade_balance.append(export_val - import_val)
                
        return fiscal_years, import_values, export_values, total_trade, trade_balance



def format_value(n):
    """
    Format a number to a string in billions (B) or millions (M).
    Examples:
        2500000000 -> "2.50B"
        7500000    -> "7.50M"
        12345      -> "12,345"
    """
    abs_n = abs(n)
    if abs_n >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    elif abs_n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    else:
        # fallback to comma‐separated integer
        return f"{n:,}"
    
def selectcountry_year_data(data, yearSelected):
    countries = data["Countries"].unique().tolist()
    import_values = data[f"{yearSelected}_import"].tolist()
    export_values = data[f"{yearSelected}_export"].tolist()
    trade_balance = [export - import_val for export, import_val in zip(export_values, import_values)]
    year_data = pd.DataFrame({
        "Partner Countries": countries,
        "Imports_Value": import_values,
        "Exports_Value": export_values,
        "Trade_Balance": trade_balance
    })
    return year_data

def selectproduct_year_data(data, yearSelected):
    products = data["Products"].unique().tolist()
    import_values = data[f"{yearSelected}_import"].tolist()
    export_values = data[f"{yearSelected}_export"].tolist()
    trade_balance = [export - import_val for export, import_val in zip(export_values, import_values)]
    year_data = pd.DataFrame({
        "Description": products,
        "Imports_Value": import_values,
        "Exports_Value": export_values,
        "Trade_Balance": trade_balance
    })
    return year_data

def selectcustom_year_data(data, yearSelected):
    custom_offices = data["Custom_offices"].unique().tolist()
    import_values = data[f"{yearSelected}_import"].tolist()
    export_values = data[f"{yearSelected}_export"].tolist()
    import_share_values = data[f"{yearSelected}_import_share"].tolist()
    export_share_values = data[f"{yearSelected}_export_share"].tolist()
    
    trade_balance = [export - import_val for export, import_val in zip(export_values, import_values)]

    year_data = pd.DataFrame({
        "Custom_Offices": custom_offices,
        "Imports_Value": import_values,
        "Imports_Share": import_share_values,
        "Exports_Value": export_values,
        "Exports_Share": export_share_values,
        "Trade_Balance": trade_balance
    })
    return year_data


def jaccard_similarity(words1, words2):
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union if union != 0 else 0

def get_recent_previous_data(product, recent_year, previous_year, recent_imp_data, recent_exp_data, previous_imp_data, previous_exp_data):
    recent_imp_inof = recent_imp_data[recent_imp_data["Description"] == product]
    recent_exp_inof = recent_exp_data[recent_exp_data["Description"] == product]
    previous_imp_inof = previous_imp_data[previous_imp_data["Description"] == product]
    previous_exp_inof = previous_exp_data[previous_exp_data["Description"] == product]
    units = recent_imp_inof["Unit"].iloc[0] if not recent_imp_inof.empty else "N/A"
    recent_imp_quantity = recent_imp_inof["Quantity"].sum() if not recent_imp_inof.empty else 0
    recent_exp_quantity = recent_exp_inof["Quantity"].sum() if not recent_exp_inof.empty else 0
    previous_imp_quantity = previous_imp_inof["Quantity"].sum() if not previous_imp_inof.empty else 0
    previous_exp_quantity = previous_exp_inof["Quantity"].sum() if not previous_exp_inof.empty else 0
    recent_import_value = recent_imp_inof["Imports_Value"].sum() if not recent_imp_inof.empty else 0
    recent_export_value = recent_exp_inof["Exports_Value"].sum() if not recent_exp_inof.empty else 0
    previous_import_value = previous_imp_inof["Imports_Value"].sum() if not previous_imp_inof.empty else 0
    previous_export_value = previous_exp_inof["Exports_Value"].sum() if not previous_exp_inof.empty else 0
    return {
        f"{recent_year}":{
            "import_value": recent_import_value,
            "export_value": recent_export_value,
            "imp_quantity": recent_imp_quantity,
            "exp_quantity": recent_exp_quantity,
            "unit": units
        },
        f"{previous_year}":{
            "import_value": previous_import_value,
            "export_value": previous_export_value,
            "imp_quantity": previous_imp_quantity,
            "exp_quantity": previous_exp_quantity,
        }   
    }

def get_recent_previous_commodity_country(product, year):
    recent_year = year
    previous_year = str(int(year.split("/")[0]) - 1) + "/" + "0"+str(+int(year.split("/")[1]) - 1)
    yr = ["2077/078", "2078/079", "2079/080", "2080/081", "2081/082"]
    if year in yr:
        recent_imp_data, recent_exp_data = load_commodity_country_data(recent_year)
        previous_imp_data, previous_exp_data = load_commodity_country_data(previous_year)
        required_imp_exp_info = get_recent_previous_data(product, recent_year, previous_year, recent_imp_data, recent_exp_data, previous_imp_data, previous_exp_data)
        return required_imp_exp_info
    else:
        print("Features not available after 2076/77. Please select another year.")
    
def get_recent_data(selected_country, product, recent_imp_data, recent_exp_data):
    recent_imp_inof = recent_imp_data[recent_imp_data["Description"] == product]
    recent_exp_inof = recent_exp_data[recent_exp_data["Description"] == product]
    return recent_imp_inof, recent_exp_inof


def get_recent_previous_commodity(product, year, selected_country):
    recent_year = year
    previous_year = str(int(year.split("/")[0]) - 1) + "/" + "0"+str(+int(year.split("/")[1]) - 1)
    if year != "2076/077":
        recent_imp_data, recent_exp_data = load_commodity_country_data(recent_year)
        required_imp_info, required_exp_info = get_recent_data(selected_country, product, recent_imp_data, recent_exp_data)
        return required_imp_info, required_exp_info
    else:
        st.warning("Features not available after 2076/77")
    

