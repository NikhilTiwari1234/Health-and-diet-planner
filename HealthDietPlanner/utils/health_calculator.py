import math

def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI (Body Mass Index)"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return "Underweight", "#FF9800"
    elif 18.5 <= bmi < 25:
        return "Normal weight", "#4CAF50"
    elif 25 <= bmi < 30:
        return "Overweight", "#FF9800"
    else:
        return "Obese", "#F44336"

def calculate_bmr(weight_kg, height_cm, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:  # female
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return round(bmr, 0)

def calculate_target_calories(bmr, activity_level, goal):
    """Calculate target calories based on BMR, activity level, and goal"""
    
    # Activity multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    # Calculate maintenance calories
    maintenance_calories = bmr * activity_multipliers.get(activity_level, 1.2)
    
    # Adjust based on goal
    if goal == 'weight_loss':
        target_calories = maintenance_calories - 500  # 500 calorie deficit
    elif goal == 'weight_gain':
        target_calories = maintenance_calories + 500  # 500 calorie surplus
    elif goal == 'muscle_building':
        target_calories = maintenance_calories + 300  # 300 calorie surplus
    else:  # maintenance
        target_calories = maintenance_calories
    
    return round(target_calories, 0)

def get_macronutrient_split(goal, calories):
    """Calculate macronutrient split based on goal"""
    if goal == 'weight_loss':
        # Higher protein, moderate carbs, lower fat
        protein_ratio = 0.30
        carbs_ratio = 0.40
        fat_ratio = 0.30
    elif goal == 'muscle_building':
        # High protein, moderate carbs, moderate fat
        protein_ratio = 0.35
        carbs_ratio = 0.40
        fat_ratio = 0.25
    elif goal == 'weight_gain':
        # Moderate protein, higher carbs, higher fat
        protein_ratio = 0.25
        carbs_ratio = 0.45
        fat_ratio = 0.30
    else:  # maintenance
        # Balanced macros
        protein_ratio = 0.25
        carbs_ratio = 0.45
        fat_ratio = 0.30
    
    protein_calories = calories * protein_ratio
    carbs_calories = calories * carbs_ratio
    fat_calories = calories * fat_ratio
    
    # Convert to grams (protein: 4 cal/g, carbs: 4 cal/g, fat: 9 cal/g)
    protein_grams = round(protein_calories / 4, 0)
    carbs_grams = round(carbs_calories / 4, 0)
    fat_grams = round(fat_calories / 9, 0)
    
    return {
        'protein': protein_grams,
        'carbs': carbs_grams,
        'fat': fat_grams
    }

def get_health_recommendations(bmi, goal):
    """Get health recommendations based on BMI and goal"""
    recommendations = []
    
    if bmi < 18.5:
        recommendations.extend([
            "Focus on gaining healthy weight through nutrient-dense foods",
            "Include calorie-dense foods like nuts, avocados, and healthy oils",
            "Consider strength training to build muscle mass"
        ])
    elif bmi >= 30:
        recommendations.extend([
            "Focus on gradual, sustainable weight loss",
            "Prioritize whole foods and limit processed foods",
            "Increase physical activity gradually"
        ])
    
    if goal == 'weight_loss':
        recommendations.extend([
            "Create a moderate calorie deficit of 300-500 calories per day",
            "Focus on high-protein, high-fiber foods for satiety",
            "Include both cardio and strength training exercises"
        ])
    elif goal == 'muscle_building':
        recommendations.extend([
            "Eat adequate protein (1.6-2.2g per kg body weight)",
            "Focus on progressive resistance training",
            "Ensure adequate rest and recovery"
        ])
    elif goal == 'weight_gain':
        recommendations.extend([
            "Eat in a moderate calorie surplus",
            "Focus on nutrient-dense, calorie-rich foods",
            "Include strength training to gain lean muscle"
        ])
    
    return recommendations
