# AI-Based Learning Recommendation Platform - Project Walkthrough

The **AI-Based Learning Recommendation Platform** is a full-stack Django application designed to solve the problem of generic course recommendations. It uses machine learning to provide personalized learning paths and skill-gap analysis.

## 🚀 Getting Started

### 1. Prerequisite Checklist
Ensure you have the following installed:
- Python 3.10+
- Django
- Scikit-learn
- Pandas
- Numpy

### 2. Run the Application
The project is already set up and the database is seeded. Simply run:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to explore the platform.

---

## 🧠 AI & Machine Learning Architecture

### Recommendation System (Content-Based Filtering)
The platform uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to vectorize course descriptions, titles, and required skills. 
- **Matching Mechanism**: When a student sets their interests and career goals, the system calculates the **Cosine Similarity** between the student's "preference vector" and every course in the database.
- **Result**: The courses with the highest similarity scores are recommended first.

### Skill-Gap Analysis
This feature performs a "career-path simulator":
1. It looks at your **Target Career Goal** (e.g., "Full Stack Developer").
2. It finds the top 3 courses most relevant to that goal.
3. It identifies the union of all skills taught in those courses.
4. It compares those "needed skills" with your **Current Skills**.
5. The difference is displayed as your **Skill Gap**, giving you a clear roadmap of what to learn next.

---

## 🎨 Design Aesthetics
- **Premium Glassmorphism**: Use of `backdrop-filter` and semi-transparent layers for a modern, high-end feel.
- **Vibrant Gradients**: Indigo to Pink color scheme inspired by modern SaaS platforms.
- **Dynamic Feedback**: Micro-animations on cards and hover states.

## 📂 Project Structure
- `core/recommender.py`: The ML heart of the system.
- `core/models.py`: Database schema for Courses, Students, and Skills.
- `static/css/style.css`: The entire custom design system.
- `templates/`: Modern HTML5 layouts.

---

## 🔑 Default Admin Account
You can log in to the admin panel at `/admin/` using:
- **Username**: `admin`
- **Password**: `admin123`
