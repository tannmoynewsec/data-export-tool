import streamlit as st
import os

# Define user roles and demo credentials
USER_CREDENTIALS = {
    "admin": {"username": "admin", "password": "admin123", "role": "Admin"},
    "property_manager": {"username": "manager", "password": "manager123", "role": "Property Manager"},
    "finance_team": {"username": "finance", "password": "finance123", "role": "Finance Team"},
    "data_engineer": {"username": "engineer", "password": "engineer123", "role": "Data Engineer"}
}

def login_screen():    # If already authenticated, do not show login box, just return (main_app will be called from entry point)
    if st.session_state.get("authenticated"):
        return
        
    st.set_page_config(page_title="Login | Property Export Tool", page_icon="🔒", layout="centered")
    st.markdown("""
    <style>
    /*.login-box {background: #f9f9fb; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); padding: 2em; margin: 2em auto; max-width: 450px; display: flex; flex-direction: column; align-items: center;}*/
    .login-title {font-size: 1.6em; font-weight: 600; color: #235390; margin-bottom: 0.8em; letter-spacing: 0px; text-align: center;}
    
    /* Form styling */
    [data-testid="stForm"] {width: 100%;}    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(90deg, #4f8cff 0%, #235390 100%);
        color: white;
        font-weight: 600;
        border-radius: 4px;
        padding: 0.5em 0.8em !important;
        width: 100%;
        transition: background 0.2s;
        font-size: 1em !important;
        min-height: 45px !important;
        line-height: 1.2 !important;
        margin-top: 10px;
    }
    [data-testid="stFormSubmitButton"] button:hover {background: linear-gradient(90deg, #235390 0%, #4f8cff 100%);}
    
    /* Form input fields */
    div[data-baseweb="select"] {font-size: 1rem;}
    div[data-baseweb="input"] {font-size: 1rem;}
    .stSelectbox, .stTextInput {margin-bottom: 0.4rem;}
    [data-testid="stVerticalBlock"] {gap: 0.5rem !important;}
    div.row-widget.stSelectbox, div.row-widget.stTextInput {padding-bottom: 0.4rem;}
    /* Increase input field height */
    [data-baseweb="input"] input, [data-baseweb="select"] div {min-height: 40px !important;}
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for form inputs if not already present
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "password" not in st.session_state:
        st.session_state.password = ""
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = list(USER_CREDENTIALS.values())[0]["role"]
        
    def handle_login():
        # Get values from session state
        selected_role = st.session_state.selected_role
        username = st.session_state.username
        password = st.session_state.password
        
        # Check credentials
        for user in USER_CREDENTIALS.values():
            if user["role"] == selected_role and username == user["username"] and password == user["password"]:
                st.session_state["authenticated"] = True
                st.session_state["user_role"] = user["role"]
                return True
        return False
    
    # Login form with direct styling
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Property Management Export Tool </div>', unsafe_allow_html=True)
    with st.form("login_form"):
        role_options = [user["role"] for user in USER_CREDENTIALS.values()]
        st.selectbox("Select Role", role_options, key="selected_role")
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        
        # Handle Enter key and form submission with one button
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if handle_login():
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password for selected role.")
    
    st.markdown('</div>', unsafe_allow_html=True)
