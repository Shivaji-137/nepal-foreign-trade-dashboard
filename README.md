# Nepal Foreign Trade Analytics Dashboard 🇳🇵

A comprehensive Streamlit-based analytics dashboard for visualizing and analyzing Nepal's international trade data from fiscal year 2071/72 to 2081/82 (Bikram Sambat).

## 📊 Overview

This dashboard provides in-depth analysis of Nepal's foreign trade patterns, including imports, exports, trade balance, and growth trends. It features interactive visualizations, detailed metric definitions, and multi-dimensional analysis capabilities.

## 🚀 Features

- **Comprehensive Trade Analytics** - Complete analysis of Nepal's trade performance over 11+ years
- **Interactive Visualizations** - Dynamic charts using Plotly (bar charts, treemaps, line charts, scatter plots)
- **Multi-dimensional Analysis** - Time series, top 10 rankings, growth calculations, and KPI monitoring
- **Professional Dashboard Design** - Nepal government theme with responsive layout
- **Bilingual Support** - Nepali BS and English AD fiscal year formats
- **Search Functionality** - Find specific products, countries, and custom offices
- **Educational Component** - Detailed metric definitions with external references

## 📁 Project Structure

### Core Dashboard Files

| File | Description |
|------|-------------|
| `dashboard.py` | Main entry point with professional styling and 6 navigation tabs |
| `summary_dashboard.py` | Trade balance summary with KPIs and metric definitions |
| `product_dashboard.py` | Top 10 products analysis and product search functionality |
| `countries_dashboard.py` | Trade partner countries analysis and country-specific insights |
| `commodity_dashboard.py` | Detailed commodity import/export analysis with filtering |
| `customoffice_dashboard.py` | Custom offices trade analysis and performance metrics |
| `commoditywithcountry.py` | Commodity-country relationship analysis and cross-referencing |

### Utility Files

| File | Description |
|------|-------------|
| `utils.py` | Data loading, processing, formatting, and utility functions |
| `visualization.py` | Plotly chart generation functions and visualization utilities |

### Data Organization

```
data/
├── raw/                          # Original Excel files by fiscal year
│   ├── 2071-072.xlsx            # FY 2071/72 raw trade data
│   ├── 2072-073.xlsx            # FY 2072/73 raw trade data
│   └── ... (through 2081-082.xlsx)
└── filtered_data/               # Processed and aggregated data
    ├── trade_2071_082.xlsx      # Main trade summary data
    ├── trad_Percechange2072_to_82.xlsx  # Growth rate calculations
    ├── impexp_Productdata.xlsx  # Product-wise trade data
    ├── impexp_countrydata.xlsx  # Country-wise trade data
    └── customoffice_trade_allyr.xlsx    # Custom office data
```

### Specialized Analysis Folders

These folders contain data processing scripts that analyze raw trade data and generate filtered datasets saved to the `filtered_data/` folder:

| Folder | Description | Output to filtered_data/ |
|--------|-------------|---------------------------|
| `trade_balance_by_chapter/` | Chapter-wise trade balance analysis scripts | Chapter-classified trade data |
| `trade_by_commodity&countries/` | Commodity-country cross-analysis tools | `impexp_countrydata.xlsx` |
| `trade_by_countries/` | Country-specific trade analysis utilities | Country-aggregated trade statistics |
| `trade_description_summary/` | Trade description processing and summarization | `trade_2071_082.xlsx`, `trad_Percechange2072_to_82.xlsx` |
| `customoffice_trade/` | Custom office data processing scripts | `customoffice_trade_allyr.xlsx` |

## 🛠️ Technical Implementation

- **Framework**: Streamlit with extensive custom CSS styling
- **Data Processing**: Pandas for data manipulation and analysis
- **Visualization**: Plotly for interactive and responsive charts
- **Performance**: Streamlit cache decorators for optimized data loading
- **Data Format**: Excel files with multiple sheets per fiscal year
- **Styling**: Professional government dashboard theme with Nepal colors

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nepal-trade-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas plotly openpyxl
   ```

3. **Run the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

4. **Access the dashboard**
   - Open your browser and go to `http://localhost:8501`

## 📈 Dashboard Sections

### 1. Trade Balance Summary
- Overall trade performance with KPI cards
- Interactive time series charts with growth rates
- Fiscal year range filtering (BS/AD formats)
- Comprehensive metric definitions and explanations

### 2. Trade by Products
- Top 10 traded products analysis
- Product search with historical trends
- Treemap and bar chart visualizations
- Detailed product performance metrics

### 3. Trade by Countries
- Partner countries trade analysis
- Country-specific import/export trends
- Trade balance calculations by country
- Geographic trade pattern insights

### 4. Trade by Commodities
- Detailed commodity analysis with unit filtering
- Import/export value and quantity comparisons
- Revenue share calculations
- Year-over-year growth analysis

### 5. Trade by Custom Offices
- Custom office performance metrics
- Import/export share analysis
- Geographic distribution of trade activities
- Office-wise trade balance tracking

### 6. Commodity-Country Analysis
- Cross-referencing commodities with trading partners
- Bilateral trade relationship insights
- Product-specific country performance
- Market diversification analysis

## 📊 Key Metrics & Definitions

- **Imports**: Total value of goods/services bought from abroad
- **Exports**: Total value of goods/services sold to foreign markets  
- **Trade Deficit**: Difference between imports and exports (Imports - Exports)
- **Trade Balance**: Net trade position (Exports - Imports)
- **Total Trade**: Sum of imports and exports
- **Import/Export Ratio**: Ratio showing import dependency relative to exports

## 📅 Data Coverage

- **Time Period**: Fiscal Year 2071/72 to 2081/82 (Bikram Sambat)
- **Data Source**: Department of Customs, Ministry of Finance, Government of Nepal
- **Update Frequency**: Annual with mid-year updates
- **Last Updated**: July 2025

## 🎨 Design Features

- **Professional Government Theme** with Nepal flag colors
- **Responsive Layout** optimized for different screen sizes
- **Interactive Elements** with hover effects and smooth transitions
- **Accessibility** considerations with proper contrast and font sizes
- **Modern UI Components** with gradient backgrounds and shadow effects

## 📝 Usage Notes

- Select fiscal year ranges using the interactive slider
- Use the search functionality to find specific products or countries
- Toggle between BS (Bikram Sambat) and AD (Anno Domini) year formats
- Hover over charts for detailed information
- Click on metric definitions for external educational resources

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements.

## 📧 Contact

**Developer**: Shivaji Chaulagain  
**Email**: [Your Email]  
**Year**: 2025

## 📄 License

© 2025 Shivaji Chaulagain. All rights reserved.

---

**Data Disclaimer**: This dashboard is for analytical and educational purposes. Trade data is sourced from official government records and processed for visualization. Always refer to official sources for formal trade statistics and policy decisions.
