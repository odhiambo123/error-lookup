import streamlit as st
import sqlite3
import pandas as pd

# Database Connection
def get_db():
    conn = sqlite3.connect('error_codes.db')
    return conn

# Initialize Database Table
conn = get_db()
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS error_catalog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_unit TEXT,
        test_type TEXT,
        chamber TEXT,
        error_code TEXT,
        description TEXT,
        remediation TEXT
    )
''')
conn.commit()
conn.close()

# Streamlit UI
st.title("🔍 Engineering Error Code Lookup")

# Sidebar for Adding Data
with st.sidebar:
    st.header("Add New Error")
    with st.form("add_error_form"):
        unit = st.text_input("Test Unit")
        test_type = st.text_input("Test Type")
        chamber = st.text_input("Chamber")
        code = st.text_input("Error Code")
        desc = st.text_area("Description")
        remedy = st.text_area("Remediation")
        submitted = st.form_submit_button("Submit")
        if submitted:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO error_catalog (test_unit, test_type, chamber, error_code, description, remediation) VALUES (?, ?, ?, ?, ?, ?)",
                           (unit, test_type, chamber, code, desc, remedy))
            conn.commit()
            conn.close()
            st.success("Entry added!")

    st.divider()
    st.header("Sync Database")
    with st.expander("Import / Export Data"):
        # Export Data
        conn = get_db()
        df_export = pd.read_sql_query("SELECT test_unit, test_type, chamber, error_code, description, remediation FROM error_catalog", conn)
        conn.close()
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Data (CSV)",
            data=csv,
            file_name='error_codes_backup.csv',
            mime='text/csv',
            help="Export the current database to a CSV file."
        )

        st.markdown("---")
        
        # Import Data
        st.write("**Import Data**")
        st.caption("Upload a CSV backup. Existing codes will be updated, new ones will be added.")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        if uploaded_file is not None:
            if st.button("🔄 Sync Data"):
                try:
                    df_import = pd.read_csv(uploaded_file)
                    df_import.fillna("", inplace=True)
                    conn = get_db()
                    cursor = conn.cursor()
                    sync_count = 0
                    for _, row in df_import.iterrows():
                        err_code = str(row.get('error_code', ''))
                        t_unit = str(row.get('test_unit', ''))
                        t_type = str(row.get('test_type', ''))
                        chamb = str(row.get('chamber', ''))
                        desc = str(row.get('description', ''))
                        remedy = str(row.get('remediation', ''))
                        
                        cursor.execute("SELECT id FROM error_catalog WHERE error_code=? AND test_unit=?", (err_code, t_unit))
                        result = cursor.fetchone()
                        
                        if result:
                            cursor.execute("""
                                UPDATE error_catalog 
                                SET test_type=?, chamber=?, description=?, remediation=? 
                                WHERE id=?
                            """, (t_type, chamb, desc, remedy, result[0]))
                        else:
                            cursor.execute("""
                                INSERT INTO error_catalog (test_unit, test_type, chamber, error_code, description, remediation) 
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (t_unit, t_type, chamb, err_code, desc, remedy))
                        sync_count += 1
                    conn.commit()
                    conn.close()
                    st.success(f"Successfully synced {sync_count} records!")
                except Exception as e:
                    st.error(f"Error during sync: {str(e)}")

# Search Interface
st.header("Search Database")
search_term = st.text_input("Enter Error Code or Unit Name:")

if search_term:
    conn = get_db()
    query = "SELECT * FROM error_catalog WHERE error_code LIKE ? OR test_unit LIKE ?"
    df = pd.read_sql_query(query, conn, params=(f'%{search_term}%', f'%{search_term}%'))
    conn.close()
    
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("No matches found.")