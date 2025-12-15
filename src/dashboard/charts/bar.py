from __future__ import annotations

import pandas as pd
import altair as alt
import streamlit as st


def render_bar_chart(df: pd.DataFrame, category_col: str, value_col: str, title: str) -> None:
    if df.empty:
        st.write("No data.")
        return

    df = df.sort_values(value_col, ascending=False)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(f"{category_col}:N", sort="-y", title=None),
            y=alt.Y(f"{value_col}:Q", title=None),
            tooltip=[category_col, value_col],
        )
        .properties(height=260, title=title)
    )

    st.altair_chart(chart, use_container_width=True)
