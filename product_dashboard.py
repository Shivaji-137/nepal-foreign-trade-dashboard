from utils import load_product_data, selectproduct_year_data
import streamlit as st
from visualization import hbarplot_top10product, treeplot_top10product
from visualization import search_product_plot, search_product_bar

def trade_product_dashboard():
    products_data = load_product_data()
    st.markdown(
    """
    <div style="
        background-color: #374151; 
        border-left: 6px solid #1f77b4; 
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
        font-family: 'Inter', sans-serif;
        line-height: 1.4;
        margin-bottom: 20px;
    ">
    <p style="font-size: 13px;">
    Explore Nepal’s top 10 traded products based on import, export, or trade balance for a selected fiscal year.<br>
    Visualize the data using treemaps, bar charts, and scatter plots to understand key trade contributors.<br>
    You can also search for any product to view its detailed trade trends over time through interactive line or bar charts.<br>
    </p>
    </div>
    """,
    unsafe_allow_html=True
)


    tab1, tab2 = st.tabs(["View top 10 Products", "Search by Product"])
    with tab1:
        yearSelected = st.selectbox(
            'Select fiscal year (BS)',
            ["2081/082", "2080/081", "2079/080", "2078/079", "2077/078", "2076/077", "2075/076", "2074/075","2073/074"],
            key='country_yearselect'
        )

        selected = st.selectbox(
            "select the top 10 product by",
            ["Import", "Export","Trade Balance"]
        )
        
        selectproductyear_data = selectproduct_year_data(products_data, yearSelected)

        fig1 = hbarplot_top10product(selectproductyear_data, selected) 
        fig2 = treeplot_top10product(selectproductyear_data, selected)
        
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig1, use_container_width=True)
        
    with tab2:
        products = products_data["Products"].unique().tolist()
        
        # Add a search box with autocomplete
        search_term = st.text_input("Search for products", key="product_search")
        
        if search_term:
            # Filter products based on search term
            filtered_products = [product for product in products if search_term.lower() in product.lower()]
            
            if filtered_products:
                selected_product = st.selectbox("Select a product", filtered_products)
                
                if selected_product:
                    # Filter data for the selected product
                    product_data = products_data[products_data["Products"] == selected_product]
                    
                    chart_type = st.radio(
                        "Select chart type",
                        ("Line Trend", "Bar Chart"),
                        horizontal=True,
                    )
                    if chart_type == "Line Trend":
                        fig = search_product_plot(product_data, selected_product)
                    else:
                        fig = search_product_bar(product_data, selected_product)
                
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(product_data)

            else:
                st.info("No products found matching your search term.")



    

