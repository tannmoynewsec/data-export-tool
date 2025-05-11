import streamlit as st
from login_screen import login_screen
from main_app import main_app

# --- App Entry Point ---
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login_screen()
else:
    main_app()
