import streamlit as st
import pandas as pd
from datetime import datetime
import io
from dotenv import load_dotenv

st.set_page_config(page_title="Property Management Data Export Tool", page_icon="🏢", layout="wide")

st.markdown("""
<style>
/* Modernize table and button look */
[data-testid="stDataEditorGrid"] {
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    background: #f9f9fb;
}
[data-testid="stButton"] button {
    border-radius: 6px;
    background: linear-gradient(90deg, #4f8cff 0%, #235390 100%);
    color: white;
    font-weight: 600;
    padding: 0.5em 1.5em;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    box-shadow: 0 1px 4px rgba(79,140,255,0.10);
    transition: background 0.2s;
}
[data-testid="stButton"] button:hover {
    background: linear-gradient(90deg, #235390 0%, #4f8cff 100%);
}
[data-testid="stDownloadButton"] button {
    border-radius: 6px;
    background: #e6f0ff;
    color: #235390;
    font-weight: 600;
    border: 1px solid #4f8cff;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}
[data-testid="stDownloadButton"] button:hover {
    background: #4f8cff;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🏢 Property Management Data Export Tool")
st.caption("A modern, streamlined interface for property data review, editing, and export.")

# Load environment variables from .env file
load_dotenv()

# Dummy data for Newsec Sweden property (10 records, all columns visible, with 'Edited' checkbox)
initial_data = [
    {
        "Property ID": 1001 + i,
        "Property Name": f"Newsec Sweden HQ {i+1}",
        "Unit Count": 50 + i,
        "Occupancy Rate": round(0.98 - 0.01 * i, 2),
        "Total Rent": 120000.00 + 1000 * i,
        "Comment": f"All units occupied {i+1}",
        "Last Modified By": "admin",
        "Edited": False
    }
    for i in range(10)
]

df = pd.DataFrame(initial_data)

st.write("Edit property data, add comments, and export to Excel/CSV.")

# Editable grid with all columns visible, including 'Edited' checkbox
df_edit = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="property_grid"
)

# --- Modern top-right action bar ---
actions_col1, actions_col2, actions_col3 = st.columns([6,1,1])
with actions_col2:
    export_excel = st.button("Export to Excel", use_container_width=True)
with actions_col3:
    export_csv = st.button("Export to CSV", use_container_width=True)

# Save button (top right, styled)
with actions_col3:
    save = st.button("Save", use_container_width=True, type="primary")

# Handle export actions
if export_excel:
    output = io.BytesIO()
    df_edit.to_excel(output, index=False)
    output.seek(0)
    ts = datetime.now().strftime("%Y-%m")
    st.download_button(
        label="Download Excel",
        data=output,
        file_name=f"property_export_{ts}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key="download_excel_btn"
    )
if export_csv:
    csv = df_edit.to_csv(index=False).encode('utf-8')
    ts = datetime.now().strftime("%Y-%m")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"property_export_{ts}.csv",
        mime="text/csv",
        use_container_width=True,
        key="download_csv_btn"
    )

# Save to Synapse (single button, no expander, no password input in UI)
if save:
    import os
    import pyodbc
    # Get connection details from environment variables
    env = os.getenv("SYNAPSE_ENV", "dev")
    ndw_server = os.getenv("SYNAPSE_SERVER", f"weu-ndw-{env}-asa.sql.azuresynapse.net")
    ndw_username = os.getenv("SYNAPSE_USERNAME", "NDWAdminASA")
    ndw_database_name = os.getenv("SYNAPSE_DATABASE", f"weu_ndw_{env}")
    ndw_password = os.getenv("SYNAPSE_PASSWORD")
    table_name = os.getenv("SYNAPSE_TABLE", "[dbo].[PropertyExport]")
    if not ndw_password:
        st.error("SYNAPSE_PASSWORD environment variable not set.")
    else:
        try:
            conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={ndw_server};DATABASE={ndw_database_name};UID={ndw_username};PWD={ndw_password}")
            cursor = conn.cursor()
            # Create table if not exists (autocommit ON for DDL)
            conn.autocommit = True
            cursor.execute(f"""
            IF OBJECT_ID('{table_name}', 'U') IS NULL
            CREATE TABLE {table_name} (
                [Property ID] INT,
                [Property Name] NVARCHAR(255),
                [Unit Count] INT,
                [Occupancy Rate] FLOAT,
                [Total Rent] FLOAT,
                [Comment] NVARCHAR(255),
                [Last Modified By] NVARCHAR(255),
                [Edited] BIT
            )
            """)
            # Switch back to manual commit for DML
            conn.autocommit = False
            cursor.execute(f"DELETE FROM {table_name}")
            conn.commit()
            for _, row in df_edit.iterrows():
                cursor.execute(f"""
                    INSERT INTO {table_name} ([Property ID], [Property Name], [Unit Count], [Occupancy Rate], [Total Rent], [Comment], [Last Modified By], [Edited])
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, int(row["Property ID"]), str(row["Property Name"]), int(row["Unit Count"]), float(row["Occupancy Rate"]), float(row["Total Rent"]), str(row["Comment"]), str(row["Last Modified By"]), bool(row["Edited"]))
            conn.commit()
            conn.close()
            st.success(f"Data saved to Synapse table {table_name}.")
        except Exception as e:
            st.error(f"Failed to save to Synapse: {e}")
