import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize connection to Supabase
url: str = "https://sbmxhjnucuhuzyacjpir.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNibXhoam51Y3VodXp5YWNqcGlyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNjc2Mzg5MSwiZXhwIjoyMDMyMzM5ODkxfQ.xPXkE1OU9jYlBjOA29uRS7wSGofugzGzJoUguf6m0ZM"
supabase: Client = create_client(url, key)


def fetch_trades():
    data = supabase.table("trades").select("*").eq("status", "filled").execute()
    return data.data


def process_data(trades):
    # Process and structure data
    trades_list = []
    for trade in trades:
        trades_list.append(
            {
                "Symbol": trade["symbol"],
                "Asset Class": trade["asset_class"],
                "Asset ID": trade["asset_id"],
                "Created At": datetime.fromisoformat(
                    trade["created_at"].rstrip("Z")
                ).strftime("%d-%m-%Y %H:%M:%S"),
                "Filled At": datetime.fromisoformat(
                    trade["filled_at"].rstrip("Z")
                ).strftime("%d-%m-%Y %H:%M:%S"),
                "Filled Avg Price": float(trade["filled_avg_price"]),
                "Filled Qty": float(trade["filled_qty"]),
                "Order Type": trade["order_type"],
                "Side": trade["side"],
                "Status": trade["status"],
                "Date/Time": datetime.fromisoformat(
                    trade["timestamp"].rstrip("Z")
                ).strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    return pd.DataFrame(trades_list)


st.title("Trade Information Dashboard")

# Column selector
if "selected_columns" not in st.session_state:
    st.session_state.selected_columns = [
        "Asset Class",
        "Symbol",
        "Filled At",
        "Filled Avg Price",
        "Side",
        "Date/Time",
    ]

all_columns = [
    "Asset Class",
    "Asset ID",
    "Client Order ID",
    "Created At",
    "Filled At",
    "Filled Avg Price",
    "Filled Qty",
    "Symbol",
    "Order Type",
    "Side",
    "Status",
    "Date/Time",
]
selected_columns = st.multiselect(
    "Select columns to display:", all_columns, default=st.session_state.selected_columns
)

# Fetching trades data
if st.button("Refresh Data"):
    trades_data = fetch_trades()
    if trades_data:
        processed_data = process_data(trades_data)
        st.session_state.selected_columns = selected_columns  # Update session state
        st.dataframe(processed_data[selected_columns])  # Display only selected columns

        # Analytics and Visualizations
        st.subheader("Analytics and Visualizations")

        # Total volume by asset class
        volume_by_asset = processed_data.groupby("Asset Class")["Filled Qty"].sum()
        fig_volume = px.bar(volume_by_asset, title="Total Volume by Asset Class")
        st.plotly_chart(fig_volume)

        # Average price by symbol
        avg_price_by_symbol = processed_data.groupby("Symbol")[
            "Filled Avg Price"
        ].mean()
        fig_avg_price = px.line(
            avg_price_by_symbol,
            title="Average Price by Symbol",
            labels={"value": "Average Price", "index": "Symbol"},
        )
        st.plotly_chart(fig_avg_price)

        # Distribution of trade types
        trade_type_counts = processed_data["Order Type"].value_counts()
        fig_trade_type = px.pie(
            trade_type_counts,
            values=trade_type_counts.values,
            names=trade_type_counts.index,
            title="Distribution of Trade Types",
        )
        st.plotly_chart(fig_trade_type)

    else:
        st.error("Failed to fetch data")
