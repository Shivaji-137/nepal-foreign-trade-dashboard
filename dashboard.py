import streamlit as st
from summary_dashboard import summary_chart
from product_dashboard import trade_product_dashboard
from countries_dashboard import trade_countries_dashboard
from commodity_dashboard import import_by_commo, export_by_commodity
from customoffice_dashboard import trade_customoffice_dashboard
from commoditywithcountry import export_by_commodityCountry, import_by_commodityCountry

# Page configuration
st.set_page_config(
    page_title="Nepal Foreign Trade",
    page_icon="🇳🇵⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Government Dashboard CSS Styling
st.markdown("""
<style>
    /* Import Google Fonts for professional appearance */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-blue: #1e40af;
        --secondary-blue: #3b82f6;
        --accent-blue: #06b6d4;
        --nepal-red: #dc143c;
        --nepal-blue: #003893;
        --success-green: #059669;
        --warning-orange: #ea580c;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-600: #4b5563;
        --gray-800: #1f2937;
    }
    
    /* Main application styling */
    .main .block-container {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    /* Enhanced header with Nepal government theme */
    .main-header {
        background: linear-gradient(135deg, var(--nepal-blue) 0%, var(--primary-blue) 50%, var(--accent-blue) 100%);
        padding: 2.5rem 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15), 0 4px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.4);
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: #e0f2fe;
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        font-weight: 400;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    }
    
    /* Professional tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
        padding: 0.75rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        padding: 0px 24px;
        /* replaced white with light gray for tab backgrounds */
        /* use subtle gray gradient instead of near-white */
        background: linear-gradient(135deg, rgba(243, 244, 246, 0.5) 0%, rgba(243, 244, 246, 0.8) 100%);
        border-radius: 10px;
        color: var(--gray-600);
        font-weight: 600;
        border: 1px solid #e5e7eb;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        border-color: var(--secondary-blue);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--secondary-blue) 0%, var(--primary-blue) 100%);
        color: white !important;
        border-color: var(--secondary-blue);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4), 0 2px 5px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    /* Enhanced description boxes with gradients */
    .description-box {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(147, 197, 253, 0.05) 100%);
        border-left: 5px solid var(--secondary-blue);
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        border-radius: 0 12px 12px 0;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1), 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(59, 130, 246, 0.1);
        border-left: 5px solid var(--secondary-blue);
    }
    
    .description-box h3 {
        color: var(--primary-blue);
        margin: 0 0 0.5rem 0;
        font-size: 1.25rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    .description-box p {
        color: var(--gray-600);
        margin: 0;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Professional feature highlights */
    .feature-highlight {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(6, 182, 212, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 1.25rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(16, 185, 129, 0.1);
    }
    
    /* Government-style metric cards */
    .metric-card {
        /* Replaced white gradient with light blue gradient for better contrast */
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15), 0 4px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
    }
    
    /* Professional status badges */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-left: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .status-active {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #166534;
        border: 1px solid #bbf7d0;
    }
    
    .status-development {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border: 1px solid #fde68a;
    }
    
    /* Professional welcome section */
    .welcome-section {
        /* replaced white/light gray gradient with softer gray gradient */
        background: linear-gradient(135deg, var(--gray-100) 0%, var(--gray-50) 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(59, 130, 246, 0.1);
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08), 0 3px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Government terminology section */
    .terminology-section {
        background: linear-gradient(135deg, rgba(220, 252, 231, 0.3) 0%, rgba(187, 247, 208, 0.2) 100%);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.1);
    }
    
    .term-card {
        /* replaced white gradient with subtle gray gradient for consistency */
        background: linear-gradient(135deg, var(--light-gray) 0%, #f9fafb 100%);
        border-left: 4px solid var(--success-green);
        padding: 1rem 1.5rem;
        margin: 0.75rem 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    
    /* Professional footer */
    .footer-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        text-align: center;
        padding: 2.5rem 1rem;
        border-radius: 15px;
        margin-top: 3rem;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Government Dashboard Header with Nepal Theme
st.markdown("""
<div class="main-header">
    <h1>🇳🇵 नेपाल विदेशी व्यापार ड्यासबोर्ड</h1>
    <h2 style="color: #e0f2fe; font-size: 1.8rem; margin: 0.5rem 0; font-weight: 500;">Nepal Foreign Trade Analytics Dashboard</h2>
    <p style="font-size: 1.3rem; margin-top: 0.5rem;">Comprehensive Analysis of Nepal's International Trade Data (FY 2071/72 - 2081/82 BS)</p>
    <p style="font-size: 1rem; margin-top: 0.8rem;">This dashboard shows Nepal’s foreign trade from fiscal year 2071/72 to first 11 month of 2081/82 (Bikram Sambat). It explains how much Nepal imported and exported each year, the difference between them (trade balance), and changes in major products. The charts and summaries help understand how Nepal’s trade has changed over time.</p>
</div>
""", unsafe_allow_html=True)





# Navigation tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Trade Balance Summary",
    "📦 Trade by Products", 
    "🌍 Trade by Countries",
    "🏭 Trade by Commodities",
    "🏛️ Trade by Custom Offices",
    "🔗 Commodity-Country Analysis",
])

with tab1:
    summary_chart()
   
with tab2:
    trade_product_dashboard()

with tab3:
    trade_countries_dashboard()

with tab4:
    st.markdown(
        """
        <div style="
            background-color: #374151; 
            border-left: 6px solid #1f77b4; 
            padding: 15px; 
            border-radius: 5px;
            color: white;
            font-weight: 600;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            font-family: 'Inter', sans-serif;
        ">
        <p style="font-size: 13px;">
        Explores Nepal’s international trade in specific commodities.  
        View the top 10 imported/exported commodities by value, quantity, or revenue, and analyze year-wise growth.  
        Also search for a commodity to compare its trade across previous years and view detailed metrics, including per-unit value and revenue share.
        <br>Bar chart in search part shows the import and export value of products for previous year(last year) and recent year according to the year selected. <span>* Products option shows the list of the recent selected year and the selected product may not match with that of the previous year, differed by capital letter or space character or any other unavailable characters. Thus, import and export bar graph may not shown or be blank in previous year</span></br>
        </p>
        
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("**Switch between Import and Export analysis:**")
    
    trade_type = st.selectbox(
        '🔄 Trade Type',
        ['Imports By Commodities', 'Exports By Commodities'],
        key='trade_type_select'
    )
    
    if trade_type == 'Imports By Commodities':
        import_by_commo()
    elif trade_type == 'Exports By Commodities':
        export_by_commodity()

with tab5:

    trade_customoffice_dashboard()

with tab6:
    # Year selection
    st.markdown(
        """
        <div style="
            background-color: #374151; 
            border-left: 6px solid #1f77b4; 
            padding: 15px; 
            border-radius: 5px;
            color: white;
            font-weight: 600;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            font-family: 'Inter', sans-serif;
            ">
            <p style="font-size: 13px;">
            Search a country to see its top 10 traded commodities with details like quantity, import and export value.<br>
            Also search a commodity to view its trade across different countries.<br>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    yearSelected = st.selectbox('� Select fiscal year (Bikram Sambat)', ["2081/082","2080/081", "2079/080", "2078/079", "2077/078", "2076/077"], key='year_selectPartner')
    
    # Sub-tabs
    imprtab, epxrtab = st.tabs(["📥 Import Analysis", "📤 Export Analysis"])
    
    with imprtab:
        import_by_commodityCountry(yearSelected)
    
    with epxrtab:
        export_by_commodityCountry(yearSelected)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1.5rem; background: #374151; border-radius: 10px; margin-top: 2rem;">
    <p style="color: white; margin: 0;">
        Data Source: Department of Customs, Ministry of Finance, Government of Nepal<br>
        <small>FY 2071/72 - 2081/82 (BS) | Updated July 2025</small>
    </p>
</div>
""", unsafe_allow_html=True)


# Add a footer
st.markdown("""
    <hr>
    <div style="text-align: center;">
        <small>&copy; 2025 Shivaji Chaulagain. All rights reserved.</small>
    </div>
""", unsafe_allow_html=True)














