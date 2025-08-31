import streamlit as st
import pandas as pd
from pages.landing import show as show_landing
from pages.auth import show as show_auth  
from pages.assessment import show as show_assessment
from pages.dashboard import show as show_dashboard
from utils.data_manager import initialize_data_files

# Initialize data files
initialize_data_files()

# Configure page
st.set_page_config(
    page_title="VitalPlan - Virtual Health & Diet Planner",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E7D32;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .sub-header {
        text-align: center;
        color: #388E3C;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #2E7D32;
    }
    .metric-card {
        background: #F1F8E9;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #81C784;
    }
    .nav-button {
        background: #2E7D32;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .success-message {
        background: #E8F5E8;
        color: #2E7D32;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #4CAF50;
    }
    .error-message {
        background: #FFEBEE;
        color: #C62828;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #F44336;
    }
</style>
""", unsafe_allow_html=True)

# Navigation logic
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Page routing
if st.session_state.page == 'landing':
    show_landing()
elif st.session_state.page == 'auth':
    show_auth()
elif st.session_state.page == 'assessment':
    if st.session_state.user_logged_in:
        show_assessment()
    else:
        st.error("Please log in to access this page.")
        show_landing()
elif st.session_state.page == 'dashboard':
    if st.session_state.user_logged_in:
        show_dashboard()
    else:
        st.error("Please log in to access this page.")
        show_landing()
