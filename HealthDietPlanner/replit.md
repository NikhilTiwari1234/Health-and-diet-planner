# VitalPlan - Virtual Health & Diet Planner

## Overview

VitalPlan is a comprehensive virtual health and diet planning web application built with Streamlit. The application provides personalized health recommendations including BMI calculations, calorie needs assessment, diet suggestions, and exercise plans based on user profiles and goals. Users can register, complete health assessments, and receive tailored recommendations for weight loss, muscle building, or maintenance goals with support for various dietary preferences (vegetarian, non-vegetarian, vegan).

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based single-page application with multi-page navigation
- **Page Structure**: Modular page system with separate components for landing, authentication, assessment, and dashboard
- **State Management**: Session-based state management for user authentication and page navigation
- **Styling**: Custom CSS for enhanced UI/UX with gradient backgrounds, feature cards, and responsive design

### Backend Architecture
- **Data Storage**: CSV-based file system for user data, profiles, and recommendations
- **Authentication**: Username/password authentication with SHA-256 password hashing
- **Health Calculations**: Dedicated utility modules for BMI, BMR, and calorie calculations using Mifflin-St Jeor equation
- **Recommendation Engine**: Algorithm-based food and exercise recommendations based on user goals and preferences

### Data Management
- **User Data**: CSV files for user accounts (`users.csv`) and health profiles (`user_profiles.csv`)
- **Content Data**: Pre-populated CSV files for food recommendations (`foods.csv`) and exercise plans (`exercises.csv`)
- **Profile Persistence**: User health assessments stored and retrieved for dashboard personalization

### Core Features
- **Health Assessment**: Comprehensive form collecting age, gender, height, weight, activity level, goals, and dietary preferences
- **Personalized Dashboard**: Multi-tab interface showing health overview, diet plans, exercise recommendations, and progress tracking
- **Calculation Engine**: BMI categorization, BMR calculation, target calorie computation with activity level adjustments
- **Goal-Based Recommendations**: Tailored suggestions for weight loss, weight gain, muscle building, and maintenance

## External Dependencies

### Python Libraries
- **streamlit**: Core web application framework
- **pandas**: Data manipulation and CSV file handling
- **plotly**: Interactive charts and visualizations for dashboard metrics
- **hashlib**: Password encryption and security
- **datetime**: Timestamp management for user registration and profile creation

### Data Sources
- **Static CSV Files**: Local food database and exercise recommendations
- **User-Generated Data**: Health profiles and assessment results stored locally

### Potential Integrations
- **Database Migration**: Architecture supports future migration from CSV to SQL databases
- **API Integrations**: Extensible design for nutrition APIs or fitness tracking services
- **Cloud Storage**: File-based system can be adapted for cloud storage solutions