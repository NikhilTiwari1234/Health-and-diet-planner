import streamlit as st
from utils.data_manager import create_user, authenticate_user
import re

def show():
    st.markdown('<h1 class="main-header">🔐 Welcome to VitalPlan</h1>', unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        show_login()
    
    with tab2:
        show_signup()
    
    # Back to home
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()

def show_login():
    st.markdown('<h3 style="color: #2E7D32; text-align: center;">Login to Your Account</h3>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submitted = st.form_submit_button("🔓 Login", type="primary", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("Please fill in all fields")
                else:
                    success, message = authenticate_user(username, password)
                    
                    if success:
                        st.session_state.user_logged_in = True
                        st.session_state.username = username
                        st.success(f"Welcome back, {username}!")
                        
                        # Check if user has a profile
                        from utils.data_manager import get_user_profile
                        profile, _ = get_user_profile(username)
                        
                        if profile:
                            st.session_state.page = 'dashboard'
                        else:
                            st.session_state.page = 'assessment'
                        
                        st.rerun()
                    else:
                        st.error(message)

def show_signup():
    st.markdown('<h3 style="color: #2E7D32; text-align: center;">Create New Account</h3>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            # Terms checkbox
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            submitted = st.form_submit_button("📝 Create Account", type="primary", use_container_width=True)
            
            if submitted:
                # Validation
                errors = []
                
                if not username or not email or not password or not confirm_password:
                    errors.append("Please fill in all fields")
                
                if len(username) < 3:
                    errors.append("Username must be at least 3 characters long")
                
                if not re.match(r'^[a-zA-Z0-9_]+$', username):
                    errors.append("Username can only contain letters, numbers, and underscores")
                
                if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
                    errors.append("Please enter a valid email address")
                
                if len(password) < 6:
                    errors.append("Password must be at least 6 characters long")
                
                if password != confirm_password:
                    errors.append("Passwords do not match")
                
                if not terms_accepted:
                    errors.append("Please accept the terms and conditions")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Create user
                    success, message = create_user(username, password, email)
                    
                    if success:
                        st.success("Account created successfully! Please login to continue.")
                        st.balloons()
                    else:
                        st.error(message)
    
    # Additional info
    st.markdown("""
    <div style="background: #F1F8E9; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
        <h4 style="color: #2E7D32;">Why Sign Up?</h4>
        <ul style="color: #388E3C;">
            <li>🎯 Get personalized health recommendations</li>
            <li>📊 Track your progress over time</li>
            <li>🥗 Receive custom diet plans</li>
            <li>💪 Access tailored exercise routines</li>
            <li>🔒 Your data is secure and private</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
