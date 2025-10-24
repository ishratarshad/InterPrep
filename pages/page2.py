import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.header("Page 2 - Dashboard")

## --
st.subheader("Stats/Charts/Metrics/Viz?")

col1, col2, col3 = st.columns(3)

col1.metric("Interviews Prepped", 14)
col2.metric("Average Score", "78.1/100")
col3.metric("Success Rate", "86%")

st.subheader("Weekly progress")

data = pd.DataFrame({
    "Week": [f"Week {i}" for i in range(1, 6)],
    "Avg Interview Score": np.random.uniform(60, 95, 5),
})

chart = (
    alt.Chart(data)
    .mark_line(point=True)
    .encode(
        x=alt.X("Week", axis=alt.Axis(labelAngle=0)),
        y="Avg Interview Score"
    )
)

st.altair_chart(chart, use_container_width=True)
