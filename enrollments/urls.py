from django.urls import path
from . import views

urlpatterns = [
    path('enrollment/<int:enrollment_id>/', views.enrollment_detail, name='enrollment_detail'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
]
