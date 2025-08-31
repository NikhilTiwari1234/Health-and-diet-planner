import streamlit as st
from utils.health_calculator import calculate_bmi, calculate_bmr, calculate_target_calories, get_bmi_category
from utils.data_manager import save_user_profile

def show():
    st.markdown('<h1 class="main-header">📋 Health Assessment</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tell us about yourself to get personalized recommendations</p>', unsafe_allow_html=True)
    
    # Check if user is logged in
    if not st.session_state.user_logged_in:
        st.error("Please log in to access this page")
        return
    
    st.markdown(f"<p style='text-align: center; color: #666;'>Welcome, <strong>{st.session_state.username}</strong>! Let's create your health profile.</p>", unsafe_allow_html=True)
    
    with st.form("health_assessment"):
        # Personal Information
        st.markdown("### 👤 Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=13, max_value=120, value=25, help="Your current age in years")
            height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, help="Your height in centimeters")
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female"], help="Biological gender for BMR calculation")
            weight_kg = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1, help="Your current weight in kilograms")
        
        # Lifestyle Information
        st.markdown("### 🏃‍♂️ Lifestyle Information")
        
        activity_level = st.selectbox(
            "Activity Level",
            [
                "sedentary",
                "light", 
                "moderate",
                "active",
                "very_active"
            ],
            format_func=lambda x: {
                "sedentary": "Sedentary (Desk job, no exercise)",
                "light": "Light Activity (Light exercise 1-3 days/week)",
                "moderate": "Moderate Activity (Moderate exercise 3-5 days/week)",
                "active": "Active (Hard exercise 6-7 days/week)",
                "very_active": "Very Active (Physical job + exercise)"
            }[x],
            help="Choose the option that best describes your daily activity level"
        )
        
        # Goals and Preferences
        st.markdown("### 🎯 Goals & Preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            goal = st.selectbox(
                "Primary Goal",
                ["weight_loss", "weight_gain", "muscle_building", "maintenance"],
                format_func=lambda x: {
                    "weight_loss": "🔥 Weight Loss",
                    "weight_gain": "📈 Weight Gain", 
                    "muscle_building": "💪 Muscle Building",
                    "maintenance": "⚖️ Maintenance"
                }[x],
                help="What's your primary health and fitness goal?"
            )
        
        with col2:
            diet_preference = st.selectbox(
                "Diet Preference",
                ["vegetarian", "non_vegetarian", "vegan"],
                format_func=lambda x: {
                    "vegetarian": "🥬 Vegetarian",
                    "non_vegetarian": "🍖 Non-Vegetarian",
                    "vegan": "🌱 Vegan"
                }[x],
                help="Your dietary preferences"
            )
        
        # Submit button
        submitted = st.form_submit_button("📊 Calculate My Health Profile", type="primary", use_container_width=True)
        
        if submitted:
            # Validate inputs
            if age < 13 or age > 120:
                st.error("Please enter a valid age between 13 and 120")
                return
            
            if height_cm < 100 or height_cm > 250:
                st.error("Please enter a valid height between 100 and 250 cm")
                return
            
            if weight_kg < 30 or weight_kg > 300:
                st.error("Please enter a valid weight between 30 and 300 kg")
                return
            
            # Calculate health metrics
            bmi = calculate_bmi(weight_kg, height_cm)
            bmr = calculate_bmr(weight_kg, height_cm, age, gender.lower())
            target_calories = calculate_target_calories(bmr, activity_level, goal)
            
            # Prepare profile data
            profile_data = {
                'age': age,
                'gender': gender.lower(),
                'height_cm': height_cm,
                'weight_kg': weight_kg,
                'activity_level': activity_level,
                'goal': goal,
                'diet_preference': diet_preference,
                'bmi': bmi,
                'bmr': bmr,
                'target_calories': target_calories
            }
            
            # Save profile
            success, message = save_user_profile(st.session_state.username, profile_data)
            
            if success:
                st.success("✅ Health profile created successfully!")
                st.session_state.assessment_completed = True
                
                # Show preview of results
                st.markdown("---")
                st.markdown("### 📊 Your Health Metrics Preview")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    bmi_category, bmi_color = get_bmi_category(bmi)
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>BMI</h4>
                        <h2 style="color: {bmi_color};">{bmi}</h2>
                        <p style="color: {bmi_color};">{bmi_category}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>BMR</h4>
                        <h2 style="color: #2E7D32;">{int(bmr)}</h2>
                        <p>calories/day</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>Target Calories</h4>
                        <h2 style="color: #2E7D32;">{int(target_calories)}</h2>
                        <p>calories/day</p>
                    </div>
                    """, unsafe_allow_html=True)
                
            else:
                st.error(f"Error saving profile: {message}")
    
    # Continue to dashboard button (outside the form)
    if 'assessment_completed' in st.session_state and st.session_state.assessment_completed:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🎯 View Full Dashboard", type="primary", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔙 Back to Login"):
            st.session_state.page = 'auth'
            st.rerun()
    
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()
