# AI-Based Learning Recommendation Platform

A premium, full-stack AI-driven educational platform built with Django and Scikit-Learn. The system provides personalized course recommendations, skill-gap analysis, and career persona predictions based on student profiles and skill sets.

## 🌟 Key Features

- **Personalized Course Recommendations**: Uses TF-IDF and Cosine Similarity to match student interests with course content.
- **AI Career Persona Prediction**: Predicts your professional identity (e.g., Data Scientist, AI Engineer) based on current skills.
- **Skill-Gap Analysis**: Automatically identifies missing skills required to reach your target career goal.
- **AI Sentiment Analysis**: Analyzes student feedback on courses to categorize sentiment (Positive/Negative/Neutral).
- **Premium Dashboard**: Glassmorphic dark-mode interface with progress tracking and interactive visualizations.

## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Machine Learning**: Scikit-Learn, Pandas, NumPy
- **Frontend**: Vanilla CSS (Modern Glassmorphism), HTML5
- **Database**: SQLite (Default)

## 🚀 Getting Started

### 1. Installation
Clone the project and install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Database Setup
Run migrations and seed the initial course data:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

### 3. Start the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## 🔑 Admin Credentials
Manage courses and student profiles at `/admin/`:
- **Username**: `admin`
- **Password**: `admin123`

---
*Developed for AI-Based Learning Optimization*
