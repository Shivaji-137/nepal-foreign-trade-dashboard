import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Read data
excel_data = pd.read_excel("./filtered_data/trade_2071_081.xlsx", sheet_name=0)
per_data = pd.read_excel("./filtered_data/trad_Percechange2072_to_81.xlsx", sheet_name=0)
col = excel_data.columns

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add bars for main trade metrics
fig.add_trace(
    go.Bar(
        x=excel_data[col[0]],
        y=excel_data[col[2]],
        name="Exports",
        marker_color='green',
        width=0.3
    ),
    secondary_y=False
)

fig.add_trace(
    go.Bar(
        x=excel_data[col[0]],
        y=excel_data[col[1]],
        name="Imports",
        marker_color='blue',
        width=0.3
    ),
    secondary_y=False
)

fig.add_trace(
    go.Bar(
        x=excel_data[col[0]],
        y=excel_data[col[4]],
        name="Total Foreign Trade",
        marker_color='yellow',
        width=0.3
    ),
    secondary_y=False
)

fig.add_trace(
    go.Bar(
        x=excel_data[col[0]],
        y=excel_data[col[3]],
        name="Trade Deficit",
        marker_color='red',
        width=0.3
    ),
    secondary_y=False
)

# Add percentage metrics as lines
# fig.add_trace(
#     go.Scatter(
#         x=excel_data[col[0]],
#         y=excel_data[col[5]],  # Export share percentage
#         name="Import/Export Ratio (%)",
#         line=dict(color='darkgoldenrod', width=3),
#         mode='lines+markers'
#     ),
#     secondary_y=True
# )

fig.add_trace(
    go.Scatter(
        x=excel_data[col[0]],
        y=per_data[col[4]],  # Import share percentage
        name="Change in Total Trade (%)",
        line=dict(color='red', width=3),
        mode='lines+markers'
    ),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(
        x=excel_data[col[0]],
        y=per_data[col[2]],  # Import share percentage
        name="Exports growth (%)",
        line=dict(color='green', width=3),
        mode='lines+markers'
    ),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(
        x=excel_data[col[0]],
        y=per_data[col[1]],  # Import share percentage
        name="Imports growth (%)",
        line=dict(color='blue', width=3),
        mode='lines+markers'
    ),
    secondary_y=True
)

# Update layout
fig.update_layout(
    title="Foreign Trade Description",
    xaxis_title="Fiscal Year",
    barmode='group',
    height=600,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Update axes labels
fig.update_yaxes(title_text="Amount (in billion NPR)", secondary_y=False)
fig.update_yaxes(title_text="Percentage (%)", secondary_y=True)

# Display the plot
st.plotly_chart(fig, use_container_width=True)
st.subheader(f"Key Insights")
st.subheader(f"Latest Fiscal Year: {excel_data[col[0]].iloc[-1]}")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Exports", value=f"{excel_data[col[2]].sum():,.2f}")
    st.metric(label="Total Imports", value=f"{excel_data[col[1]].sum():,.2f}")
with col2:
    st.metric(label="Total Trade Deficit", value=f"{excel_data[col[3]].sum():,.2f}")
    st.metric(label="Total Foreign Trade", value=f"{excel_data[col[4]].sum():,.2f}")