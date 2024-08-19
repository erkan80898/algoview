from datetime import datetime
from imports import pd, init_supabase


def fetch_trades():
    supabase = init_supabase()
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
