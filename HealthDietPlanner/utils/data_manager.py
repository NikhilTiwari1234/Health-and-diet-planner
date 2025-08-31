import pandas as pd
import hashlib
import os
from datetime import datetime

def initialize_data_files():
    """Initialize CSV files if they don't exist"""
    
    # Initialize users.csv
    if not os.path.exists('users.csv'):
        users_df = pd.DataFrame(columns=['username', 'password_hash', 'email', 'created_date'])
        users_df.to_csv('users.csv', index=False)
    
    # Initialize user_profiles.csv
    if not os.path.exists('user_profiles.csv'):
        profiles_df = pd.DataFrame(columns=[
            'username', 'age', 'gender', 'height_cm', 'weight_kg', 
            'activity_level', 'goal', 'diet_preference', 'bmi', 'bmr', 
            'target_calories', 'created_date'
        ])
        profiles_df.to_csv('user_profiles.csv', index=False)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def create_user(username, password, email):
    """Create a new user"""
    try:
        users_df = pd.read_csv('users.csv')
        
        # Check if username already exists
        if username in users_df['username'].values:
            return False, "Username already exists"
        
        # Check if email already exists
        if email in users_df['email'].values:
            return False, "Email already exists"
        
        # Create new user
        new_user = {
            'username': username,
            'password_hash': hash_password(password),
            'email': email,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)
        users_df.to_csv('users.csv', index=False)
        
        return True, "User created successfully"
    
    except Exception as e:
        return False, f"Error creating user: {str(e)}"

def authenticate_user(username, password):
    """Authenticate user login"""
    try:
        users_df = pd.read_csv('users.csv')
        
        if username not in users_df['username'].values:
            return False, "Username not found"
        
        user_row = users_df[users_df['username'] == username].iloc[0]
        
        if verify_password(password, user_row['password_hash']):
            return True, "Login successful"
        else:
            return False, "Incorrect password"
    
    except Exception as e:
        return False, f"Error during authentication: {str(e)}"

def save_user_profile(username, profile_data):
    """Save or update user profile"""
    try:
        profiles_df = pd.read_csv('user_profiles.csv')
        
        # Remove existing profile if it exists
        profiles_df = profiles_df[profiles_df['username'] != username]
        
        # Add new profile
        profile_data['username'] = username
        profile_data['created_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        profiles_df = pd.concat([profiles_df, pd.DataFrame([profile_data])], ignore_index=True)
        profiles_df.to_csv('user_profiles.csv', index=False)
        
        return True, "Profile saved successfully"
    
    except Exception as e:
        return False, f"Error saving profile: {str(e)}"

def get_user_profile(username):
    """Get user profile data"""
    try:
        profiles_df = pd.read_csv('user_profiles.csv')
        
        if username not in profiles_df['username'].values:
            return None, "Profile not found"
        
        profile = profiles_df[profiles_df['username'] == username].iloc[0]
        return profile.to_dict(), "Profile found"
    
    except Exception as e:
        return None, f"Error retrieving profile: {str(e)}"

def get_food_recommendations(diet_preference, goal, limit=10):
    """Get food recommendations based on diet preference and goal"""
    try:
        foods_df = pd.read_csv('foods.csv')
        
        # Filter by diet preference
        if diet_preference == 'vegan':
            filtered_foods = foods_df[foods_df['diet_type'] == 'vegan']
        elif diet_preference == 'vegetarian':
            filtered_foods = foods_df[foods_df['diet_type'].isin(['veg', 'vegan'])]
        else:  # non-vegetarian
            filtered_foods = foods_df  # All foods
        
        # Filter by goal suitability
        goal_foods = filtered_foods[
            (filtered_foods['goal_suitability'] == goal) | 
            (filtered_foods['goal_suitability'] == 'maintenance')
        ]
        
        # If not enough foods, add more from general foods
        if len(goal_foods) < limit:
            additional_foods = filtered_foods[
                ~filtered_foods.index.isin(goal_foods.index)
            ].head(limit - len(goal_foods))
            goal_foods = pd.concat([goal_foods, additional_foods])
        
        return goal_foods.head(limit)
    
    except Exception as e:
        return pd.DataFrame()

def get_exercise_recommendations(goal, limit=8):
    """Get exercise recommendations based on goal"""
    try:
        exercises_df = pd.read_csv('exercises.csv')
        
        # Filter by goal suitability
        goal_exercises = exercises_df[
            (exercises_df['goal_suitability'] == goal) | 
            (exercises_df['goal_suitability'] == 'maintenance')
        ]
        
        # If not enough exercises, add more from general exercises
        if len(goal_exercises) < limit:
            additional_exercises = exercises_df[
                ~exercises_df.index.isin(goal_exercises.index)
            ].head(limit - len(goal_exercises))
            goal_exercises = pd.concat([goal_exercises, additional_exercises])
        
        return goal_exercises.head(limit)
    
    except Exception as e:
        return pd.DataFrame()
