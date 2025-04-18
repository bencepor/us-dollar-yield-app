import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Title
st.title("US Dollar Index (UUP) vs. 10-Year US Yield")

# Define date range
start_date = "2023-01-01"
end_date = pd.to_datetime("today").strftime("%Y-%m-%d")

# Fetch data
dxy = yf.download("DX-Y.NYB", start=start_date, end=end_date)
us10y = yf.download("^TNX", start=start_date, end=end_date)

# Flatten multi-index columns (important!)
dxy.columns = dxy.columns.get_level_values(0)
us10y.columns = us10y.columns.get_level_values(0)

# Drop missing rows
dxy = dxy.dropna(subset=["Close"])
us10y = us10y.dropna(subset=["Close"])

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(
        x=dxy.index,
        y=dxy["Close"],
        name="US Dollar Index",
        line=dict(color="firebrick"),
    ),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(
        x=us10y.index,
        y=us10y["Close"] / 10,
        name="10-Year Yield",
        line=dict(color="navy"),
    ),
    secondary_y=True,
)

# Update layout
fig.update_layout(
    title="US Dollar Index vs. 10-Year Yield",
    xaxis_title="Date",
    plot_bgcolor='#f4ece1',
    paper_bgcolor='#f4ece1',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    hovermode="x unified"
)

# Update y-axes
fig.update_yaxes(title_text="US Dollar Index", range=[100, 110], secondary_y=False)
fig.update_yaxes(title_text="10-Year Yield (%)", range=[0.3, 0.5], secondary_y=True)

st.plotly_chart(fig, use_container_width=True)