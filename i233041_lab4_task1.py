import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------
# Page Configuration
# ----------------------
st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Exploratory Data Analysis Interface")

# ----------------------
# Sidebar Controls
# ----------------------
with st.sidebar:
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# ----------------------
# Main Logic
# ----------------------
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        columns = df.columns.tolist()
        selected_col = st.sidebar.selectbox("Select Column for Analysis", columns)

        # ----------------------
        # Dataset Overview
        # ----------------------
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        st.subheader("Dataset Overview")
        rows, cols = df.shape
        st.write(f"**Rows:** {rows} | **Columns:** {cols}")

        st.write("**Data Types:**")
        st.write(df.dtypes)

        st.write("**Missing Values:**")
        st.write(df.isnull().sum())

        st.write("**Numerical Summary:**")
        st.write(df.describe())

        # ----------------------
        # Column Analysis & Visualization
        # ----------------------
        st.subheader(f"Analysis of Column: {selected_col}")
        col_data = df[selected_col]

        if pd.api.types.is_numeric_dtype(col_data):
            st.write("**Column Type:** Numerical")
            fig, ax = plt.subplots()
            sns.histplot(col_data.dropna(), kde=True, ax=ax)
            ax.set_title(f"Histogram of {selected_col}")
            ax.set_xlabel(selected_col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        else:
            st.write("**Column Type:** Categorical")
            fig, ax = plt.subplots()
            value_counts = col_data.value_counts()
            sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax)
            ax.set_title(f"Bar Chart of {selected_col}")
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("Please upload a CSV file to begin EDA.")
