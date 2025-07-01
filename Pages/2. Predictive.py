import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# --- Title ---
st.title("🏫 School Clustering & Prediction - Bogotá Saber 11")

# --- Load Data ---
csv_path = "C:\\Study document\\6611 Dataset\\MASTER- Ranking of Schools_ Based on Saber 11th Grade.xlsx - Append.csv"
df = pd.read_csv(csv_path)

# --- Columns ---
categorical_cols = ["Concession", "City", "Sector"]
numerical_cols = [
    "Enrolled students (last 3 years)",
    "Evaluated (last 3 years)",
    "Mathematics Index",
    "Natural Sciences Index",
    "Social and Citizenship Index",
    "Critical Reading Index",
    "English Index"
]

# --- Preprocessing ---
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])

cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", num_pipeline, numerical_cols),
    ("cat", cat_pipeline, categorical_cols)
])

X = preprocessor.fit_transform(df[categorical_cols + numerical_cols])

# --- Clustering ---
kmeans = KMeans(n_clusters=4, random_state=42)
df["Cluster"] = kmeans.fit_predict(X)

# --- PCA for Plotting ---
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X)
df["PC1"] = X_pca[:, 0]
df["PC2"] = X_pca[:, 1]

# --- User Input ---
st.sidebar.header("📥 Enter New School Data")
with st.sidebar.form("input_form"):
    user_input = {
        "Concession": st.selectbox("Concession", df["Concession"].dropna().unique()),
        "City": st.selectbox("City", df["City"].dropna().unique()),
        "Sector": st.selectbox("Sector", df["Sector"].dropna().unique()),
        "Enrolled students (last 3 years)": st.number_input("Enrolled students", value=100),
        "Evaluated (last 3 years)": st.number_input("Evaluated", value=90),
        "Mathematics Index": st.slider("Math Index", 0.0, 100.0, 50.0),
        "Natural Sciences Index": st.slider("Science Index", 0.0, 100.0, 50.0),
        "Social and Citizenship Index": st.slider("Social Index", 0.0, 100.0, 50.0),
        "Critical Reading Index": st.slider("Reading Index", 0.0, 100.0, 50.0),
        "English Index": st.slider("English Index", 0.0, 100.0, 50.0)
    }
    submitted = st.form_submit_button("Predict Cluster")

if submitted:
    user_df = pd.DataFrame([user_input])

    # Apply same preprocessing
    user_X = preprocessor.transform(user_df)

    # Predict cluster
    predicted_cluster = kmeans.predict(user_X)[0]
    st.success(f"🎯 Predicted Cluster: {predicted_cluster}")

    # Add to PCA for plotting
    user_pca = pca.transform(user_X)
    st.subheader("📍 Your School on Cluster Plot")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="PC1", y="PC2", hue="Cluster", palette="Set2", ax=ax)
    ax.scatter(user_pca[0, 0], user_pca[0, 1], color="black", label="Your School", marker="X", s=200)
    ax.legend()
    st.pyplot(fig)