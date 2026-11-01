"""
SpaceX Falcon 9 Mission Control & Landing Intelligence Dashboard
IBM Applied Data Science Capstone Project
Author: Muhammad Qasim
"""

import pandas as pd
import numpy as np
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Data Loading & Preparation
# -----------------------------------------------------------------------------
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Clean & normalize columns
min_payload = int(spacex_df['Payload Mass (kg)'].min())
max_payload = int(spacex_df['Payload Mass (kg)'].max())

# Add human-readable landing outcome label (no emojis/ticks/crosses)
spacex_df['Landing Outcome'] = spacex_df['class'].apply(
    lambda x: 'Recovered' if x == 1 else 'Lost / Expended'
)

# Color maps for professional themes
BOOSTER_COLOR_MAP = {
    'v1.0': '#64748B',
    'v1.1': '#3B82F6',
    'FT': '#00E5FF',
    'B4': '#A855F7',
    'B5': '#00E676'
}

OUTCOME_COLOR_MAP = {
    'Recovered': '#00E676',
    'Lost / Expended': '#FF3366'
}

# -----------------------------------------------------------------------------
# Dash Application Setup
# -----------------------------------------------------------------------------
app = dash.Dash(
    __name__,
    title="SpaceX Mission Control | Falcon 9 Telemetry",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# -----------------------------------------------------------------------------
# Reusable UI Helpers (Clean, Professional, No Emojis)
# -----------------------------------------------------------------------------
def create_kpi_card(card_id_prefix, title, default_val, subtitle, accent_color):
    return html.Div(
        className="mission-card kpi-card",
        style={"borderTop": f"3px solid {accent_color}"},
        children=[
            html.Div(
                className="kpi-title",
                children=[
                    html.Span(title)
                ]
            ),
            html.Div(
                id=f"kpi-{card_id_prefix}-value",
                className="kpi-value",
                style={"color": accent_color},
                children=default_val
            ),
            html.Div(
                id=f"kpi-{card_id_prefix}-sub",
                className="kpi-subtitle",
                children=subtitle
            )
        ]
    )

# -----------------------------------------------------------------------------
# App Layout
# -----------------------------------------------------------------------------
app.layout = html.Div(
    style={"padding": "24px 32px", "maxWidth": "1600px", "margin": "0 auto"},
    children=[
        # 1. TOP COMMAND BAR / HEADER
        html.Div(
            className="mission-card",
            style={
                "padding": "20px 28px",
                "marginBottom": "24px",
                "display": "flex",
                "flexWrap": "wrap",
                "justifyContent": "space-between",
                "alignItems": "center",
                "gap": "16px",
                "background": "linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(11, 15, 25, 0.95) 100%)",
                "border": "1px solid rgba(0, 229, 255, 0.2)"
            },
            children=[
                # Left Title & Badges
                html.Div(
                    children=[
                        html.Div(
                            style={"display": "flex", "alignItems": "center", "gap": "14px", "marginBottom": "6px"},
                            children=[
                                html.H1(
                                    "SPACEX FALCON 9 MISSION CONTROL",
                                    style={
                                        "margin": 0,
                                        "fontFamily": "'Space Grotesk', sans-serif",
                                        "fontSize": "1.65rem",
                                        "fontWeight": "700",
                                        "letterSpacing": "0.06em",
                                        "color": "#F8FAFC"
                                    }
                                ),
                                html.Span(
                                    style={
                                        "background": "rgba(0, 230, 118, 0.12)",
                                        "color": "#00E676",
                                        "border": "1px solid rgba(0, 230, 118, 0.3)",
                                        "borderRadius": "20px",
                                        "padding": "3px 10px",
                                        "fontSize": "0.7rem",
                                        "fontWeight": "600",
                                        "letterSpacing": "0.08em",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "6px"
                                    },
                                    children=[
                                        html.Span(className="pulse-dot"),
                                        "LIVE TELEMETRY"
                                    ]
                                )
                            ]
                        ),
                        html.P(
                            "First Stage Landing Prediction & Launch Telemetry Analytics • IBM Applied Data Science Capstone",
                            style={"margin": 0, "color": "#94A3B8", "fontSize": "0.85rem"}
                        )
                    ]
                ),
                # Right Meta Badges
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "10px"},
                    children=[
                        html.Div(
                            style={
                                "padding": "6px 14px",
                                "borderRadius": "8px",
                                "background": "rgba(255, 255, 255, 0.05)",
                                "border": "1px solid rgba(255, 255, 255, 0.1)",
                                "fontSize": "0.8rem",
                                "color": "#CBD5E1",
                                "textAlign": "right"
                            },
                            children=[
                                html.Span("Lead Scientist: ", style={"color": "#64748B"}),
                                html.Strong("Muhammad Qasim", style={"color": "#00E5FF"})
                            ]
                        ),
                        html.Div(
                            style={
                                "padding": "6px 14px",
                                "borderRadius": "8px",
                                "background": "rgba(59, 130, 246, 0.1)",
                                "border": "1px solid rgba(59, 130, 246, 0.3)",
                                "fontSize": "0.8rem",
                                "color": "#60A5FA",
                                "fontWeight": "600"
                            },
                            children="Falcon 9 Fleet: 56 Flights"
                        )
                    ]
                )
            ]
        ),

        # 2. DYNAMIC KPI STATS ROW (5 Cards Grid - Clean, Professional)
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(210px, 1fr))",
                "gap": "18px",
                "marginBottom": "24px"
            },
            children=[
                create_kpi_card("total", "Total Missions", "56", "Filtered Flights", "#38BDF8"),
                create_kpi_card("rate", "Landing Success Rate", "42.9%", "Booster Recovery %", "#00E676"),
                create_kpi_card("success", "Boosters Recovered", "24", "ASDS / RTLS Touchdowns", "#00F5A0"),
                create_kpi_card("failure", "Lost Boosters", "32", "Expended / Ocean Impact", "#FF3366"),
                create_kpi_card("payload", "Avg Payload Mass", "4,960 kg", "Target Orbit Mass", "#F59E0B"),
            ]
        ),

        # 3. INTERACTIVE HUD FILTER PANEL
        html.Div(
            className="mission-card",
            style={"padding": "24px 28px", "marginBottom": "24px"},
            children=[
                html.Div(
                    style={"display": "grid", "gridTemplateColumns": "1fr 1.3fr", "gap": "32px", "alignItems": "center"},
                    children=[
                        # Launch Site Dropdown
                        html.Div(
                            children=[
                                html.Div(
                                    style={"marginBottom": "8px"},
                                    children=[
                                        html.Label(
                                            "LAUNCH COMPLEX SELECTOR",
                                            style={
                                                "fontFamily": "'Space Grotesk', sans-serif",
                                                "fontSize": "0.78rem",
                                                "fontWeight": "600",
                                                "letterSpacing": "0.1em",
                                                "color": "#94A3B8"
                                            }
                                        )
                                    ]
                                ),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Launch Complexes (Global Telemetry)', 'value': 'ALL'},
                                        {'label': 'Cape Canaveral LC-40 (CCAFS LC-40)', 'value': 'CCAFS LC-40'},
                                        {'label': 'Cape Canaveral SLC-40 (CCAFS SLC-40)', 'value': 'CCAFS SLC-40'},
                                        {'label': 'Kennedy Space Center (KSC LC-39A)', 'value': 'KSC LC-39A'},
                                        {'label': 'Vandenberg Space Force Base (VAFB SLC-4E)', 'value': 'VAFB SLC-4E'}
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site...',
                                    clearable=False,
                                    searchable=True,
                                    style={
                                        'backgroundColor': '#0F172A',
                                        'color': '#F8FAFC'
                                    }
                                )
                            ]
                        ),
                        # Payload Slider
                        html.Div(
                            children=[
                                html.Div(
                                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "8px"},
                                    children=[
                                        html.Label(
                                            "PAYLOAD ENVELOPE (KG)",
                                            style={
                                                "fontFamily": "'Space Grotesk', sans-serif",
                                                "fontSize": "0.78rem",
                                                "fontWeight": "600",
                                                "letterSpacing": "0.1em",
                                                "color": "#94A3B8"
                                            }
                                        ),
                                        html.Div(
                                            id="payload-range-badge",
                                            style={
                                                "fontFamily": "'JetBrains Mono', monospace",
                                                "fontSize": "0.78rem",
                                                "color": "#00E5FF",
                                                "background": "rgba(0, 229, 255, 0.1)",
                                                "border": "1px solid rgba(0, 229, 255, 0.25)",
                                                "padding": "2px 10px",
                                                "borderRadius": "12px"
                                            },
                                            children=f"0 kg – {max_payload:,} kg"
                                        )
                                    ]
                                ),
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=500,
                                    marks={
                                        0: {'label': '0 kg', 'style': {'color': '#CBD5E1', 'fontSize': '12px', 'fontWeight': '500'}},
                                        2500: {'label': '2,500 kg', 'style': {'color': '#CBD5E1', 'fontSize': '12px', 'fontWeight': '500'}},
                                        5000: {'label': '5,000 kg', 'style': {'color': '#CBD5E1', 'fontSize': '12px', 'fontWeight': '500'}},
                                        7500: {'label': '7,500 kg', 'style': {'color': '#CBD5E1', 'fontSize': '12px', 'fontWeight': '500'}},
                                        10000: {'label': '10,000 kg', 'style': {'color': '#CBD5E1', 'fontSize': '12px', 'fontWeight': '500'}}
                                    },
                                    value=[min_payload, max_payload]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),

        # 4. PRIMARY ANALYTICS ROW (Pie/Donut & Scatter Chart)
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1.3fr",
                "gap": "24px",
                "marginBottom": "24px"
            },
            children=[
                # Chart 1: Donut Chart
                html.Div(
                    className="mission-card",
                    style={"padding": "16px 20px"},
                    children=[
                        dcc.Graph(
                            id='success-pie-chart',
                            config={"displayModeBar": False}
                        )
                    ]
                ),
                # Chart 2: Scatter Chart
                html.Div(
                    className="mission-card",
                    style={"padding": "16px 20px"},
                    children=[
                        dcc.Graph(
                            id='success-payload-scatter-chart',
                            config={"displayModeBar": True, "displaylogo": False}
                        )
                    ]
                )
            ]
        ),

        # 5. SECONDARY ANALYTICS ROW (Booster Reusability & Timeline Progression)
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "24px",
                "marginBottom": "24px"
            },
            children=[
                # Chart 3: Booster Matrix
                html.Div(
                    className="mission-card",
                    style={"padding": "16px 20px"},
                    children=[
                        dcc.Graph(
                            id='booster-bar-chart',
                            config={"displayModeBar": False}
                        )
                    ]
                ),
                # Chart 4: Flight Timeline Curve
                html.Div(
                    className="mission-card",
                    style={"padding": "16px 20px"},
                    children=[
                        dcc.Graph(
                            id='timeline-scatter-chart',
                            config={"displayModeBar": False}
                        )
                    ]
                )
            ]
        ),

        # 6. MISSION FLIGHT TELEMETRY LOG (DATA TABLE - Professional)
        html.Div(
            className="mission-card",
            style={"padding": "24px", "marginBottom": "24px"},
            children=[
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "16px"},
                    children=[
                        html.H3(
                            "FALCON 9 FLIGHT LOG & TELEMETRY MANIFEST",
                            style={
                                "margin": 0,
                                "fontFamily": "'Space Grotesk', sans-serif",
                                "fontSize": "1.05rem",
                                "fontWeight": "600",
                                "letterSpacing": "0.08em",
                                "color": "#F8FAFC"
                            }
                        ),
                        html.Span(
                            id="table-count-badge",
                            style={
                                "fontSize": "0.78rem",
                                "color": "#94A3B8",
                                "background": "rgba(255, 255, 255, 0.05)",
                                "padding": "4px 12px",
                                "borderRadius": "8px",
                                "border": "1px solid rgba(255, 255, 255, 0.08)"
                            },
                            children="Showing filtered launches"
                        )
                    ]
                ),
                dash_table.DataTable(
                    id='mission-table',
                    columns=[
                        {'name': 'Flight #', 'id': 'Flight Number'},
                        {'name': 'Launch Site', 'id': 'Launch Site'},
                        {'name': 'Booster Serial', 'id': 'Booster Version'},
                        {'name': 'Category', 'id': 'Booster Version Category'},
                        {'name': 'Payload (kg)', 'id': 'Payload Mass (kg)', 'type': 'numeric', 'format': {'specifier': ',.0f'}},
                        {'name': 'Landing Status', 'id': 'Landing Outcome'}
                    ],
                    style_as_list_view=True,
                    page_size=7,
                    sort_action="native",
                    style_table={"overflowX": "auto"},
                    style_header={
                        'backgroundColor': '#0B1120',
                        'color': '#94A3B8',
                        'fontWeight': '600',
                        'fontFamily': "'Space Grotesk', sans-serif",
                        'borderBottom': '1px solid rgba(255,255,255,0.12)',
                        'textAlign': 'left',
                        'padding': '14px 16px'
                    },
                    style_cell={
                        'backgroundColor': 'transparent',
                        'color': '#E2E8F0',
                        'fontFamily': "'Inter', sans-serif",
                        'fontSize': '0.86rem',
                        'padding': '12px 16px',
                        'borderBottom': '1px solid rgba(255,255,255,0.05)',
                        'textAlign': 'left'
                    },
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{class} = 1'},
                            'color': '#00E676',
                            'fontWeight': '600'
                        },
                        {
                            'if': {'filter_query': '{class} = 0'},
                            'color': '#FF5252'
                        }
                    ]
                )
            ]
        ),

        # 7. FOOTER
        html.Div(
            style={
                "textAlign": "center",
                "color": "#64748B",
                "fontSize": "0.8rem",
                "padding": "16px 0",
                "borderTop": "1px solid rgba(255, 255, 255, 0.05)"
            },
            children=[
                html.Span("IBM Applied Data Science Capstone Project • Falcon 9 Landing Prediction Pipeline • "),
                html.A(
                    "GitHub Repository",
                    href="https://github.com/QASIM07J/IBM-Applied-Data-Science-Capstone",
                    target="_blank",
                    style={"color": "#00E5FF", "textDecoration": "none"}
                ),
                html.Span(" • Created by Muhammad Qasim")
            ]
        )
    ]
)

# -----------------------------------------------------------------------------
# Common Graph Theme Layout
# -----------------------------------------------------------------------------
def get_chart_layout(title, height=360):
    return {
        "title": {
            "text": title,
            "font": {"family": "'Space Grotesk', sans-serif", "size": 15, "color": "#F1F5F9"},
            "x": 0.04,
            "y": 0.94
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": "'Inter', sans-serif", "color": "#94A3B8"},
        "margin": {"l": 55, "r": 25, "t": 55, "b": 45},
        "height": height,
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.28,
            "xanchor": "center",
            "x": 0.5,
            "font": {"size": 11, "color": "#94A3B8"}
        }
    }

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

# Callback: Update Payload Range Badge
@app.callback(
    Output('payload-range-badge', 'children'),
    Input('payload-slider', 'value')
)
def update_payload_badge(payload_range):
    return f"{payload_range[0]:,} kg – {payload_range[1]:,} kg"

# Callback: Update Dynamic KPI Cards & Mission Log Table
@app.callback(
    [
        Output('kpi-total-value', 'children'),
        Output('kpi-rate-value', 'children'),
        Output('kpi-rate-value', 'style'),
        Output('kpi-success-value', 'children'),
        Output('kpi-failure-value', 'children'),
        Output('kpi-payload-value', 'children'),
        Output('mission-table', 'data'),
        Output('table-count-badge', 'children')
    ],
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_kpis_and_table(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) & 
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    total_missions = len(filtered_df)
    if total_missions > 0:
        success_count = int(filtered_df['class'].sum())
        failure_count = total_missions - success_count
        success_rate = (success_count / total_missions) * 100
        avg_payload = filtered_df['Payload Mass (kg)'].mean()
        
        # Color conditional for success rate
        if success_rate >= 65:
            rate_color = "#00E676"
        elif success_rate >= 40:
            rate_color = "#00E5FF"
        else:
            rate_color = "#FFB800"

        rate_text = f"{success_rate:.1f}%"
        avg_payload_text = f"{avg_payload:,.0f} kg"
    else:
        success_count = 0
        failure_count = 0
        rate_text = "N/A"
        rate_color = "#64748B"
        avg_payload_text = "0 kg"

    table_data = filtered_df.to_dict('records')
    count_badge_text = f"Showing {total_missions} launches"

    rate_style = {"color": rate_color}

    return (
        f"{total_missions}",
        rate_text,
        rate_style,
        f"{success_count}",
        f"{failure_count}",
        avg_payload_text,
        table_data,
        count_badge_text
    )

# Callback 1: Success Pie/Donut Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        site_success = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = go.Figure(data=[go.Pie(
            labels=site_success['Launch Site'],
            values=site_success['class'],
            hole=0.62,
            textinfo='label+percent',
            marker=dict(
                colors=['#00E5FF', '#3B82F6', '#8B5CF6', '#EC4899'],
                line=dict(color='#07090E', width=2)
            ),
            hoverinfo='label+value+percent',
            hovertemplate="<b>%{label}</b><br>Successful Touchdowns: %{value}<br>Share: %{percent}<extra></extra>"
        )])
        fig.update_layout(
            get_chart_layout("TOTAL SUCCESSFUL TOUCHDOWNS BY LAUNCH SITE"),
            annotations=[dict(
                text="<b>ALL SITES</b><br><span style='font-size:11px;color:#94A3B8;'>Recovery Share</span>",
                x=0.5, y=0.5,
                font=dict(size=13, color='#F8FAFC', family="'Space Grotesk', sans-serif"),
                showarrow=False
            )]
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        class_counts = filtered_df['class'].value_counts().reset_index()
        class_counts.columns = ['class', 'count']
        class_counts['Outcome'] = class_counts['class'].map({1: 'Recovered', 0: 'Lost / Expended'})

        colors = [OUTCOME_COLOR_MAP.get(outcome, '#64748B') for outcome in class_counts['Outcome']]
        total_site_launches = class_counts['count'].sum()
        successes = filtered_df['class'].sum()
        pct = (successes / total_site_launches * 100) if total_site_launches > 0 else 0

        fig = go.Figure(data=[go.Pie(
            labels=class_counts['Outcome'],
            values=class_counts['count'],
            hole=0.62,
            textinfo='label+percent',
            marker=dict(colors=colors, line=dict(color='#07090E', width=2)),
            hovertemplate="<b>%{label}</b><br>Flights: %{value}<br>Ratio: %{percent}<extra></extra>"
        )])
        fig.update_layout(
            get_chart_layout(f"TOUCHDOWN RATIO: {entered_site}"),
            annotations=[dict(
                text=f"<b>{pct:.1f}%</b><br><span style='font-size:10px;color:#94A3B8;'>SUCCESS RATE</span>",
                x=0.5, y=0.5,
                font=dict(size=14, color='#00E676', family="'JetBrains Mono', monospace"),
                showarrow=False
            )]
        )
        return fig

# Callback 2: Payload vs. Success Scatter Chart (No Ticks / Crosses)
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) & 
        (spacex_df['Payload Mass (kg)'] <= high)
    ].copy()

    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    # Add gentle y-jitter for crystal-clear visualization without point collision
    np.random.seed(42)
    filtered_df['class_jitter'] = filtered_df['class'] + np.random.uniform(-0.04, 0.04, size=len(filtered_df))

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class_jitter',
        color='Booster Version Category',
        color_discrete_map=BOOSTER_COLOR_MAP,
        hover_data={
            'Flight Number': True,
            'Launch Site': True,
            'Payload Mass (kg)': ':.0f',
            'Booster Version': True,
            'Landing Outcome': True,
            'class_jitter': False
        }
    )

    fig.update_traces(
        marker=dict(size=11, opacity=0.88, line=dict(width=1, color='#FFFFFF')),
        hovertemplate="<b>Flight #%{customdata[0]}</b><br>Booster: %{customdata[3]}<br>Payload: %{x:,.0f} kg<br>Site: %{customdata[1]}<br>Status: <b>%{customdata[4]}</b><extra></extra>"
    )

    chart_title = (
        "PAYLOAD VS. OUTCOME CORRELATION (ALL SITES)" 
        if entered_site == 'ALL' 
        else f"PAYLOAD VS. OUTCOME ({entered_site})"
    )

    base_layout = get_chart_layout(chart_title)
    base_layout["xaxis"] = dict(
        title="Payload Mass (kg)",
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 255, 255, 0.1)",
        range=[-200, 10200]
    )
    # Professional Labels: No ticks, no crosses
    base_layout["yaxis"] = dict(
        title="Landing Outcome",
        tickvals=[0, 1],
        ticktext=["Lost / Expended", "Recovered / Landed"],
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 255, 255, 0.1)",
        range=[-0.25, 1.25]
    )

    fig.update_layout(base_layout)
    return fig

# Callback 3: Booster Reusability Matrix Bar Chart
@app.callback(
    Output('booster-bar-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_booster_matrix(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) & 
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    if selected_site := (entered_site != 'ALL'):
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    # Group by booster category & outcome
    booster_summary = filtered_df.groupby(['Booster Version Category', 'Landing Outcome']).size().reset_index(name='Count')

    fig = px.bar(
        booster_summary,
        x='Booster Version Category',
        y='Count',
        color='Landing Outcome',
        color_discrete_map=OUTCOME_COLOR_MAP,
        barmode='group'
    )

    base_layout = get_chart_layout("BOOSTER GENERATION RECOVERY EFFICIENCY")
    base_layout["xaxis"] = dict(
        title="Booster Version Category (Chronological)",
        gridcolor="rgba(255, 255, 255, 0.06)",
        categoryorder='array',
        categoryarray=['v1.0', 'v1.1', 'FT', 'B4', 'B5']
    )
    base_layout["yaxis"] = dict(
        title="Flight Count",
        gridcolor="rgba(255, 255, 255, 0.06)",
        dtick=2
    )

    fig.update_layout(base_layout)
    fig.update_traces(marker=dict(line=dict(width=1, color='#07090E')))
    return fig

# Callback 4: Flight Progression Timeline
@app.callback(
    Output('timeline-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_timeline_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) & 
        (spacex_df['Payload Mass (kg)'] <= high)
    ].sort_values('Flight Number').copy()

    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    if len(filtered_df) > 0:
        filtered_df['Cumulative Successes'] = filtered_df['class'].cumsum()
        filtered_df['Cumulative Launches'] = np.arange(1, len(filtered_df) + 1)
        filtered_df['Cumulative Success Rate'] = (
            filtered_df['Cumulative Successes'] / filtered_df['Cumulative Launches'] * 100
        )

        fig = go.Figure()
        
        # Cumulative Rate Line
        fig.add_trace(go.Scatter(
            x=filtered_df['Flight Number'],
            y=filtered_df['Cumulative Success Rate'],
            mode='lines+markers',
            name='Cumulative Recovery Rate %',
            line=dict(color='#00E5FF', width=3),
            marker=dict(
                size=7,
                color=filtered_df['class'].map({1: '#00E676', 0: '#FF3366'}),
                line=dict(width=1, color='#FFFFFF')
            ),
            hovertemplate="Flight #%{x}<br>Cumulative Success Rate: %{y:.1f}%<extra></extra>"
        ))

        base_layout = get_chart_layout("FALCON 9 HISTORICAL LEARNING CURVE")
        base_layout["xaxis"] = dict(
            title="Chronological Flight Number",
            gridcolor="rgba(255, 255, 255, 0.06)"
        )
        base_layout["yaxis"] = dict(
            title="Cumulative Success Rate (%)",
            gridcolor="rgba(255, 255, 255, 0.06)",
            range=[-5, 105]
        )
        fig.update_layout(base_layout)
        return fig
    else:
        fig = go.Figure()
        fig.update_layout(get_chart_layout("FALCON 9 HISTORICAL LEARNING CURVE"))
        return fig

# -----------------------------------------------------------------------------
# Run Application
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    if hasattr(app, 'run'):
        app.run(debug=True, port=8050)
    else:
        app.run_server(debug=True, port=8050)
