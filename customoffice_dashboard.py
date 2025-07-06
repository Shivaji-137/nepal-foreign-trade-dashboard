from utils import load_custom_office_data, selectcustom_year_data
import streamlit as st
from visualization import hbarplot_top10countries
from visualization import search_product_plot, search_product_bar

def trade_customoffice_dashboard():
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
            View the top 10 custom offices in Nepal based on import, export, or trade balance for selected fiscal years.<br>
            You can also search for a specific custom office to see detailed trade trends and compare them using line or bar charts.<br>
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    customoffice_data = load_custom_office_data()

    tab1, tab2 = st.tabs(["View top 10 Custom Offices", "Search by Custom Offices"])
    with tab1:
        yearSelected = st.selectbox(
            'Select fiscal year (BS)',
            ["2081/082","2080/081", "2079/080", "2078/079", "2077/078", "2076/077", "2075/076", "2074/075","2073/074", "2072/073"],
            key='year_selectcustom'
        )

        selected = st.selectbox(
            "Select the top 10 Custom Offices by",
            ["Import", "Export", "Trade Balance"], 
            key="top10_custom_offices_select"
        )
        selectcustomyear_data = selectcustom_year_data(customoffice_data, yearSelected)

        fig1 = hbarplot_top10countries(selectcustomyear_data, selected, desc="Custom_Offices")

        st.plotly_chart(fig1, use_container_width=True, key="custom1")

        

    with tab2:
        offices = customoffice_data["Custom_offices"].unique().tolist()
        
        # Add a search box with autocomplete
        search_term = st.text_input("Search for custom office", key="custom_search")
        
        if search_term:
            # Filter products based on search term
            filtered_office = [office for office in offices if search_term.lower() in office.lower()]
            
            if filtered_office:
                selected_office = st.selectbox("Select a country", filtered_office, key="custom_search_select")
                
                if selected_office:
                    # Filter data for the selected product
                    office_data = customoffice_data[customoffice_data["Custom_offices"] == selected_office]
                    
                    chart_type = st.radio(
                        "Select chart type",
                        ("Line Trend", "Bar Chart"),
                        horizontal=True, key="custom_search_chart_type"
                    )
                    if chart_type == "Line Trend":
                        fig = search_product_plot(office_data, selected_office, "custom")
                    else:
                        fig = search_product_bar(office_data, selected_office, "custom")
                
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(office_data)

            else:
                st.info("No custom office found matching your search term.")



    

