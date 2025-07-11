from django.shortcuts import render

# Create your views here.
# -------------------------
# enrollments/views.py
# -------------------------
from django.shortcuts import render, redirect
from .models import Enrollment
from courses.models import Course
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404





@login_required
def enroll(request, course_id):
    course = Course.objects.get(id=course_id)
    profile = request.user.profile
    if profile.role == 'student':
        Enrollment.objects.get_or_create(student=profile, course=course)
    return redirect('my_courses')

@login_required
def my_courses(request):
    profile = request.user.profile
    enrollments = Enrollment.objects.filter(student=profile)
    return render(request, 'enrollments/my_courses.html', {'enrollments': enrollments})

@login_required
def teacher_enrollments(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role == 'teacher':
        enrollments = Enrollment.objects.filter(course__teacher=profile)
        return render(request, 'enrollments/teacher_enrollments.html', {'enrollments': enrollments})
    return render(request, 'unauthorized.html')

def enrollment_detail(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    return render(request, 'enrollments/enrollment_detail.html', {'enrollment': enrollment})

@login_required
def enroll_course(request, course_id):
    profile = request.user.profile
    if profile.role != 'student':
        return redirect('course_list')

    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=profile, course=course)
    return redirect('course_list')


