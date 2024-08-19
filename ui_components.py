from imports import st
from data_fetch import process_data, fetch_trades


def display_ui():
    processed_data = process_data(
        fetch_trades()
        if "trades_data" not in st.session_state
        else st.session_state.trades_data
    )

    # Column selection and sorting
    sort_column = st.selectbox("Sort by", options=processed_data.columns, index=0)
    sort_ascending = st.checkbox("Ascending", value=True)
    if sort_column:
        processed_data = processed_data.sort_values(
            by=[sort_column], ascending=sort_ascending
        )

    # Column selection for display
    selected_columns = st.multiselect(
        "Select columns to display:",
        options=processed_data.columns.tolist(),
        default=processed_data.columns.tolist(),
    )
    st.dataframe(processed_data[selected_columns])
