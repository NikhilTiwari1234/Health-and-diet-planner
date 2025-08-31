import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_manager import get_user_profile, get_food_recommendations, get_exercise_recommendations
from utils.health_calculator import get_bmi_category, get_macronutrient_split, get_health_recommendations

def show():
    # Check if user is logged in
    if not st.session_state.user_logged_in:
        st.error("Please log in to access this page")
        return
    
    # Get user profile
    profile, message = get_user_profile(st.session_state.username)
    
    if not profile:
        st.error("Profile not found. Please complete your health assessment first.")
        if st.button("📋 Go to Assessment"):
            st.session_state.page = 'assessment'
            st.rerun()
        return
    
    # Header
    st.markdown(f'<h1 class="main-header">🎯 Welcome, {st.session_state.username}!</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your Personalized Health Dashboard</p>', unsafe_allow_html=True)
    
    # Navigation menu
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 Overview", use_container_width=True):
            st.session_state.dashboard_tab = 'overview'
    with col2:
        if st.button("🥗 Diet Plan", use_container_width=True):
            st.session_state.dashboard_tab = 'diet'
    with col3:
        if st.button("💪 Exercise Plan", use_container_width=True):
            st.session_state.dashboard_tab = 'exercise'
    with col4:
        if st.button("📈 Progress", use_container_width=True):
            st.session_state.dashboard_tab = 'progress'
    
    # Initialize tab if not exists
    if 'dashboard_tab' not in st.session_state:
        st.session_state.dashboard_tab = 'overview'
    
    st.markdown("---")
    
    # Show content based on selected tab
    if st.session_state.dashboard_tab == 'overview':
        show_overview(profile)
    elif st.session_state.dashboard_tab == 'diet':
        show_diet_plan(profile)
    elif st.session_state.dashboard_tab == 'exercise':
        show_exercise_plan(profile)
    elif st.session_state.dashboard_tab == 'progress':
        show_progress(profile)
    
    # Footer navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Update Assessment"):
            st.session_state.page = 'assessment'
            st.rerun()
    
    with col2:
        if st.button("🔓 Logout"):
            st.session_state.user_logged_in = False
            st.session_state.username = None
            st.session_state.page = 'landing'
            st.rerun()
    
    with col3:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()

def show_overview(profile):
    st.markdown("### 📊 Health Overview")
    
    # Health metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    bmi_category, bmi_color = get_bmi_category(profile['bmi'])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>BMI</h4>
            <h2 style="color: {bmi_color};">{profile['bmi']}</h2>
            <p style="color: {bmi_color};">{bmi_category}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>BMR</h4>
            <h2 style="color: #2E7D32;">{int(profile['bmr'])}</h2>
            <p>cal/day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Target Calories</h4>
            <h2 style="color: #2E7D32;">{int(profile['target_calories'])}</h2>
            <p>cal/day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        goal_emoji = {
            'weight_loss': '🔥',
            'weight_gain': '📈',
            'muscle_building': '💪',
            'maintenance': '⚖️'
        }
        st.markdown(f"""
        <div class="metric-card">
            <h4>Goal</h4>
            <h2>{goal_emoji.get(profile['goal'], '🎯')}</h2>
            <p>{profile['goal'].replace('_', ' ').title()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # BMI Chart
        fig_bmi = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = profile['bmi'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "BMI Status"},
            gauge = {
                'axis': {'range': [None, 40]},
                'bar': {'color': bmi_color},
                'steps': [
                    {'range': [0, 18.5], 'color': "#FFF3E0"},
                    {'range': [18.5, 25], 'color': "#E8F5E8"},
                    {'range': [25, 30], 'color': "#FFF3E0"},
                    {'range': [30, 40], 'color': "#FFEBEE"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30
                }
            }
        ))
        fig_bmi.update_layout(height=300)
        st.plotly_chart(fig_bmi, use_container_width=True)
    
    with col2:
        # Macronutrient breakdown
        macros = get_macronutrient_split(profile['goal'], profile['target_calories'])
        
        fig_macro = px.pie(
            values=[macros['protein'], macros['carbs'], macros['fat']],
            names=['Protein', 'Carbohydrates', 'Fat'],
            title="Daily Macronutrient Breakdown (grams)",
            color_discrete_sequence=['#4CAF50', '#81C784', '#A5D6A7']
        )
        fig_macro.update_layout(height=300)
        st.plotly_chart(fig_macro, use_container_width=True)
    
    # Health recommendations
    st.markdown("### 💡 Personalized Health Recommendations")
    recommendations = get_health_recommendations(profile['bmi'], profile['goal'])
    
    for i, rec in enumerate(recommendations[:5], 1):
        st.markdown(f"""
        <div style="background: #F1F8E9; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #4CAF50;">
            <strong>{i}.</strong> {rec}
        </div>
        """, unsafe_allow_html=True)

def show_diet_plan(profile):
    st.markdown("### 🥗 Personalized Diet Plan")
    
    # Diet summary
    col1, col2, col3 = st.columns(3)
    macros = get_macronutrient_split(profile['goal'], profile['target_calories'])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Daily Protein</h4>
            <h2 style="color: #2E7D32;">{int(macros['protein'])}g</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Daily Carbs</h4>
            <h2 style="color: #2E7D32;">{int(macros['carbs'])}g</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Daily Fat</h4>
            <h2 style="color: #2E7D32;">{int(macros['fat'])}g</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Food recommendations
    st.markdown("#### 🍽️ Recommended Foods")
    foods = get_food_recommendations(profile['diet_preference'], profile['goal'], 12)
    
    if not foods.empty:
        # Create food cards
        for i in range(0, len(foods), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(foods):
                    food = foods.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="feature-card">
                            <h5>{food['food_name']}</h5>
                            <p><strong>Category:</strong> {food['category']}</p>
                            <p><strong>Calories:</strong> {food['calories_per_100g']}/100g</p>
                            <p><strong>Protein:</strong> {food['protein']}g</p>
                            <p><strong>Carbs:</strong> {food['carbs']}g</p>
                            <p><strong>Fat:</strong> {food['fat']}g</p>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.warning("No food recommendations available. Please check your diet preferences.")
    
    # Meal planning tips
    st.markdown("#### 📋 Meal Planning Tips")
    meal_tips = {
        'weight_loss': [
            "Focus on high-protein, low-calorie foods",
            "Include plenty of vegetables and fiber",
            "Control portion sizes",
            "Eat 4-5 smaller meals throughout the day"
        ],
        'weight_gain': [
            "Add healthy fats like nuts and avocados",
            "Include calorie-dense foods",
            "Eat more frequent meals",
            "Add protein shakes between meals"
        ],
        'muscle_building': [
            "Consume 1.6-2.2g protein per kg body weight",
            "Time protein intake around workouts",
            "Include complex carbohydrates",
            "Stay hydrated during training"
        ],
        'maintenance': [
            "Maintain balanced macronutrient ratios",
            "Focus on whole, unprocessed foods",
            "Listen to hunger cues",
            "Practice portion control"
        ]
    }
    
    tips = meal_tips.get(profile['goal'], meal_tips['maintenance'])
    for tip in tips:
        st.markdown(f"• {tip}")

def show_exercise_plan(profile):
    st.markdown("### 💪 Personalized Exercise Plan")
    
    # Exercise summary
    goal_descriptions = {
        'weight_loss': "Focus on cardio and high-intensity exercises to burn calories",
        'weight_gain': "Combine strength training with moderate cardio",
        'muscle_building': "Emphasize strength training and progressive overload",
        'maintenance': "Balance cardio and strength training for overall fitness"
    }
    
    st.markdown(f"""
    <div class="feature-card">
        <h4>Your Goal: {profile['goal'].replace('_', ' ').title()}</h4>
        <p>{goal_descriptions.get(profile['goal'], 'Balanced approach to fitness')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Exercise recommendations
    exercises = get_exercise_recommendations(profile['goal'], 12)
    
    if not exercises.empty:
        st.markdown("#### 🏃‍♂️ Recommended Exercises")
        
        # Group exercises by category
        categories = exercises['category'].unique()
        
        for category in categories:
            category_exercises = exercises[exercises['category'] == category]
            
            st.markdown(f"##### {category.title()} Exercises")
            
            for _, exercise in category_exercises.iterrows():
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    intensity_color = {
                        'Low': '#4CAF50',
                        'Medium': '#FF9800', 
                        'High': '#F44336'
                    }
                    
                    st.markdown(f"""
                    <div style="background: #F9F9F9; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                        <h6>{exercise['exercise_name']}</h6>
                        <p><strong>Target:</strong> {exercise['target_muscle']}</p>
                        <p><strong>Intensity:</strong> <span style="color: {intensity_color.get(exercise['intensity'], '#666')};">{exercise['intensity']}</span></p>
                        <p><strong>Equipment:</strong> {exercise['equipment_needed']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h6>Duration</h6>
                        <h4>{exercise['duration_minutes']} min</h4>
                        <p>{exercise['calories_per_hour']} cal/hr</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("No exercise recommendations available.")
    
    # Weekly plan suggestion
    st.markdown("#### 📅 Weekly Exercise Schedule")
    
    weekly_plans = {
        'weight_loss': {
            'Cardio': '4-5 times per week',
            'Strength Training': '2-3 times per week',
            'Rest Days': '1-2 days'
        },
        'muscle_building': {
            'Strength Training': '4-5 times per week',
            'Cardio': '2-3 times per week (light)',
            'Rest Days': '1-2 days'
        },
        'weight_gain': {
            'Strength Training': '3-4 times per week',
            'Cardio': '2 times per week (moderate)',
            'Rest Days': '2-3 days'
        },
        'maintenance': {
            'Cardio': '3-4 times per week',
            'Strength Training': '2-3 times per week',
            'Rest Days': '1-2 days'
        }
    }
    
    plan = weekly_plans.get(profile['goal'], weekly_plans['maintenance'])
    
    col1, col2, col3 = st.columns(3)
    for i, (activity, frequency) in enumerate(plan.items()):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
            <div class="metric-card">
                <h6>{activity}</h6>
                <p>{frequency}</p>
            </div>
            """, unsafe_allow_html=True)

def show_progress(profile):
    st.markdown("### 📈 Progress Tracking")
    
    # Current stats
    st.markdown("#### 📊 Current Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Weight", f"{profile['weight_kg']} kg")
    
    with col2:
        st.metric("BMI", f"{profile['bmi']}")
    
    with col3:
        st.metric("Target Calories", f"{int(profile['target_calories'])}")
    
    with col4:
        days_since = (pd.Timestamp.now() - pd.to_datetime(profile['created_date'])).days
        st.metric("Days Active", f"{days_since}")
    
    # Progress chart placeholder
    st.markdown("#### 📉 Weight Progress Chart")
    
    # Sample progress data for visualization
    import numpy as np
    dates = pd.date_range(start=profile['created_date'], periods=30, freq='D')
    
    # Simulate weight progress based on goal
    if profile['goal'] == 'weight_loss':
        weights = np.linspace(profile['weight_kg'], profile['weight_kg'] - 2, 30) + np.random.normal(0, 0.2, 30)
    elif profile['goal'] == 'weight_gain':
        weights = np.linspace(profile['weight_kg'], profile['weight_kg'] + 2, 30) + np.random.normal(0, 0.2, 30)
    else:
        weights = np.full(30, profile['weight_kg']) + np.random.normal(0, 0.3, 30)
    
    progress_df = pd.DataFrame({
        'Date': dates,
        'Weight': weights
    })
    
    fig = px.line(progress_df, x='Date', y='Weight', title='Weight Progress Over Time')
    fig.update_traces(line_color='#2E7D32', line_width=3)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Weight (kg)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Goals and achievements
    st.markdown("#### 🎯 Goals & Achievements")
    
    achievements = [
        "✅ Completed health assessment",
        "✅ Set personalized goals",
        "✅ Received custom diet plan",
        "✅ Got exercise recommendations"
    ]
    
    for achievement in achievements:
        st.markdown(f"""
        <div style="background: #E8F5E8; padding: 0.5rem 1rem; border-radius: 5px; margin: 0.5rem 0; border-left: 4px solid #4CAF50;">
            {achievement}
        </div>
        """, unsafe_allow_html=True)
    
    # Next milestones
    st.markdown("#### 🎯 Next Milestones")
    
    milestones = {
        'weight_loss': [
            "🎯 Lose 1 kg in 2 weeks",
            "💪 Complete 10 workouts",
            "🥗 Follow diet plan for 7 days",
            "📉 Reduce BMI by 0.5 points"
        ],
        'weight_gain': [
            "📈 Gain 0.5 kg in 2 weeks", 
            "💪 Increase strength training frequency",
            "🥗 Meet daily calorie targets",
            "📊 Track weight consistently"
        ],
        'muscle_building': [
            "💪 Increase workout intensity",
            "🥩 Meet daily protein targets",
            "📈 Gain lean muscle mass",
            "⚡ Improve strength metrics"
        ],
        'maintenance': [
            "⚖️ Maintain current weight",
            "🏃‍♂️ Stay consistent with exercise",
            "🥗 Continue balanced nutrition",
            "📊 Monitor health metrics"
        ]
    }
    
    user_milestones = milestones.get(profile['goal'], milestones['maintenance'])
    
    for milestone in user_milestones:
        st.markdown(f"• {milestone}")
