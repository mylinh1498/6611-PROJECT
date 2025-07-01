import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bogotá School Insights", layout="wide")

# === 1. Load Data ===
@st.cache_data
def load_data():
    file_path = "C:\\Study document\\6611 Dataset\\MASTER- Ranking of Schools_ Based on Saber 11th Grade.xlsx - Append.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

st.title("📊 Bogotá Saber 11 School Performance Explorer")

# === 2. Clean Up Columns ===
df.columns = df.columns.str.strip()

# === 3. Filters ===
st.sidebar.header("🔎 Filter")
year_filter = st.sidebar.slider("Select Year Range", 2014, 2024, (2014, 2024))
filtered_df = df[df["Year"].between(year_filter[0], year_filter[1])]

# === 4. Basic Stats ===
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🏫 Public Schools", (filtered_df["Sector"] == "OFFICIAL").sum())
with col2:
    st.metric("🏫 Private Schools", (filtered_df["Sector"] == "PRIVATE").sum())
with col3:
    st.metric("🏫 Concession Schools", (filtered_df["Concession"] == "Yes").sum())

# === 5. Ranking Count ===
st.subheader("📚 School Ranking Distribution")
ranking_counts = filtered_df["Ranking"].value_counts().sort_index()
st.bar_chart(ranking_counts)

# === 6. Performance Scores ===
st.subheader("📈 Mathematics Index Summary")
col4, col5 = st.columns(2)
with col4:
    avg_score = filtered_df["Mathematics Index"].mean()
    st.metric("Average Score", f"{avg_score:.3f}")
with col5:
    max_score = filtered_df["Mathematics Index"].max()
    top_school = filtered_df.loc[filtered_df["Mathematics Index"].idxmax(), "Name of Establishment"]
    st.metric("Highest Score", f"{max_score:.3f} ({top_school})")

# === 7. Yearly School Count ===
st.subheader("📅 Schools Count by Year")
yearly_counts = filtered_df.groupby("Year")["Name of Establishment"].count()
st.line_chart(yearly_counts)

# === 8. Trends by Subject Index (if other subjects exist) ===
if "Critical Reading Index" in df.columns:
    st.subheader("📘 Subject Index Trends Over Years")
    subject_options = [
        col for col in df.columns if "Index" in col and col != "Total Index"
    ]
    selected_subject = st.selectbox("Select Subject", subject_options)

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=filtered_df, x="Year", y=selected_subject, hue="Sector", estimator="mean", ci=None, ax=ax)
    plt.title(f"{selected_subject} Over Time")
    st.pyplot(fig)

# === 9. Raw Data View ===
with st.expander("🧾 Show Raw Data"):
    st.dataframe(filtered_df)