from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.course_list, name='home'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('dashboard/analysis/', core_views.career_analysis, name='career_analysis'),
    path('profile/update/', core_views.profile_update, name='profile_update'),
    path('course/<int:pk>/', core_views.course_detail, name='course_detail'),
    path('course/<int:pk>/enroll/', core_views.enroll_course, name='enroll_course'),
    
    # Auth
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/signup/', core_views.signup, name='signup'),
]
