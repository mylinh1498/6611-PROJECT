import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Descriptive Analysis")

# Sample data
data = {
    "Year": list(range(2014, 2025)),
    "Mathematics": [53, 54, 56, 54, 52, 51, 52, 50, 54, 55, 59],
    "Reading": [55, 53, 56, 57, 55, 53, 53, 54, 56, 57, 59],
}
df = pd.DataFrame(data).set_index("Year")

# Show data
st.subheader("Historical Data")
st.dataframe(df)

# Line chart
st.subheader("Trend Over Time")
st.line_chart(df)