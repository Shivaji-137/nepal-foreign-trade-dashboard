from utils import load_commodity_data, get_recent_previous_commodity_country
import streamlit as st
from visualization import top10_importCommodity_plot, import_commodity_comparision, plot_expimp_growth_by_year
import pandas as pd

def tab1_content(keys, key):
    if keys == "Import":
        select = st.selectbox(
                    'Select the top 10 product by',
                    options=[f"{keys} Value", "Quantity", f"{keys} Revenue"],
                    key=f"select_{keys}{key}item"
        )
    elif keys == "Export":
        select = st.selectbox(
                    'Select the top 10 product by',
                    options=[f"{keys} Value", "Quantity"],
                    key=f"select_{keys}{key}item"
        )

    unit_select = st.radio(
        'Select the unit of measurement',
        options=["All","Kilogram(Kg)", "Kilolitre(Kl)","Litre(LTR)", "Pieces(PCS)"],
        horizontal=True,
        help=f"Select the unit of measurement for the top 10 {keys}ed products",
        format_func=lambda x: x.split('(')[0],  # Display only the unit name
        key=f"unit_select{keys}{key}"
    )
    return select, unit_select

def tab2_content(products, commodity_data, keys, hasrevenue, recent_year):
    search_term = st.text_input('Search products', placeholder="Type to search product...", key=f"{keys}_input")
    value = f"{keys}s_Value"
    revenue = f"{keys}s_Revenue"

    if search_term:
        filtered_products = [product for product in products if search_term.lower() in product.lower()]

        if filtered_products:
            selected_product = st.selectbox("Select a product", filtered_products)
            
            if selected_product:
                # Filter data for the selected product
                product_data = commodity_data[commodity_data["Description"] == selected_product].reset_index(drop=True)
                
                previous_recent_yearinfo = get_recent_previous_commodity_country(product_data["Description"].values[0], recent_year)
                
                if previous_recent_yearinfo is not None:
                    fig, fig_ = plot_expimp_growth_by_year(previous_recent_yearinfo, keys)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(fig, use_container_width=True)
                    with col2:
                        st.plotly_chart(fig_, use_container_width=True)
                    # st.plotly_chart(fig)
                else:
                    st.write("No data of previous year is available ")
                # Get the data point
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
                    with col3:
                        st.metric(
                            label=f"{keys} Revenue (NPR)",
                            value=f"{product_info[revenue]*1000:,.0f}"
                        )
                    
                # Create tabs for different visualizations
                viz_tab1, viz_tab2 = st.tabs(["Comparative Analysis", "Detail View"])
                
                with viz_tab1:
                    # Calculate total imports for comparison
                    fig1, fig2 = import_commodity_comparision(selected_product, product_info, commodity_data, keys, hasrevenue)
                    st.plotly_chart(fig1, use_container_width=True)
                    st.plotly_chart(fig2, use_container_width=True)

                    
                with viz_tab2:
                    # Show the product details in a styled dataframe
                    st.write("### Product Details")
                    
                    # Create a more readable dataframe with better formatting
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
                    
                    # Display the raw data
                    st.write("### Raw Data")
                    if hasrevenue:
                        st.dataframe(
                            product_data.style.format({
                                'Imports_Value': '{:,.2f}',
                                'Quantity': '{:,.2f}',
                                'Imports_Revenue': '{:,.2f}'
                            }),
                            use_container_width=True
                        )
                    else:
                        st.dataframe(
                            product_data.style.format({
                                'Exports_Value': '{:,.2f}',
                                'Quantity': '{:,.2f}',
                            }),
                            use_container_width=True
                        )
                    # Calculate value per unit
                    if hasrevenue:
                        value_per_unit = (product_info["Imports_Value"]*1000) / product_info["Quantity"] if product_info["Quantity"] > 0 else 0
                        revenue_per_unit = (product_info["Imports_Revenue"]*1000) / product_info["Quantity"] if product_info["Quantity"] > 0 else 0
    
                        st.write("### Derived Metrics")
                        metrics_df = pd.DataFrame({
                            "Metric": ["Value per Unit", "Revenue per Unit", "Revenue Percentage"],
                            "Value": [
                                f"{value_per_unit:,.2f} NPR per {product_info['Unit']}",
                                f"{revenue_per_unit:,.2f} NPR per {product_info['Unit']}",
                                f"{(product_info['Imports_Revenue']/product_info['Imports_Value'])*100:.2f}%"
                            ]
                        })
                    
                        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        else:
            st.info("No products found matching your search term.")
    

def search_by_exportImport(keys):
    selected_year = st.selectbox(
            'Select Fiscal Year',
            options=["2081/082", "2080/081", "2079/080", "2078/079", "2077/078", "2076/077", "2075/076", "2074/075"],
            index=0,
            key=f"fiscal_year_select{keys}"
    )
    imp_data, exp_data  = load_commodity_data(selected_year)
    if keys == "Import":
        commodity1_data = imp_data
        products1 = [str(product) for product in commodity1_data["Description"].dropna().unique().tolist()]

        tab1, tab2 = st.tabs([f"View Top 10 {keys}ed Products", f"Search {keys}ed Product"])

        with tab1:
            select, unit_select = tab1_content(keys, "co")
            fig = top10_importCommodity_plot(commodity1_data, select, unit_select, keys, True)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            tab2_content(products1, commodity1_data, keys, True, selected_year)

    elif keys == "Export":
        commodity_data = exp_data
        products = [str(product) for product in commodity_data["Description"].dropna().unique().tolist()]

        tab1, tab2 = st.tabs([f"View Top 10 {keys}ed Products", f"Search {keys}ed Product"])

        with tab1:
            select, unit_select = tab1_content(keys, "cs")
            fig = top10_importCommodity_plot(commodity_data, select, unit_select, keys, False)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            tab2_content(products, commodity_data, keys, False, selected_year)
            
def export_by_commodity():
    search_by_exportImport("Export")

def import_by_commo():
    search_by_exportImport("Import")
   
