from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __cl__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    skills_taught = models.ManyToManyField(Skill, related_name="courses")
    popularity_score = models.FloatField(default=0.0)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_skills = models.ManyToManyField(Skill, related_name="students", blank=True)
    interests = models.TextField(blank=True, help_text="Enter interests separated by commas")
    career_goal = models.CharField(max_length=200, blank=True, help_text="e.g. Data Scientist, Full Stack Dev")
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course')

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    sentiment = models.CharField(max_length=20, default='Neutral') # AI will populate this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"
