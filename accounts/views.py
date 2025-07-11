from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from .models import Profile
from enrollments.models import Enrollment
from courses.models import Course
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Create the Profile object
            role = form.cleaned_data['role']
            Profile.objects.create(user=user, role=role)

            # Automatically log the user in
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    # Ensure the user has a profile
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Create profile automatically with default role if not exists
        with transaction.atomic():
            profile = Profile.objects.create(user=request.user, role='student')
    return render(request, 'accounts/dashboard.html', {'profile': profile})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # Ensure profile exists
            try:
                _ = user.profile
            except Profile.DoesNotExist:
                with transaction.atomic():
                    Profile.objects.create(user=user, role='student')  # default role
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'admin'


@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().select_related('profile')
    return render(request, 'accounts/user_list.html', {'users': users})


@user_passes_test(is_admin)
def edit_user_role(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        role = request.POST.get('role')
        if role in dict(Profile.USER_ROLES):
            user.profile.role = role
            user.profile.save()
            return redirect('user_list')
    return render(request, 'accounts/edit_user.html', {'user_obj': user})


@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'accounts/confirm_delete.html', {'user_obj': user})

from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
@login_required
def teacher_enrollments(request):
    profile = request.user.profile
    if profile.role != 'teacher':
        return redirect('dashboard')  # or return 403 if you prefer

    courses = Course.objects.filter(teacher=profile)
    enrollments = Enrollment.objects.filter(course__in=courses).select_related('student', 'course')

    context = {
        'courses': courses,
        'enrollments': enrollments,
    }
    return render(request, 'accounts/teacher_enrollments.html', context)

@login_required
def profile_view(request):
    profile = request.user.profile

    context = {'profile': profile}

    if profile.role == 'teacher':
        courses = Course.objects.filter(teacher=profile)
        course_data = []

        for course in courses:
            enrolled_students = Enrollment.objects.filter(course=course)
            course_data.append({
                'course': course,
                'enrollments': enrolled_students
            })

        context['courses'] = course_data

    elif profile.role == 'student':
        enrollments = Enrollment.objects.filter(student=profile).select_related('course')
        grades = {grade.enrollment_id: grade for grade in Grade.objects.filter(enrollment__in=enrollments)}
        context['enrollments'] = [
            {
                'course': enrollment.course,
                'grade': grades.get(enrollment.id)
            }
            for enrollment in enrollments
        ]

    return render(request, 'accounts/profile.html', context)