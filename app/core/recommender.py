import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.models import Course, StudentProfile
import numpy as np

class Recommender:
    def __init__(self):
        self.courses = list(Course.objects.all())
        if not self.courses:
            self.df = pd.DataFrame()
            return

        data = []
        for c in self.courses:
            skills = " ".join([s.name for s in c.skills_taught.all()])
            combined_features = f"{c.title} {c.description} {c.category} {skills}"
            data.append({
                'id': c.id,
                'combined_features': combined_features
            })
        
        self.df = pd.DataFrame(data)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])

    def get_recommendations(self, student_profile, num_recommendations=5):
        if self.df.empty:
            return []

        # Create a user profile vector based on interests and career goal
        user_skills = " ".join([s.name for s in student_profile.current_skills.all()])
        user_input = f"{student_profile.interests} {student_profile.career_goal} {user_skills}"
        
        user_vector = self.vectorizer.transform([user_input])
        
        # Calculate cosine similarity between user vector and all course vectors
        similarity_scores = cosine_similarity(user_vector, self.tfidf_matrix)
        
        # Get indices of top courses
        course_indices = similarity_scores.flatten().argsort()[::-1]
        
        recommended_courses = []
        for i in course_indices:
            course_id = self.df.iloc[i]['id']
            # Filter out already enrolled courses if any (optional)
            recommended_courses.append(Course.objects.get(id=course_id))
            if len(recommended_courses) >= num_recommendations:
                break
                
        return recommended_courses

    def get_skill_gap(self, student_profile, target_career_goal):
        # Identify skills needed for the career goal vs current student skills
        career_vector = self.vectorizer.transform([target_career_goal])
        similarity_scores = cosine_similarity(career_vector, self.tfidf_matrix)
        top_indices = similarity_scores.flatten().argsort()[::-1][:3]
        
        required_skills = set()
        for i in top_indices:
            course_id = self.df.iloc[i]['id']
            c = Course.objects.get(id=course_id)
            for s in c.skills_taught.all():
                required_skills.add(s.name)
        
        current_skills = set([s.name for s in student_profile.current_skills.all()])
        gap_skills = required_skills - current_skills
        
        return list(gap_skills)

    def analyze_sentiment(self, text):
        """Simple AI Sentiment analysis based on word impact"""
        positive_words = ['great', 'excellent', 'amazing', 'good', 'helpful', 'useful', 'easy', 'learned', 'perfect']
        negative_words = ['bad', 'poor', 'difficult', 'hard', 'useless', 'confusing', 'boring', 'slow', 'waste']
        
        text = text.lower()
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count > neg_count:
            return 'Positive'
        elif neg_count > pos_count:
            return 'Negative'
        else:
            return 'Neutral'

    def predict_career_path(self, student_profile):
        """Predicts a suggested career title and returns matching scores"""
        personas = {
            'Data Scientist': 'Python Pandas NumPy Statistics Machine Learning SQL',
            'Full Stack Developer': 'Django React JavaScript Node.js SQL HTML CSS',
            'Cloud Architect': 'AWS Azure Cloud Docker Kubernetes Terraform',
            'Cybersecurity Analyst': 'Network Security Linux Ethical Hacking Cryptography',
            'AI Engineer': 'Python PyTorch TensorFlow Deep Learning NLP Computer Vision'
        }
        
        user_skills = " ".join([s.name for s in student_profile.current_skills.all()])
        if not user_skills:
            return "General Learner", {}
            
        persona_titles = list(personas.keys())
        persona_descriptions = list(personas.values())
        
        temp_vectorizer = TfidfVectorizer().fit(persona_descriptions + [user_skills])
        persona_matrices = temp_vectorizer.transform(persona_descriptions)
        user_matrix = temp_vectorizer.transform([user_skills])
        
        similarities = cosine_similarity(user_matrix, persona_matrices).flatten()
        
        results = {}
        for i, title in enumerate(persona_titles):
            results[title] = round(float(similarities[i]) * 100, 1)
            
        best_match_idx = np.argmax(similarities)
        return persona_titles[best_match_idx], results
