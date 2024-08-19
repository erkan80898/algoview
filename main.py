# app.py
from imports import st, time
from data_fetch import fetch_trades
from ui_components import display_ui

st.title("Trade Information Dashboard")

# Fetch and process data, store in session state for reusability
if "trades_data" not in st.session_state:
    st.session_state.trades_data = fetch_trades()

display_ui()


def rerun_app():
    """Schedule app to rerun every 60 seconds."""
    time.sleep(60)
    st.experimental_rerun()


# Fetch data every 60 secs
if (
    "auto_fetch_timer" not in st.session_state
    or time.time() - st.session_state.auto_fetch_timer > 60
):
    st.session_state.auto_fetch_timer = time.time()  # Reset timer
    rerun_app()
