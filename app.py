import streamlit as st
import pandas as pd

# Load the Excel file
@st.cache_data
def load_data():
    file_path = "data/final.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")
    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

df = load_data()

# Detect possible column names
col_models = None
col_compatible = None
for c in df.columns:
    if "model" in c and col_models is None and "compatible" not in c:
        col_models = c
    if "compatible" in c:
        col_compatible = c

# Display logo and branding
st.image("data/logo.png", width=200)
st.markdown("### Powered by FM MOBILE PARTS")

st.title("📱 LCD Model Finder")

if not col_models or not col_compatible:
    st.error("Could not detect the correct columns in your Excel file. Please make sure it has 'Models' and 'Compatible Models' columns.")
else:
    # Input for searching compatible model
    query = st.text_input("Enter a compatible model to search:")

    if query:
        # Search in compatible models column
        results = df[df[col_compatible].astype(str).str.contains(query, case=False, na=False)]
        if not results.empty:
            st.success(f"✅ Found {len(results)} matching records.")
            st.write("### Compatible Original Models:")
            st.table(results[[col_models]].drop_duplicates().reset_index(drop=True))
        else:
            st.error("❌ No matching model found.")
