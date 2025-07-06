from utils import load_commodity_country_data, get_recent_previous_commodity
import streamlit as st
import pandas as pd
from visualization import top10_importCommodity_plot, plot_different_countries_with_same_product
from commodity_dashboard import tab1_content


def group_country_by_prod(countries, commodity_data, selected_year, keys, hasrevenue, key):
    st.write("Group the product by countries")
    search_country = st.text_input('Search Countries', placeholder="Type to enter countries", key=f"{keys}_{key}")
    value = f"{keys}s_Value"
    revenue = f"{keys}s_Revenue"

    if search_country:
        grouped_country = [country for country in countries if search_country.lower() in country.lower()]
        if grouped_country:
            selected_country = st.selectbox("Select a country", grouped_country, key=f"{keys}_country_{key}")
            
            if selected_country:
                selected_country_data = commodity_data.groupby("Partner Countries").get_group(selected_country).reset_index(drop=True)
                # Get the data point
                select, unitselect = tab1_content(keys, key)
                fig1 = top10_importCommodity_plot(selected_country_data, select, unitselect, keys, hasrevenue) 
                
                st.plotly_chart(fig1, use_container_width=True)

                tab2_content(selected_country_data["Description"].unique().tolist(), selected_country_data, selected_country, keys, hasrevenue, recent_year=selected_year)


                # st.dataframe(selected_country_data, use_container_width=True, hide_index=True)
                    

def tab2_content(products, commodity_data, selected_country, keys, hasrevenue, recent_year):
    st.subheader(f"Search a commodity to view its trade in {selected_country} and across different countries.")
    search_term = st.text_input('Search products', placeholder="Type to search product...", key=f"{keys}_input{keys}")
    value = f"{keys}s_Value"
    revenue = f"{keys}s_Revenue"

    if search_term:
        filtered_products = [product for product in products if search_term.lower() in str(product).lower()]

        if filtered_products:
            selected_product = st.selectbox("Select a product", filtered_products, key=keys)
            
            if selected_product:
                # Filter data for the selected product
                product_data = commodity_data[commodity_data["Description"] == selected_product].reset_index(drop=True)
                if not product_data.empty and "Description" in commodity_data.columns:
                    desc_value = str(product_data["Description"].values[0])
                    commodity_data['Description'] = commodity_data['Description'].astype(str)

                    product_data_withcou = commodity_data[commodity_data['Description']==desc_value].reset_index(drop=True)
                    st.write(f"### '{selected_product}' {keys} Details from {selected_country}")
                    product_info = product_data.iloc[0]
                    # Create columns for key metrics
                    col1, col2, col3 = st.columns(3)
                    
                    
                    # Display key metrics
                    with col1:
                        st.metric(
                            label=f"{keys} Value (NPR)",
                            value=f"{product_info[value]*1000:,.0f}"
                    )
                    
                    with col2:
                        st.metric(
                            label=f"Quantity ({product_info['Unit']})",
                            value=f"{product_info['Quantity']:,.0f}"
                        )

                

                    if hasrevenue:
                        detail_df = pd.DataFrame({
                            "Attribute": ["HS Code", "Description", "Unit", "Quantity", 
                                            "Import Value (NPR)", "Import Revenue (NPR)"],
                            "Value": [
                                product_info["HSCode"],
                                product_info["Description"],
                                product_info["Unit"],
                                f"{product_info['Quantity']:,.0f}",
                                f"{product_info['Imports_Value']*1000:,.0f}",
                                f"{product_info['Imports_Revenue']*1000:,.0f}"
                            ]
                        })
                    else:
                        detail_df = pd.DataFrame({
                            "Attribute": ["HS Code", "Description", "Unit", "Quantity", 
                                            "Export Value (NPR)"],
                            "Value": [
                                product_info["HSCode"],
                                product_info["Description"],
                                product_info["Unit"],
                                f"{product_info['Quantity']:,.0f}",
                                f"{product_info["Exports_Value"]*1000:,.0f}",
                            ]
                        })

                    
                    st.dataframe(detail_df, use_container_width=True, hide_index=True)
                else:
                    product_data_withcou = pd.DataFrame()
                # Get the data point

                import_data, export_data = get_recent_previous_commodity(product_data["Description"].values[0], recent_year, selected_country)
                fig, fig1 = plot_different_countries_with_same_product(import_data, export_data, selected_product)
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.plotly_chart(fig1, use_container_width=True)
                
                # st.dataframe(detail_df, use_container_width=True, hide_index=True)
    
                
        else:
            st.info("No products found matching your search term.")
    

def search_by_exportImport_country(keys, selected_year):
    imp_data, exp_data  = load_commodity_country_data(selected_year)
    if keys == "Import":
        commodity1_data = imp_data
        countries1 = [str(country) for country in commodity1_data["Partner Countries"].dropna().unique().tolist()]
        group_country_by_prod(countries1, commodity1_data, selected_year, keys, True, "imp")

    elif keys == "Export":
        commodity_data = exp_data
        countries = [str(country) for country in commodity_data["Partner Countries"].dropna().unique().tolist()]

        group_country_by_prod(countries, commodity_data, selected_year, keys, False, "exp")
            
def export_by_commodityCountry(selected_year):
    # search_by_exportImport("Export", selected_year)
    search_by_exportImport_country("Export", selected_year)

def import_by_commodityCountry(selected_year):
    # search_by_exportImport("Import", selected_year)
    search_by_exportImport_country("Import", selected_year)
   
