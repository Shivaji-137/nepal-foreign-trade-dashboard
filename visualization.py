import pandas as pd
import plotly.graph_objects as go
from utils import format_value
import plotly.express as px
from utils import prepare_search_data
from plotly.subplots import make_subplots

#.................................SUMMARY...............................

def show_description_chart(growth_data, summary_data, nepali_engyr):
    """
    Generates a Plotly figure with a grouped bar chart for summary data and
    corresponding line charts for growth data on a secondary y-axis.
    """
    summary_cols = summary_data.columns.tolist()[1:5]
    growth_cols = growth_data.columns.tolist()[1:6]
    print(growth_cols)
    
    nam = ["Imports", "Exports", "Trade Deficit", "Total Trade"]
    nams = ["Imports", "Exports", "Trade Deficit", "Total Trade", "Imp/Exp Ratio"]
    color = ["#2ECC71", "#3498DB", "#E74C3C", "#9B59B6"]
    colors =[ "#2ECC71", "#3498DB", "#E74C3C", "#9B59B6", "#F8A4D5"]
    if nepali_engyr == "BS":
        fiscal_years = summary_data.iloc[:, 0]

    elif nepali_engyr == "AD":
        fiscal_yearad = ["2014/15", "2015/16", "2016/17", "2017/18", "2018/19", 
                        "2019/20", "2020/21", "2021/22", "2022/23", "2023/24", "2024/25"]
        range_yr = len(fiscal_yearad) - summary_data.iloc[:,0].shape[0]
        fiscal_years = fiscal_yearad[range_yr:]
        
    fig = go.Figure()

    for i in range(len(summary_cols)):
        fig.add_trace(go.Bar(
            x=fiscal_years, 
            y=summary_data[summary_cols[i]]*1000, 
            name=nam[i], 
            marker_color=color[i]
        ))
    
    for i in range(len(growth_cols)):
        fig.add_trace(go.Scatter(
            x=fiscal_years, 
            y=growth_data[growth_cols[i]], 
            name=f"{nams[i]} Growth", 
            mode='lines+markers',
            line=dict(color=colors[i], dash='dot'),
            marker=dict(color=colors[i]),
            yaxis="y2"
        ))

    # Update the layout with the CORRECTED structure for axes
    fig.update_layout(
        barmode='group',

        xaxis_title=f"Fiscal Year ({nepali_engyr})",
        
        # Configure Primary Y-axis (for the bars)
        yaxis=dict(
            title=dict(
                text="Amount (in trillion NPR)",
                font=dict(color="#1f77b4")
            ),
            tickfont=dict(color="#1f77b4")
        ),
        
        # Create and configure Secondary Y-axis (for the lines)
        yaxis2=dict(
            title=dict(
                text="Growth Rate (%)",
                font=dict(color="#d62728")
            ),
            tickfont=dict(color="#d62728"),
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        
        legend_title_text="Metric", 
        font=dict(size=12),
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig



def show_kpi_chart(summary_data, growth_data):
    current_year = summary_data.iloc[-1, 0]
    
    kpi_cards = []
    kpi_data = {
        "Imports": {
            "value": summary_data.iloc[-1, 1]*1000,
            "growth": growth_data.iloc[-1, 1],
            "previous_growth":growth_data.iloc[-2,1]

        },
        "Exports": {
            "value": summary_data.iloc[-1, 2]*1000,
            "growth": growth_data.iloc[-1, 2],
            "previous_growth":growth_data.iloc[-2,2]

        },
        "Trade Deficit": {
            "value": summary_data.iloc[-1, 3]*1000,
            "growth": growth_data.iloc[-1, 3],
            "previous_growth":growth_data.iloc[-2,3]
        },
        
        "Imp/Exp ratio": {
            "value": summary_data.iloc[-1, 5],
            "growth": growth_data.iloc[-1, 5],
            "previous_growth":growth_data.iloc[-2,5]

        }
    }
    for kpi, data in kpi_data.items():
        growth = data["growth"]
        if growth > data["previous_growth"]:
            delta = f"{growth:.2f}%▲"
            delta_color = "green"
        else:
            delta = f"{growth:.2f}%▼"
            delta_color = "red"

        kpi_cards.append({
            "label": kpi,
            "value": f"{format_value(data['value'])}",
            "delta": delta,
            "delta_color": delta_color
        })
    
    return kpi_cards

#........................BY PRODUCTS............................................................

def hbarplot_top10product(currentyear_data, selected):
    currentyear_data = currentyear_data.iloc[:-1, :]  # Exclude the last row which is a total row
    current_top10import = currentyear_data.sort_values(by="Imports_Value", ascending=False).head(10)
    # Update the row BEFORE reversing
    current_top10import.loc[current_top10import["Description"].str.contains("electrical machinery and equipment and parts thereof; sound recorders and reproducers; television image and sound recorders and reproducers, parts and accessories of such articles", case=False), 'Description'] = "Electrical machinery; sound recorders and reproducers; television image, parts of such articles"
    current_top10import.loc[current_top10import["Description"].str.contains("Natural, cultured pearls; precious, semi-precious stones; precious metals, metals clad with precious metal, and articles thereof; imitation jewellery; coin", case=False), 'Description'] = "Natural, cultured pearls; precious, semi-precious stones; precious metals, imitation jewellery; coin"
    # Then reverse it for plotting
    current_top10import = current_top10import.iloc[::-1]
    current_top10export = currentyear_data.sort_values(by="Exports_Value", ascending=False).head(10).iloc[::-1]
    current_top10tradebalance = currentyear_data.sort_values(by="Trade_Balance", ascending=False).head(10).iloc[::-1]
    fig = go.Figure()
    # show chart that is sorted by trade balances
    if selected == "Trade Balance":
        fig.add_trace(go.Treemap(
            labels=current_top10tradebalance["Description"],
            values=current_top10tradebalance["Trade_Balance"]*1000,
            parents=[""] * len(current_top10tradebalance),  # Empty string parents for top level
            textinfo="label+value",
            hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Top 10 Trade Balance Products Treemap',
            height=500,
        )
        
    elif selected == "Import":
        fig.add_traces(go.Bar(
            y=current_top10import["Description"],
            x = current_top10import["Imports_Value"]*1000,
            orientation="h",
            name="Imports",
            text=current_top10import["Imports_Value"].apply(lambda x: f"{format_value(x*1000)} NPR"),  # Add values as text
            texttemplate='%{text}',  # Format the text
            textposition='inside',
            marker_color='#2ECC71'
        ))
        fig.update_layout(
            title='Top 10 Import Products',
            # barmode='relative',
            height=500,
            yaxis=dict(tickfont=dict(size=7)),
            legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
        )
    elif selected == "Export":
        fig.add_traces(go.Bar(
            y=current_top10export["Description"],
            x = current_top10export["Exports_Value"],
            orientation="h",
            name="Exports",
            text=current_top10export["Exports_Value"].apply(lambda x: f"{format_value(x*1000)} NPR"),  # Add values as text
            texttemplate='%{text}',  # Format the text
            textposition='inside', 
            marker_color='#377eb8'
        ))
        fig.update_layout(
            title='Top 10 Export Products',
            # barmode='relative',
            height=600,
            yaxis=dict(tickfont=dict(size=10)),
            legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
        )
    return fig
    

def treeplot_top10product(currentyear_data, selected):
    currentyear_data = currentyear_data.iloc[:-1, :]  # Exclude the last row which is a total row
    current_top10import = currentyear_data.sort_values(by="Imports_Value", ascending=False).head(10)
    current_top10import["Imports_Value"] = current_top10import["Imports_Value"]*1000

    # Update the row BEFORE reversing
    current_top10import.loc[current_top10import["Description"].str.contains("electrical machinery and equipment and parts thereof; sound recorders and reproducers; television image and sound recorders and reproducers, parts and accessories of such articles", case=False), 'Description'] = "Electrical machinery; sound recorders and reproducers; television image, parts of such articles"
    current_top10import.loc[current_top10import["Description"].str.contains("Natural, cultured pearls; precious, semi-precious stones; precious metals, metals clad with precious metal, and articles thereof; imitation jewellery; coin", case=False), 'Description'] = "Natural, cultured pearls; precious, semi-precious stones; precious metals, imitation jewellery; coin"

    # Then reverse it for plotting
    current_top10import = current_top10import.iloc[::-1]

    current_top10export = currentyear_data.sort_values(by="Exports_Value", ascending=False).head(10).iloc[::-1]
    current_top10export["Exports_Value"] = current_top10export["Exports_Value"]*1000

    current_top10tradebalance = currentyear_data.sort_values(by="Trade_Balance", ascending=False).head(10).iloc[::-1]
    current_top10tradebalance["Trade_Balance"] = current_top10import["Trade_Balance"]*1000

    fig = go.Figure()

    if selected == "Import":
        fig = go.Figure()
        fig = px.scatter(
            current_top10import,
            x="Imports_Value",
            y="Description",
            title="Top 10 Import Products (scatter plot)",
            labels={"Import_Value": "Value", "Description": "Products"},
            hover_data=["Imports_Value"],
            color="Imports_Value",
            color_continuous_scale='RdYlGn'
        )
        fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
        fig.update_layout(
            xaxis_title="Import Value (NPR)",
            # yaxis_title="Products",
            height=500,
            showlegend=False
        )

    
    elif selected == "Export":
        fig = go.Figure()
        fig = px.scatter(
            current_top10export,
            x="Exports_Value",
            y="Description",
            title="Top 10 Export Products (scatter plot)",
            labels={"Exports_Value": "Value", "Description": "Products"},
            hover_data=["Exports_Value"],
            color="Exports_Value",
            color_continuous_scale='RdYlGn'
            # color_discrete_sequence=["#636efa"]  # Default color
        )
        fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
        fig.update_layout(
            xaxis_title="Export Value (NPR)",
            # yaxis_title="Products",
            height=500,
            showlegend=False
        )

    elif selected == "Trade Balance":
        # fig = go.Figure()
        fig.add_traces(go.Bar(
            y=current_top10tradebalance["Description"],
            x = current_top10tradebalance["Exports_Value"]*1000,
            orientation="h",
            name="Exports",
            text=current_top10tradebalance["Exports_Value"].apply(lambda x: f"{format_value(x*1000)} NPR"),  # Add values as text
            texttemplate='%{text}',  # Format the text
            textposition='outside',
            marker_color='#377eb8'
        ))
        fig.add_traces(go.Bar(
            y=current_top10tradebalance["Description"],
            x = -current_top10tradebalance["Imports_Value"]*1000,
            orientation="h",
            name="Imports",
            text=current_top10tradebalance["Imports_Value"].apply(lambda x: f"{format_value(x*1000)} NPR"),  # Add values as text
            texttemplate='%{text}',  # Format the text
            textposition='outside',
            marker_color='#e41a1c'
        ))
        fig.update_layout(
            title=f'Exports-Imports for Top 10 Products',
            barmode='relative',
            height=600,
            yaxis=dict(tickfont=dict(size=13)),
            legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
        )
        
    return fig

#...............................Search function for all tab...........................

def search_product_plot(product_data, selected_product, keys=None):
    if keys == "custom":
        fiscal_years, import_values, export_values, imports_share, export_shares = prepare_search_data(product_data, keys)
        fig = go.Figure()
        
        # Add traces for imports, exports and trade balance
        fig.add_trace(go.Scatter(
            x=fiscal_years,
            y=import_values,
            mode='lines+markers',
            name='Imports',
            marker_color='#2ECC71'
        ))
        
        fig.add_trace(go.Scatter(
            x=fiscal_years,
            y=export_values,
            mode='lines+markers',
            name='Exports',
            marker_color='#3498DB'
        ))
        
        
        fig.update_layout(
            title=f'Trade Trend for: {selected_product}',
            xaxis_title='Fiscal Year (BS)',
            yaxis_title='Value (NPR)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        return fig
    

    else:
        fiscal_years, import_values, export_values, total_trade, trade_balance = prepare_search_data(product_data, keys)

        # Create trend plot
        fig = go.Figure()
        
        # Add traces for imports, exports and trade balance
        fig.add_trace(go.Scatter(
            x=fiscal_years,
            y=import_values,
            mode='lines+markers',
            name='Imports',
            marker_color='#2ECC71'
        ))
        
        fig.add_trace(go.Scatter(
            x=fiscal_years,
            y=export_values,
            mode='lines+markers',
            name='Exports',
            marker_color='#3498DB'
        ))
        fig.add_trace(go.Scatter(
            x=fiscal_years,
            y=total_trade,
            mode='lines+markers',
            name='Total Trade',
            marker_color='#9A31CA'
        ))
        
        fig.add_trace(go.Scatter(
            x=fiscal_years,
            y=trade_balance,
            mode='lines+markers',
            name='Trade Balance',
            marker_color='#E74C3C'
        ))
        
        fig.update_layout(
            title=f'Trade Trend for: {selected_product}',
            xaxis_title='Fiscal Year (BS)',
            yaxis_title='Value (NPR)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        return fig

def search_product_bar(product_data, selected_product, keys=None):
    if keys == "custom":
        fiscal_years, import_values, export_values, imports_share, export_shares = prepare_search_data(product_data, keys)
        # Create bar plot
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=fiscal_years,
            y=import_values,
            name='Imports',
            text=[f"{format_value(x*1000)} NPR" for x in import_values],
            texttemplate='%{text}',
            textposition='inside',
            marker_color='#2ECC71'
        ))
        
        fig.add_trace(go.Bar(
            x=fiscal_years,
            y=export_values,
            name='Exports',
            text=[f"{format_value(x*1000)} NPR" for x in export_values],
            texttemplate='%{text}',
            textposition='inside',
            marker_color='#3498DB'
        ))
        fig.add_trace(go.Scatter(
            x=fiscal_years, 
            y=imports_share, 
            name="Imports_share(%)", 
            mode='lines+markers',
            line=dict(color="#41E94F", dash='dot'),
            marker=dict(color="#07831B"),
            yaxis="y2"
        ))
        fig.add_trace(go.Scatter(
            x=fiscal_years, 
            y=export_shares, 
            name="Exports_share(%)", 
            mode='lines+markers',
            line=dict(color="#3877EB", dash='dot'),
            marker=dict(color="#084986"),
            yaxis="y2"
        ))
        
        fig.update_layout(
            title=f'Trade Bar Chart for: {selected_product}',
            xaxis_title='Fiscal Year (BS)',
            barmode='group',
            yaxis=dict(
                title=dict(
                    text="Amount (in trillion NPR)",
                    font=dict(color="#1f77b4")
                ),
                tickfont=dict(color="#1f77b4")
            ),
        
            # Create and configure Secondary Y-axis (for the lines)
            yaxis2=dict(
                title=dict(
                    text="Share (%)",
                    font=dict(color="#d62728")
                ),
                tickfont=dict(color="#d62728"),
                overlaying="y",
                side="right",
                showgrid=False,
            ),
            
            legend_title_text="Metric", 
            font=dict(size=12),
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )

        )
        
        return fig
    
    else:
        fiscal_years, import_values, export_values, total_trade, trade_balance = prepare_search_data(product_data, keys)

        # Create bar plot
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=fiscal_years,
            y=import_values,
            name='Imports',
            text=[f"{format_value(x)}" for x in import_values],
            texttemplate='%{text}',
            textposition='inside',
            textangle=270,
            textfont=dict(size=10),
            marker_color='#2ECC71'
        ))
        
        fig.add_trace(go.Bar(
            x=fiscal_years,
            y=export_values,
            name='Exports',
            text=[f"{format_value(x)}" for x in export_values],
            texttemplate='%{text}',
            textposition='inside',
            textangle= 270,
            textfont=dict(size=10),
            marker_color='#3498DB'
        ))
        fig.add_trace(go.Bar(
            x=fiscal_years,
            y=total_trade,
            name='Total Trade',
            text=[f"{format_value(x)}" for x in total_trade],
            texttemplate='%{text}',
            textposition='inside',
            textangle=270,
            textfont=dict(size=10),
            marker_color="#9A31CA"
        ))
        
        fig.add_trace(go.Bar(
            x=fiscal_years,
            y=trade_balance,
            name='Trade Balance',
            text=[f"{format_value(x)}" for x in trade_balance],
            texttemplate='%{text}',
            textposition='inside',
            textangle= 270,
            textfont=dict(size=10),
            marker_color='#E74C3C'
        ))
        
        fig.update_layout(
            title=f'Trade Bar Chart for: {selected_product}',
            xaxis_title='Fiscal Year (BS)',
            yaxis_title='Value in trillion (NPR)',
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig

# ....................By Countries...............................

def hbarplot_top10countries(currentyear_data, selected, desc):
    currentyear_data = currentyear_data.iloc[:-1, :]  # Exclude the last row which is a total row
    current_top10import = currentyear_data.sort_values(by="Imports_Value", ascending=False).head(10)

    # Then reverse it for plotting
    current_top10import = current_top10import.iloc[::-1]
    current_top10export = currentyear_data.sort_values(by="Exports_Value", ascending=False).head(10).iloc[::-1]
    current_top10tradebalance = currentyear_data.sort_values(by="Trade_Balance", ascending=False).head(10).iloc[::-1]

    fig = go.Figure()
    # show chart that is sorted by trade balances
    if selected == "Trade Balance":
        fig.add_traces(go.Bar(
            y=current_top10tradebalance[desc],
            x = current_top10tradebalance["Exports_Value"]*1000,
            orientation="h",
            name="Exports",
            marker_color='#377eb8'
        ))
        fig.add_traces(go.Bar(
            y=current_top10tradebalance[desc],
            x = -current_top10tradebalance["Imports_Value"]*1000,
            orientation="h",
            name="Imports",
            marker_color='#e41a1c'
        ))
        fig.update_layout(
            title=f'Exports-Imports for Top 10 Trade {desc}',
            barmode='relative',
            height=600,
            yaxis=dict(tickfont=dict(size=13)),
            legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
        )
        
        
    elif selected == "Import":
        fig.add_traces(go.Bar(
            y=current_top10import[desc],
            x = current_top10import["Imports_Value"]*1000,
            orientation="h",
            name="Imports",
            marker_color='#377eb8'
        ))
        fig.update_layout(
            title=f'Top 10 Import Trade {desc} (Value in NPR)',
            # barmode='relative',
            height=500,
            yaxis=dict(tickfont=dict(size=12)),
            legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
        )
    elif selected == "Export":
        fig.add_traces(go.Bar(
            y=current_top10export[desc],
            x = current_top10export["Exports_Value"]*1000,
            orientation="h",
            name="Exports",
            marker_color='#377eb8'
        ))
        fig.update_layout(
            title=f'Top 10 Export Trade {desc} (Value in NPR)',
            # barmode='relative',
            height=600,
            yaxis=dict(tickfont=dict(size=10)),
            legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
        )
    return fig
    

def treeplot_top10countries(currentyear_data, selected):
    currentyear_data = currentyear_data.iloc[:-1, :]  # Exclude the last row which is a total row
    current_top10import = currentyear_data.sort_values(by="Imports_Value", ascending=False).head(10)
    current_top10import["Imports_Value"] = current_top10import["Imports_Value"]*1000

    # Then reverse it for plotting
    current_top10import = current_top10import.iloc[::-1]

    current_top10export = currentyear_data.sort_values(by="Exports_Value", ascending=False).head(10).iloc[::-1]
    current_top10export["Exports_Value"] = current_top10export["Exports_Value"]*1000

    current_top10tradebalance = currentyear_data.sort_values(by="Trade_Balance", ascending=False).head(10).iloc[::-1]
    current_top10tradebalance["Trade_Balance"] = current_top10tradebalance["Trade_Balance"]*1000

    fig = go.Figure()

    if selected == "Import":
        fig = go.Figure()
        fig = px.scatter(
            current_top10import,
            x="Imports_Value",
            y="Partner Countries",
            title="Top 10 Import Trade Countries (scatter plot)",
            labels={"Import_Value": "Value", "Partner Countries": "Products"},
            hover_data=["Imports_Value"],
            color="Imports_Value",
            color_continuous_scale='RdYlGn'
        )
        fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
        fig.update_layout(
            xaxis_title="Import Value (NPR)",
            # yaxis_title="Products",
            height=500,
            showlegend=False
        )

    
    elif selected == "Export":
        fig = go.Figure()
        fig = px.scatter(
            current_top10export,
            x="Exports_Value",
            y="Partner Countries",
            title="Top 10 Export Trade Countries (scatter plot)",
            labels={"Exports_Value": "Value", "Partner Countries": "Country"},
            hover_data=["Exports_Value"],
            color="Exports_Value",
            color_continuous_scale='RdYlGn'
        )
        fig.update_traces(marker=dict(size=13, line=dict(width=2, color='DarkSlateGrey')))
        fig.update_layout(
            xaxis_title="Export Value (in NPR)",
            height=500,
            showlegend=False
        )

    elif selected == "Trade Balance":
        fig.add_trace(go.Treemap(
            labels=current_top10tradebalance["Partner Countries"],
            values=current_top10tradebalance["Trade_Balance"],
            parents=[""] * len(current_top10tradebalance),  # Empty string parents for top level
            textinfo="label+value",
            hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Top 10 Trade Balance Trade Countries Treemap',
            height=500,
        )
    return fig

#...........................Import By Commodity..................
def unit_data(data,unit):
    dat = data
    if unit == "Kilogram(Kg)":
        dat = dat[dat["Unit"].str.upper() == "KG"]
    elif unit == "Kilolitre(Kl)":
        dat = dat[dat["Unit"] == "KL"]
    elif unit == "Litre(LTR)":
        dat = dat[dat["Unit"] == "LTR"]
    elif unit == "Pieces(PCS)":
        dat = dat[dat["Unit"] == "PCS"]
    elif unit == "All":
        dat = data
   
    return dat

def top10_importCommodity_plot(data, select, unit_select, keys, hasrevenue):
    value = f"{keys}s_Value"
    revenue = f"{keys}s_Revenue"
    data = data.iloc[:-1,:]
   
    top10_unit_value = unit_data(data, unit_select).sort_values(by=value, ascending=False).head(10).iloc[::-1]
    top10_unit_quantity = unit_data(data, unit_select).sort_values(by="Quantity", ascending=False).head(10).iloc[::-1]
    if hasrevenue:
        top10_unit_revenue = unit_data(data, unit_select).sort_values(by=revenue, ascending=False).head(10).iloc[::-1]
    
    fig = go.Figure()

    if select == f"{keys} Value":
        text_labels = [f"{format_value(float(val))} {unit}" for val, unit in 
                      zip(top10_unit_value["Quantity"], top10_unit_value["Unit"])]
        
        fig.add_traces(go.Bar(
            y=top10_unit_value["Description"],
            x=top10_unit_value[value]*1000,
            orientation="h",
            name=f"{keys}s",
            marker_color="#0f6bd3",
            text=text_labels,  # Add formatted text with value and unit
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=12)
        ))
        fig.update_layout(
            title=f'Top 10 {keys}ed Product (Value in NPR)',
            height=500,
            xaxis_title=f"{keys} Value (in billion NPR)",
            yaxis=dict(
                tickfont=dict(size=14),
                side='left'
            ),
            legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
        )
        

    elif select == "Quantity":
        # Format the text to include both quantity with unit AND import value
        quantity_labels = [f"{format_value(q)} {unit} | NPR {format_value(val)}" for q, unit, val in 
                          zip(top10_unit_quantity["Quantity"], top10_unit_quantity["Unit"], 
                              top10_unit_quantity[value]*1000)]
        
        fig.add_traces(go.Bar(
            y=top10_unit_quantity["Description"],
            x=top10_unit_quantity["Quantity"],
            orientation="h",
            name="Quantity",
            marker_color="#616DDA",
            text=quantity_labels,  # Show both quantity and import value
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=12)
        ))
        fig.update_layout(
            title=f'Top 10 {keys}ed Products by Quantity',
            xaxis_title="Quantity in billion",
            height=500,
            yaxis=dict(tickfont=dict(size=14)),
            legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
        )
        

    elif select == f"{keys} Revenue":
        if hasrevenue:
            text_labels = [f"{format_value(val)} {unit}" for val, unit in 
                        zip(top10_unit_revenue["Quantity"], top10_unit_revenue["Unit"])]
            
            fig.add_traces(go.Bar(
                y=top10_unit_revenue["Description"],
                x=top10_unit_revenue[revenue]*1000,
                orientation="h",
                name=f"{keys}",
                marker_color="#0f6bd3",
                text=text_labels,  # Add formatted text with value and unit
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(color='white', size=12)
            ))
            fig.update_layout(
                title=f'Top 10 {keys}ed Product by Revenue (Value in NPR)',
                height=500,
                xaxis_title=" Value (in billion NPR)",
                yaxis=dict(
                    tickfont=dict(size=14),
                    side='left'
                ),
                legend=dict(x=0.5, y=-0.15, xanchor='center', orientation='h')
            )
        else:
            pass
        
    return fig

def import_commodity_comparision(selected_product, product_info, commodity_data, keys, hasrevenue):
    value = f"{keys}s_Value"
    revenue = f"{keys}s_Revenue"

    total_value = commodity_data[value].sum()
    revenue_case = "Share of Import Revenue" if hasrevenue else " "
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]], subplot_titles=[f"Share of {keys} Value",revenue_case])

    if hasrevenue:
        total_import_revenue = commodity_data["Imports_Revenue"].sum()                
                        
    # Add pie charts for import value and revenue
    fig.add_trace(
        go.Pie(
            labels=[selected_product, "All Other Products"],
            values=[product_info[value], total_value - product_info[value]],
            hole=.4,
            marker_colors=["#3498DB", "#E74C3C"],
            textinfo="percent+label"
        ),
        row=1, col=1
    )

    if hasrevenue:
        fig.add_trace(
            go.Pie(
                labels=[selected_product, "All Other Products"],
                values=[product_info["Imports_Revenue"], total_import_revenue - product_info["Imports_Revenue"]],
                hole=.4,
                marker_colors=["#2ECC71", "#9B59B6"],
                textinfo="percent+label"
            ),
            row=1, col=2
        )
    
    fig.update_layout(
        title_text=f"Import Significance of {selected_product} in Fiscal Year 2080/81",
        height=500
    )
        
    # Bar chart for context - compare with similar products
    similar_products = commodity_data[
        (commodity_data["Unit"] == product_info["Unit"]) & 
        (commodity_data["Description"] != selected_product)
    ].nlargest(5, value)
    
    # Add the selected product to create comparison
    comparison_df = pd.concat([
        pd.DataFrame([product_info]),
        similar_products
    ])
    
    # Create comparison bar chart
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        x=comparison_df["Description"],
        y=comparison_df[value]*1000,  # Convert to NPR
        marker_color=['#3498DB' if desc == selected_product else '#E74C3C' 
                        for desc in comparison_df["Description"]],
        text=[f"{val*1000:,.0f} NPR" for val in comparison_df[value]],
        textposition='auto'
    ))
    
    fig2.update_layout(
        title=f"Comparison with Top 5 Products (Same Unit: {product_info['Unit']})",
        xaxis=dict(title="Products"),
        yaxis=dict(title=f"{keys} Value (NPR)"),
        height=500
    )
    
    return fig, fig2

def plot_expimp_growth_by_year(data, keys):
    recent_year = list(data.keys())[0]
    previous_year = list(data.keys())[1]
    recent_year_data = data[recent_year]
    previous_year_data = data[previous_year]
    years = [previous_year, recent_year]
    imp_data = [previous_year_data["import_value"]*1000, recent_year_data["import_value"]*1000]
    print("import data", imp_data[0])
    imp_quantity = [previous_year_data["imp_quantity"], recent_year_data["imp_quantity"]]
    exp_data = [previous_year_data["export_value"]*1000, recent_year_data["export_value"]*1000]
    exp_quantity = [previous_year_data["exp_quantity"], recent_year_data["exp_quantity"]]
    units = recent_year_data["unit"]
    imp_change_data = (imp_data[1] - imp_data[0])/imp_data[0]*100 if imp_data[0] != 0 else 0
    exp_change_data = (exp_data[1] - exp_data[0])/exp_data[0]*100 if exp_data[0] != 0 else 0
    imp_quant_change = (imp_quantity[1] - imp_quantity[0])/imp_quantity[0]*100 if imp_quantity[0] != 0 else 0
    exp_quant_change = (exp_quantity[1] - exp_quantity[0])/exp_quantity[0]*100 if exp_quantity[0] != 0 else 0

    fig = go.Figure()
    fig_ = go.Figure()
    fig.add_trace(go.Bar(
            x=years, 
            y=imp_data, 
            name="Imports_Value", 
            text=[f"{format_value(x)} NPR" for x in imp_data],
            marker=dict(color="#07831B"),
    ))
    
    # Fixed annotation inside the import bar
    fig.add_annotation(
        x=years[1],
        y=imp_data[1] * 0.5,  # Position at 50% of bar height (middle)
        text=f"{'Import↗' if imp_change_data >= 0 else 'Import↘'} {abs(imp_change_data):.1f}%",
        showarrow=False,
        font=dict(
            size=14,
            color="white",  # White text for better visibility inside green bar
            family="Arial",
            weight="bold"
        ),
        bgcolor="rgba(0,0,0,0.7)",  # Semi-transparent black background
        bordercolor="white",
        borderwidth=1
    )
    
    fig_.add_trace(go.Bar(
            x=years, 
            y=imp_quantity, 
            name="Imports_Quantity", 
            text=[f"{int(x)} {units}" for x in imp_quantity],
            marker=dict(color="#C9AA44"),
    ))
    
    # Fixed annotation inside the import quantity bar
    fig_.add_annotation(
        x=years[1],
        y=imp_quantity[1] * 0.5,  # Position at 50% of bar height (middle)
        text=f"{'Imp Quant↗' if imp_quant_change >= 0 else 'Imp Quant↘'} {abs(imp_quant_change):.1f}%",
        showarrow=False,
        font=dict(
            size=14,
            color="white",
            family="Arial",
            weight="bold"
        ),
        bgcolor="rgba(0,0,0,0.7)",
        bordercolor="white",
        borderwidth=1
    )
    
    fig.update_layout(
        title=f'Growth Bar Chart',
        xaxis_title='Fiscal Year (BS)',
        barmode='group',
        yaxis=dict(
            title=dict(
                text="Amount (in trillion NPR)",
                font=dict(color="#1f77b4")
            ),
            tickfont=dict(color="#1f77b4")
        ),
        legend_title_text="Metric", 
        font=dict(size=12),
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.add_trace(go.Bar(
        x=years, 
        y=exp_data, 
        name="Exports_Value", 
        text=[f"{format_value(x)} NPR" for x in exp_data],
        marker=dict(color="#084986"),
    ))
    
    # Fixed annotation inside the export bar - only show if export growth is not 0
    if abs(exp_change_data) >= 0.01:  # Only show if growth is greater than 0.01%
        fig.add_annotation(
            x=years[1],
            y=exp_data[1] * 0.5,  # Position at 50% of bar height (middle)
            text=f"{'Export↗' if exp_change_data >= 0 else 'Export↘'} {abs(exp_change_data):.1f}%",
            showarrow=False,
            font=dict(
                size=14,
                color="white",
                family="Arial",
                weight="bold"
            ),
            bgcolor="rgba(0,0,0,0.7)",
            bordercolor="white",
            borderwidth=1
        )
    else:
        # Show "No Export" when growth is 0
        fig.add_annotation(
            x=years[1],
            y=exp_data[1] * 0.5,
            text="No Export",
            showarrow=False,
            font=dict(
                size=14,
                color="white",
                family="Arial",
                weight="bold"
            ),
            bgcolor="rgba(255,0,0,0.7)",  # Red background for "No Export"
            bordercolor="white",
            borderwidth=1
        )
    
    fig_.add_trace(go.Bar(
            x=years, 
            y=exp_quantity, 
            name="Exports_Quantity", 
            text=[f"{int(x)} {units}" for x in exp_quantity],
            marker=dict(color="#BD81CC"),
    ))
    
    # Fixed annotation inside the export quantity bar - only show if export quantity change is not 0
    if abs(exp_quant_change) > 0.01:  # Only show if quantity change is greater than 0.01%
        fig_.add_annotation(
            x=years[1],
            y=exp_quantity[1] * 0.5,  # Position at 50% of bar height (middle)
            text=f"{'↗' if exp_quant_change >= 0 else '↘'} {abs(exp_quant_change):.1f}%",
            showarrow=False,
            font=dict(
                size=14,
                color="white",
                family="Arial",
                weight="bold"
            ),
            bgcolor="rgba(0,0,0,0.7)",
            bordercolor="white",
            borderwidth=1
        )
    else:
        # Show "No Export" when quantity change is 0
        fig_.add_annotation(
            x=years[1],
            y=exp_quantity[1] * 0.5,
            text="No Export",
            showarrow=False,
            font=dict(
                size=14,
                color="white",
                family="Arial",
                weight="bold"
            ),
            bgcolor="rgba(255,0,0,0.7)",  # Red background for "No Export"
            bordercolor="white",
            borderwidth=1
        )
    
    fig_.update_layout(
        title=f'Quantity Bar Chart',
        xaxis_title='Fiscal Year (BS)',
        barmode='group',
        yaxis=dict(
            title=dict(
                text="Quantity",
                font=dict(color="#1f77b4")
            ),
            tickfont=dict(color="#1f77b4")
        ),
        
        legend_title_text="Metric", 
        font=dict(size=12),
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
        
    return fig, fig_


def plot_different_countries_with_same_product(import_data, export_data, product):
    print(import_data.columns)
    import_value = import_data["Imports_Value"]*1000
    import_quantity = import_data["Quantity"]
    export_value = export_data["Exports_Value"]*1000
    export_quantity = export_data["Quantity"]
    impquantity_labels = [f"{format_value(q)} {unit}" for q, unit in 
                          zip(import_data["Quantity"], import_data["Unit"])]
    expquantity_labels = [f"{format_value(q)} {unit}" for q, unit in 
                          zip(export_data["Quantity"], export_data["Unit"])]
      
    
    fig = go.Figure()
    fig1 = go.Figure()

    fig.add_traces(
        go.Bar(
            x=import_data["Partner Countries"],
            y = import_value,
            name="Imports_Value", 
            text=[f"{format_value(x)} NPR" for x in import_value],
            marker=dict(color="#07831B"),
        )
    )
    fig1.add_traces(
        go.Bar(
            x=import_data["Partner Countries"],
            y = import_quantity,
            name="Imports_quantity", 
            marker=dict(color="#07831B"),
            text=impquantity_labels,  # Show both quantity and import value
            textposition='outside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=12)
        )
    )
    
    
    fig.add_traces(
        go.Bar(
            x=export_data["Partner Countries"],
            y = export_value,
            name="Exports_Value", 
            text=[f"{format_value(x)} NPR" for x in export_value],
            marker=dict(color="#084986"),
        )
    )
    fig1.add_traces(
        go.Bar(
            x=export_data["Partner Countries"],
            y = export_quantity,
            name="Exports_quantity", 
            marker=dict(color="#084986"),
            text=expquantity_labels,  
            textposition='outside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=12)
        )
    )
    fig.update_layout(
        title=f"Trade Information of '{product}' from different countries",
        xaxis_title='Countries',
        barmode='group',
        yaxis=dict(
            title=dict(
                text="Amount (in Billion NPR)",
                font=dict(color="#1f77b4")
            ),
            tickfont=dict(color="#1f77b4")
        ),
        legend_title_text="Metric", 
        font=dict(size=12),
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig1.update_layout(
        title=f"Trade Quantity of '{product}' from different countries",
        xaxis_title='Countries',
        barmode='group',
        yaxis=dict(
            title=dict(
                text="Quantity",
                font=dict(color="#1f77b4")
            ),
            tickfont=dict(color="#1f77b4")
        ),
        legend_title_text="Metric", 
        font=dict(size=12),
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig, fig1

    


