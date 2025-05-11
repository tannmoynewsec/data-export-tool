# filepath: c:\Users\se-tansan01\OneDrive - Stronghold Invest AB\Documents\github-repo\data-export-tool\app\main_app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import io
from dotenv import load_dotenv
import os
import pyodbc

def main_app():
    # Show login screen if not authenticated
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        from login_screen import login_screen
        login_screen()
        return

    st.set_page_config(page_title="Property Management Data Export Tool", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")
    
    st.markdown("""
    <style>
    /* Main layout optimizations */
    section[data-testid="stSidebar"] {display: none;}
    .stApp {max-width: 100vw; padding: 0 1rem;}
    .main {padding: 0.3rem 0 0.5rem 0;}
    .block-container {max-width: 100%; padding-top: 0.6rem; padding-bottom: 0;}    /* Header and title styling */
    header[data-testid="stHeader"] {background: white; z-index: 999; height: auto; padding-top: 0.5rem; padding-bottom: 0.5rem; margin-bottom: 0.3rem;}
    .page-title {font-size: 1.1em; font-weight: 600; margin-bottom: 0.5em; margin-top: 0.5em !important;}
    
    /* Content styling */
    [data-testid="stDataEditorGrid"] {border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); background: #f9f9fb; max-height: calc(100vh - 180px);}
    
    /* Button styling */
    [data-testid="stButton"] button {
        border-radius: 4px; 
        background: linear-gradient(90deg, #4f8cff 0%, #235390 100%); 
        color: white; 
        font-weight: 600; 
        padding: 0.2em 0.6em !important; 
        margin: 0 !important; 
        box-shadow: 0 1px 4px rgba(79,140,255,0.10); 
        transition: background 0.2s;
        min-height: 0 !important;
        line-height: 1.2 !important;
        font-size: 0.8em !important;
    }
    [data-testid="stButton"] button:hover {background: linear-gradient(90deg, #235390 0%, #4f8cff 100%);}
    [data-testid="stDownloadButton"] button {
        border-radius: 4px; 
        background: #e6f0ff; 
        color: #235390; 
        font-weight: 600; 
        border: 1px solid #4f8cff; 
        padding: 0.2em 0.6em !important; 
        margin: 0 !important;
        min-height: 0 !important;
        line-height: 1.2 !important;
        font-size: 0.8em !important;
    }
    [data-testid="stDownloadButton"] button:hover {background: #4f8cff; color: white;}
      /* Component containers */
    .compact-button button {padding: 0.2em 0.6em !important; font-size: 0.8em !important; min-height: 0 !important;}
    
    /* Tooltip alignment fixes */
    [data-baseweb="tooltip"],
    [data-baseweb="popover"] {
        text-align: center !important;
        align-items: center !important;
    }
    
    div[data-testid="stToolbar"] {
        visibility: hidden;
    }
    
    .actions-container {
        margin-top: 0.3em; 
        padding: 0.2em 0; 
        border-top: 1px solid #eee; 
        position: sticky; 
        bottom: 0px; 
        background: white;
        z-index: 100;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
        margin-bottom: 0px;
    }
    .logout-container {position: absolute; top: 0.5rem; right: 1.5rem; z-index: 100;}
    
    /* Minimize excess padding and margins while preserving Streamlit's vertical rhythm */
    h1, h2, h3, p {margin: 0.15em 0 !important; padding: 0 !important;}
    .stMarkdown {margin: 0.3em 0 !important;}
    .element-container {margin-bottom: 0.3em !important; padding-top: 0.1em !important;}
    
    /* Make the action buttons row more compact */
    .stHorizontalBlock {gap: 0.2rem !important;}
    div[data-testid="column"] {padding: 0 !important; margin: 0 !important;}
    </style>
    """, unsafe_allow_html=True)
    
    # Header area with title and logout button using Streamlit's default alignment
    header_col1, header_col2 = st.columns([6.5, 1.5])
    
    with header_col1:
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 0.1rem; padding: 0;">
            <h2 class="page-title" style="margin: 0; font-size: 1.1em; color: #235390;">🏢 Property Management Export Tool</h2>
            <span style="color: #666; font-size: 0.8em; margin-left: 1rem;">Welcome, {}</span>
        </div>
        """.format(st.session_state.get('username', 'user')), unsafe_allow_html=True)
    
    with header_col2:
        logout_container = st.container()
        with logout_container:
            st.markdown('<div style="padding-right: 1rem;">', unsafe_allow_html=True)
            if st.button("Logout", key="logout_btn", help="Sign out", use_container_width=False):
                st.session_state.clear()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Load data
    load_dotenv()
    
    # Define database connection parameters
    env = os.getenv("SYNAPSE_ENV", "dev")
    ndw_server = os.getenv("SYNAPSE_SERVER", f"weu-ndw-{env}-asa.sql.azuresynapse.net")
    ndw_username = os.getenv("SYNAPSE_USERNAME", "NDWAdminASA")
    ndw_database_name = os.getenv("SYNAPSE_DATABASE", f"weu_ndw_{env}")
    ndw_password = os.getenv("SYNAPSE_PASSWORD")
    table_name = os.getenv("SYNAPSE_TABLE", "[dbo].[PropertyExport]")
      # Default data in case we can't load from database
    # Generate 10 records for April 2025 and 10 for May 2025
    initial_data = []
    
    # April 2025 records
    for i in range(10):
        initial_data.append({
            "Year-Month": "2025-04",
            "Property ID": 1001 + i,
            "Property Name": f"Newsec Sweden HQ {i+1}",
            "Unit Count": 50 + i,
            "Occupancy Rate": round(0.98 - 0.01 * i, 2),
            "Total Rent": 120000.00 + 1000 * i,
            "Comment": f"April data for unit {i+1}",
            "Last Modified By": st.session_state.get("username", "admin"),
            "Edited": False
        })
    
    # May 2025 records
    for i in range(10):
        initial_data.append({
            "Year-Month": "2025-05",
            "Property ID": 1001 + i,
            "Property Name": f"Newsec Sweden HQ {i+1}",
            "Unit Count": 52 + i,  # Slightly different data for May
            "Occupancy Rate": round(0.99 - 0.01 * i, 2),
            "Total Rent": 122000.00 + 1000 * i,
            "Comment": f"May data for unit {i+1}",
            "Last Modified By": st.session_state.get("username", "admin"),
            "Edited": False
        })
    
    
    # Try to load data from Synapse if available
    df = pd.DataFrame(initial_data)  # Default to initial data
    
    if ndw_password:
        try:
            conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={ndw_server};DATABASE={ndw_database_name};UID={ndw_username};PWD={ndw_password}")            # Check if the table exists
            cursor = conn.cursor()
            table_exists_query = f"""
                IF OBJECT_ID('{table_name}', 'U') IS NOT NULL
                    SELECT 1
                ELSE
                    SELECT 0
            """
            cursor.execute(table_exists_query)
            table_exists = cursor.fetchone()[0]
            cursor.close()  # Close the cursor after fetching the result
            
            # If table exists, load data from it
            if table_exists == 1:
                # Use a new connection for read_sql to avoid cursor conflicts
                df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
                st.toast(f"Data loaded successfully", icon="✅")
            
            conn.close()
        except Exception as e:
            st.error(f"Failed to connect to database: {e}")
    
    # Add filtering capability at the top
    st.markdown("<h3 style='font-size: 1rem; margin-bottom: 0.5rem;'>Filter Data</h3>", unsafe_allow_html=True)
    filter_cols = st.columns([1, 1, 3])
    
    # Year-Month filter 
    with filter_cols[0]:
        available_months = ["All"] + sorted(df["Year-Month"].unique().tolist())
        selected_month = st.selectbox("Year-Month", available_months, key="month_filter")
    
    # Property ID filter
    with filter_cols[1]:
        available_properties = ["All"] + sorted([str(id) for id in df["Property ID"].unique().tolist()])
        selected_property = st.selectbox("Property ID", available_properties, key="property_filter")
    
    # Apply filters to dataframe
    filtered_df = df.copy()
    if selected_month != "All":
        filtered_df = filtered_df[filtered_df["Year-Month"] == selected_month]
    if selected_property != "All":
        filtered_df = filtered_df[filtered_df["Property ID"] == int(selected_property)]
      # Information about filters applied
    with filter_cols[2]:
        if selected_month != "All" or selected_property != "All":
            st.markdown(f"<p style='color: #4f8cff; padding-top: 1.7rem;'><strong>Filtered:</strong> Showing {len(filtered_df)} of {len(df)} records</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #666; padding-top: 1.7rem;'>No filters applied</p>", unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.3;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.8em; color: #666; margin-bottom: 0.2em;'>Edit property data, add comments, check the 'Edited' box to mark changes, then Export/Save.</p>", unsafe_allow_html=True)
    
    # Store the original dataframe for comparison
    if "original_df" not in st.session_state:
        st.session_state.original_df = filtered_df.copy()
    
    # Data editor with frozen "Edited" column
    df_edit = st.data_editor(
        filtered_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="property_grid",
        height=None,  # This lets the grid adapt to available space
        disabled=["Property ID", "Last Modified By"],  # Disable editing for these columns
        column_config={
            "Edited": st.column_config.CheckboxColumn(
                "Edited",
                help="Check this box to mark a row as edited before saving",
                default=False,
                required=True
            ),
            "Year-Month": st.column_config.TextColumn(
                "Year-Month",
                help="Year and month in YYYY-MM format",
                validate="^[0-9]{4}-[0-9]{2}$"
            )
        },
        column_order=["Year-Month", "Property ID", "Property Name", "Unit Count", 
                      "Occupancy Rate", "Total Rent", "Comment", "Last Modified By", "Edited"]
    )
    
    # Add a note about marking edits
    st.markdown("<p style='font-size: 0.75em; color: #ff9900; margin-top: 0.2em;'>⚠️ Important: Check the 'Edited' box for any rows you've modified before saving.</p>", unsafe_allow_html=True)
    
    # --- Action bar: Compact Export and Save buttons at the bottom ---
    st.markdown('<div class="actions-container">', unsafe_allow_html=True)
    # Use a more compact layout with fixed width columns
    act_col1, act_col2, act_col3, act_col4, act_col5 = st.columns([5, 1, 1, 1, 2])
    
    with act_col1:
        st.markdown("<p style='font-weight: 600; margin-top: 2px; white-space: nowrap; font-size: 0.75em;'>Actions:</p>", unsafe_allow_html=True)
    
    with act_col2:
        export_excel = st.button("📊 Excel", key="excel_btn", help="Export to Excel file", use_container_width=True)
    
    with act_col3:
        export_csv = st.button("📄 CSV", key="csv_btn", help="Export to CSV file", use_container_width=True)
    
    with act_col4:
        save = st.button("💾 Save", key="save_btn", type="primary", help="Save to Azure Synapse", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
      # Handle export and save actions    # Handle excel export
    if export_excel:
        # Display message that export is happening without data refresh
        st.info("Exporting data to Excel without refreshing. Changes will not be saved to the database.")
        
        # Create the Excel export from the current data without refreshing
        output = io.BytesIO()
        # Use the filtered data for export without any refresh
        df_edit.to_excel(output, index=False)
        output.seek(0)
        ts = datetime.now().strftime("%Y-%m")
          # Download inline with action buttons
        dl_col1, dl_col2, dl_col3, dl_col4, dl_col5 = st.columns([3, 4, 1, 1, 1])
        with dl_col2:
            st.markdown('<div class="compact-button">', unsafe_allow_html=True)
            st.download_button(
                label="📊 Download Excel",
                data=output,
                file_name=f"property_export_{ts}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                help="Download data as Excel file without refreshing",
                key="download_excel_btn"
            )
            st.markdown('</div>', unsafe_allow_html=True)
      # Handle CSV export
    if export_csv:
        # Display message that export is happening without data refresh
        st.info("Exporting data to CSV without refreshing. Changes will not be saved to the database.")
        
        # Create the CSV export from the current data without refreshing
        csv = df_edit.to_csv(index=False).encode('utf-8')
        ts = datetime.now().strftime("%Y-%m")
          # Download inline with action buttons
        dl_col1, dl_col2, dl_col3, dl_col4, dl_col5 = st.columns([3, 4, 1, 1, 1])
        with dl_col2:
            st.markdown('<div class="compact-button">', unsafe_allow_html=True)
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name=f"property_export_{ts}.csv",
                mime="text/csv",
                use_container_width=True,
                help="Download data as CSV file without refreshing",
                key="download_csv_btn"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    if save:
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
                conn.autocommit = True
                cursor.execute(f"""
                IF OBJECT_ID('{table_name}', 'U') IS NULL
                CREATE TABLE {table_name} (
                    [Year-Month] NVARCHAR(7),
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
                conn.autocommit = False
                
                # Process each row in the data editor
                updates_count = 0
                inserts_count = 0
                
                for _, row in df_edit.iterrows():
                    # Check if record exists
                    cursor.execute(f"""
                        SELECT COUNT(*) FROM {table_name} 
                        WHERE [Year-Month] = ? AND [Property ID] = ?                    """, str(row["Year-Month"]), int(row["Property ID"]))
                    record_exists = cursor.fetchone()[0] > 0
                    
                    if record_exists and row["Edited"]:
                        # Update existing record if it was edited and update the Last Modified By field
                        current_user = st.session_state.get("username", "admin")
                        
                        cursor.execute(f"""
                            UPDATE {table_name} 
                            SET [Property Name] = ?, 
                                [Unit Count] = ?, 
                                [Occupancy Rate] = ?, 
                                [Total Rent] = ?, 
                                [Comment] = ?, 
                                [Last Modified By] = ?, 
                                [Edited] = ?
                            WHERE [Year-Month] = ? AND [Property ID] = ?                        """, str(row["Property Name"]), int(row["Unit Count"]), 
                            float(row["Occupancy Rate"]), float(row["Total Rent"]), 
                            str(row["Comment"]), current_user,  # Update with current username
                            bool(row["Edited"]), str(row["Year-Month"]), int(row["Property ID"]))
                        
                        if cursor.rowcount > 0:
                            updates_count += 1
                    
                    elif not record_exists:
                        # Insert if it's a new record
                        current_user = st.session_state.get("username", "admin")
                        
                        cursor.execute(f"""
                            INSERT INTO {table_name} ([Year-Month], [Property ID], [Property Name], [Unit Count], [Occupancy Rate], [Total Rent], [Comment], [Last Modified By], [Edited])
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, str(row["Year-Month"]), int(row["Property ID"]), str(row["Property Name"]), 
                            int(row["Unit Count"]), float(row["Occupancy Rate"]), float(row["Total Rent"]), 
                            str(row["Comment"]), current_user, bool(row["Edited"]))
                        
                        inserts_count += 1
                
                conn.commit()
                conn.close()
                
                # Show appropriate success message
                if updates_count > 0 and inserts_count > 0:
                    st.success(f"Data saved to {table_name}: {updates_count} records updated, {inserts_count} new records added.")
                elif updates_count > 0:
                    st.success(f"Data saved to {table_name}: {updates_count} records updated.")
                elif inserts_count > 0:
                    st.success(f"Data saved to {table_name}: {inserts_count} new records added.")
                else:
                    st.info(f"No changes needed to save to {table_name}.")
            except Exception as e:
                st.error(f"Failed to save to Synapse: {e}")
