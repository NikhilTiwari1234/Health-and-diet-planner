import streamlit as st

def show():
    # Hero section
    st.markdown('<h1 class="main-header">🏥 VitalPlan</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your Virtual Health & Diet Planner</p>', unsafe_allow_html=True)
    
    # Main introduction
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%); border-radius: 15px; margin: 2rem 0;">
            <h3 style="color: #2E7D32; margin-bottom: 1rem;">Transform Your Health Journey</h3>
            <p style="font-size: 1.1rem; color: #388E3C; line-height: 1.6;">
                Get personalized diet and exercise recommendations based on your unique profile, 
                goals, and preferences. Start your journey to a healthier you today!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("---")
    st.markdown('<h2 style="text-align: center; color: #2E7D32; margin: 2rem 0;">🌟 What VitalPlan Offers</h2>', unsafe_allow_html=True)
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Health Analytics</h4>
            <ul>
                <li>BMI & BMR calculations</li>
                <li>Target calorie recommendations</li>
                <li>Macronutrient breakdown</li>
                <li>Progress tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🥗 Personalized Diet Plans</h4>
            <ul>
                <li>Vegetarian, Non-veg & Vegan options</li>
                <li>Goal-specific food recommendations</li>
                <li>Nutritional information</li>
                <li>Calorie-conscious suggestions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🏃‍♂️ Exercise Recommendations</h4>
            <ul>
                <li>Goal-oriented workout plans</li>
                <li>Cardio & strength training</li>
                <li>Flexibility & core exercises</li>
                <li>Equipment-based filtering</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Goal Achievement</h4>
            <ul>
                <li>Weight loss & gain support</li>
                <li>Muscle building programs</li>
                <li>Maintenance plans</li>
                <li>Flexible lifestyle adaptation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works section
    st.markdown("---")
    st.markdown('<h2 style="text-align: center; color: #2E7D32; margin: 2rem 0;">🔄 How It Works</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="background: #4CAF50; color: white; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-size: 1.5rem; font-weight: bold;">1</div>
            <h4 style="color: #2E7D32;">Sign Up</h4>
            <p>Create your account with basic details</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="background: #4CAF50; color: white; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-size: 1.5rem; font-weight: bold;">2</div>
            <h4 style="color: #2E7D32;">Health Assessment</h4>
            <p>Enter your physical details and goals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="background: #4CAF50; color: white; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-size: 1.5rem; font-weight: bold;">3</div>
            <h4 style="color: #2E7D32;">Get Results</h4>
            <p>Receive personalized calculations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="background: #4CAF50; color: white; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-size: 1.5rem; font-weight: bold;">4</div>
            <h4 style="color: #2E7D32;">Follow Plan</h4>
            <p>Implement your custom recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h3 style="color: #2E7D32; margin-bottom: 1rem;">Ready to Start Your Health Journey?</h3>
            <p style="color: #666; margin-bottom: 2rem;">Join thousands of users who have transformed their lives with VitalPlan</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Get Started - Login/Sign Up", key="get_started", type="primary", use_container_width=True):
            st.session_state.page = 'auth'
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p><strong>VitalPlan</strong> - Your trusted partner in health and wellness</p>
        <p style="font-size: 0.9rem;">💡 Disclaimer: This tool provides general guidance. Consult healthcare professionals for medical advice.</p>
    </div>
    """, unsafe_allow_html=True)
