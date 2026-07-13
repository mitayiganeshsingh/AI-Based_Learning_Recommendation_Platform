from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Course, StudentProfile, Enrollment, Skill, Review
from .recommender import Recommender
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    profile = request.user.studentprofile
    recommender = Recommender()
    
    # Get recommendations
    recommendations = recommender.get_recommendations(profile)
    
    # Get skill gap for their current goal
    skill_gap = []
    if profile.career_goal:
        skill_gap = recommender.get_skill_gap(profile, profile.career_goal)
        
    # AI Career Prediction
    predicted_career, career_scores = recommender.predict_career_path(profile)
    
    enrolled_courses = Enrollment.objects.filter(student=profile)
    
    context = {
        'profile': profile,
        'recommendations': recommendations,
        'skill_gap': skill_gap,
        'predicted_career': predicted_career,
        'career_scores': career_scores,
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def career_analysis(request):
    profile = request.user.studentprofile
    recommender = Recommender()
    predicted_career, career_scores = recommender.predict_career_path(profile)
    
    # Format scores for display
    sorted_scores = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    
    return render(request, 'core/career_analysis.html', {
        'profile': profile,
        'predicted_career': predicted_career,
        'scores': sorted_scores
    })

@login_required
def profile_update(request):
    profile = request.user.studentprofile
    if request.method == 'POST':
        profile.interests = request.POST.get('interests')
        profile.career_goal = request.POST.get('career_goal')
        
        # Simple skill parsing from comma separated string
        skill_str = request.POST.get('skills', '')
        if skill_str:
            skill_list = [s.strip() for s in skill_str.split(',') if s.strip()]
            profile.current_skills.clear()
            for s_name in skill_list:
                skill, _ = Skill.objects.get_or_create(name=s_name)
                profile.current_skills.add(skill)
        
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('dashboard')
    
    current_skills_str = ", ".join([s.name for s in profile.current_skills.all()])
    return render(request, 'core/profile_update.html', {'profile': profile, 'current_skills_str': current_skills_str})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user.studentprofile, course=course).exists()
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        recommender = Recommender()
        sentiment = recommender.analyze_sentiment(comment)
        
        Review.objects.create(
            course=course,
            student=request.user.studentprofile,
            rating=rating,
            comment=comment,
            sentiment=sentiment
        )
        messages.success(request, "Review submitted and analyzed by AI!")
        return redirect('course_detail', pk=pk)

    reviews = course.reviews.all().order_by('-created_at')
    return render(request, 'core/course_detail.html', {'course': course, 'is_enrolled': is_enrolled, 'reviews': reviews})

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    Enrollment.objects.get_or_create(student=request.user.studentprofile, course=course)
    messages.success(request, f"Successfully enrolled in {course.title}")
    return redirect('course_detail', pk=pk)
