from utils import load_country_data, selectcountry_year_data
import streamlit as st
from visualization import hbarplot_top10countries, treeplot_top10countries
from visualization import search_product_plot, search_product_bar

def trade_countries_dashboard():
    countries_data = load_country_data()
    st.markdown(
            """
            <div style="
                background-color: #374151; 
                border-left: 6px solid #1f77b4; 
                padding: 15px 20px;  /* a bit more horizontal padding */
                border-radius: 5px;
                color: white;
                font-weight: 600;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15); /* slightly stronger shadow */
                font-family: 'Inter', sans-serif;
                line-height: 1.4;
                margin-bottom: 20px;
            ">
            <p style="font-size: 13px;">
            View the top 10 countries based on Nepal imports from, Nepal exports to, or trade balance for selected fiscal years.<br>
            You can also search for a specific country to see detailed trade trends: how much Nepal imported from or Nepal exported to and compare them using line or bar charts.<br>
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    tab1, tab2 = st.tabs(["View top 10 Trade Countries", "Search by Countries"])
    with tab1:
        yearSelected = st.selectbox(
            'Select fiscal year (BS)',
            ["2081/082", "2080/081", "2079/080", "2078/079", "2077/078", "2076/077", "2075/076", "2074/075","2073/074", "2072/073", "2071/072"],
            key='year select'
        )

        selected = st.selectbox(
            "Select the top 10 Trade Countries by",
            ["Import", "Export", "Trade Balance"], 
            key="top10_countries_select"
        )
        selectcountryyear_data = selectcountry_year_data(countries_data, yearSelected)

        fig1 = hbarplot_top10countries(selectcountryyear_data, selected, desc="Partner Countries")
        fig2 = treeplot_top10countries(selectcountryyear_data, selected)

        st.plotly_chart(fig1, use_container_width=True, key="1")
        st.plotly_chart(fig2, use_container_width=True, key="3")

        

    with tab2:
        countries = countries_data["Countries"].unique().tolist()
        
        # Add a search box with autocomplete
        search_term = st.text_input("Search for country", key="country_search")
        
        if search_term:
            # Filter products based on search term
            filtered_country = [country for country in countries if search_term.lower() in country.lower()]
            
            if filtered_country:
                selected_country = st.selectbox("Select a country", filtered_country)
                
                if selected_country:
                    # Filter data for the selected product
                    country_data = countries_data[countries_data["Countries"] == selected_country]
                    
                    chart_type = st.radio(
                        "Select chart type",
                        ("Line Trend", "Bar Chart"),
                        horizontal=True, key="countr_search"
                    )
                    if chart_type == "Line Trend":
                        fig = search_product_plot(country_data, selected_country)
                    else:
                        fig = search_product_bar(country_data, selected_country)
                
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(country_data)

            else:
                st.info("No country found matching your search term.")



    

