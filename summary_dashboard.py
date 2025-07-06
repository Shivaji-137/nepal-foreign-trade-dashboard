import streamlit as st
from utils import load_summary_data, load_growth_data
from visualization import show_description_chart, show_kpi_chart

def summary_chart():
     # Load and filter data
    summary_data = load_summary_data()
    growth_data = load_growth_data()
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
        This section provides a comprehensive analysis of Nepal's trade performance across different years. Here, you can filter data range by fiscal year and visualize trends. Key performance indicators (KPIs) shows trade performance of current fiscal year. Also, you can see definition of each term used in this dashbaord below. Explore the data to understand significant economic shifts over time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    
    start, end = st.select_slider(
        "Select Fiscal Year Range",
        options=summary_data.iloc[:, 0].tolist(),
        value=("2075/76", "2081/82"),
        key="fiscal_year_range_BS",
    )
    summary_data = summary_data[
        (summary_data.iloc[:, 0] >= start) &
        (summary_data.iloc[:, 0] <= end)
    ]
    growth_data = growth_data[
        (growth_data.iloc[:, 0] >= start) &
        (growth_data.iloc[:, 0] <= end)
    ]

    # Inject KPI card CSS
    st.markdown("""
    <style>
    .metric-container {
        display: flex;
        height: 5rem;
        width: 100%;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border-radius: 0.8rem;
        color: #31333F;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-content { display: flex; align-items: center; }
    .metric-icon { font-size: 2.0rem; margin-right: 0.75rem; line-height: 1; }
    .metric-text { display: flex; flex-direction: column; }
    .metric-label { font-size: 1rem; font-weight: 600; text-transform: uppercase; }
    .metric-value { font-size: 1.75rem; font-weight: 700; }
    .metric-delta { font-size: 1.1rem; font-weight: 600; display: flex; align-items: center; }
    .metric-white { background-color: #2ECC71; }
    .metric-green { background-color: #3498DB; }
    .metric-red   { background-color: #DF6557; }
    .metric-pink  { background-color: #F8A4D5; color: #31333F; }
    </style>
    """, unsafe_allow_html=True)

    # Side-by-side layout: chart on left, KPI cards on right
    col1, col2 = st.columns((3, 1))
    with col1:
        nepali_engyr = st.radio(
            "",
            ("BS", "AD"),
            horizontal=True,
            key="fiscal_year_format"
        )
        fig1 = show_description_chart(growth_data, summary_data, nepali_engyr)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(
        "<p style='font-size:0.75rem; color:#555;'>"
        "Note: The growth rate data of fiscal year 2071/72 is not available, hence it is set to 0%."
        "</p>",
        unsafe_allow_html=True)

    with col2:
        st.subheader("KPI: First 11 month of Fiscal Year (2081/82) in comparison with previous year")
        kpi_cards = show_kpi_chart(summary_data, growth_data)
        for idx, card in enumerate(kpi_cards):
            icon   = [ "📥", "📤"," 📉",  "⚖️"][idx]
            bg_cls = ["metric-white", "metric-green", "metric-red", "metric-pink"][idx]
            st.markdown(f"""
            <div class="metric-container {bg_cls}">
              <div class="metric-content">
                <div class="metric-icon">{icon}</div>
                <div class="metric-text">
                  <div class="metric-label">{card['label']}</div>
                  <div class="metric-value">{card['value']}</div>
                </div>
              </div>
              <div class="metric-delta" style="color: {card['delta_color']}">
                {card['delta']}
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

   # st.subheader("Trade Summary Data")
    #cols1, cols2 = st.columns((1, 1))
    #with cols1:
     #   st.dataframe(summary_data, use_container_width=True)
    #with cols2:
        #st.dataframe(growth_data, use_container_width=True)

    

    metric_definitions = {
        "Imports": {
            "points": [
                "Total value of goods/services bought from abroad.",
                "Reflects domestic demand and local production gaps.",
                "High imports can widen a trade deficit if not offset by exports.",
            ],
            "link": "https://en.wikipedia.org/wiki/Import"
        },
        "Exports": {
            "points": [
                "Total value of goods/services sold to foreign markets.",
                "Indicative of global competitiveness & production capacity.",
                "Growth in exports is generally positive for GDP and currency strength.",
            ],
            "link": "https://en.wikipedia.org/wiki/Export"
        },
        "Trade Deficit": {
            "points": [
                "Difference between imports and exports (Imports – Exports).",
                "A positive value indicates more imports than exports (net outflow).",
                "Financed via foreign borrowing or investment; sustained deficits may weaken currency.",
            ],
            "link": "https://en.wikipedia.org/wiki/Trade_deficit"
        },
        "Trade Balance": {
            "points": [
                "The difference between a country's total exports and total imports over a specific period.",
                "Calculated as Exports – Imports.",
                "A positive trade balance (trade surplus) means exports exceed imports; a negative balance (trade deficit) means imports exceed exports.",
                "It is a major component of a country's current account in the balance of payments."
            ],
            "link": "https://en.wikipedia.org/wiki/Balance_of_trade"
        },
        
        "Total Trade": {
            "points": [
                "Sum of imports and exports.",
                "Overall scale of a country’s engagement in international trade.",
                "Useful to compare trade volume vs peers or over time.",
            ],
            "link": "https://en.wikipedia.org/wiki/Balance_of_trade#Total_trade"
        },
        "Import/Export Ratio": {
            "points": [
                "Ratio = Imports / Exports.",
                "Shows reliance on foreign goods relative to export earnings.",
                "A rising ratio can signal growing dependency on imports.",
            ],
            "link": "https://www.tradeatlas.com/en/blog/the-ratio-of-exports-to-imports"
        }
    }

    # Professional Trade Metrics Reference Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0; border: 1px solid #e5e7eb;">
        <h3 style="color: #1e40af; margin: 0 0 1rem 0; font-size: 1.4rem; font-weight: 600;">
            📊 Trade Metrics Reference Guide
        </h3>
        <p style="color: #64748b; margin: 0; line-height: 1.6;">
            Understanding key trade indicators and their economic implications for Nepal's international commerce.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced metric selector
    selected = st.selectbox(
        "� Select Trade Metric for Detailed Analysis",
        list(metric_definitions.keys()),
        key="metric_selector",
        help="Choose a trade metric to view comprehensive definition, calculation method, and economic significance"
    )
    
    # Professional metric display
    metric_info = metric_definitions[selected]
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(147, 197, 253, 0.02) 100%); 
                border-left: 4px solid #3b82f6; padding: 1.5rem; margin: 1rem 0; border-radius: 0 10px 10px 0;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);">
        <h4 style="color: #1e40af; margin: 0 0 1rem 0; font-size: 1.3rem; font-weight: 600;">
            📋 {selected} - Comprehensive Overview
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed points with professional styling
    for i, bullet in enumerate(metric_info["points"], 1):
        st.markdown(f"""
        <div style="background: #374151; border-left: 3px solid #10b981; padding: 0.8rem 1.2rem; 
                    margin: 0.5rem 0; border-radius: 0 6px 6px 0;">
            <p style="margin: 0; color: white; font-weight: 500; line-height: 1.6;">
                <span style="color: white; font-weight: 600;">{i}.</span> {bullet}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional reference link
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 1rem; 
                border-radius: 8px; margin: 1rem 0; border: 1px solid #fbbf24;">
        <p style="margin: 0; color: #92400e; font-weight: 500;">
            📚 <strong>Additional Resources:</strong> 
            <a href="{metric_info['link']}" target="_blank" style="color: #dc2626; text-decoration: none; font-weight: 600;">
                Learn more about {selected} →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    
