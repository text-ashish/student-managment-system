from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm
from accounts.models import Profile
from enrollments.models import Enrollment
from django.contrib.auth.decorators import login_required

@login_required
def course_list(request):
    courses = Course.objects.all()
    enrolled_ids = []

    # If student, fetch courses they're already enrolled in
    if request.user.is_authenticated:
        profile = request.user.profile
        if profile.role == 'student':
            enrolled_ids = Enrollment.objects.filter(
                student=profile
            ).values_list('course_id', flat=True)

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrolled_ids': enrolled_ids
    })

@login_required
def create_course(request):
    profile = request.user.profile
    if profile.role != 'teacher':
        return redirect('course_list')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = profile
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    
    return render(request, 'courses/create_course_form.html', {'form': form})
