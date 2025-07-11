from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Grade
from enrollments.models import Enrollment

@login_required
def assign_grade(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    # Get the latest grade (if any)
    latest_grade = Grade.objects.filter(enrollment=enrollment).order_by('-graded_on').first()

    if request.method == 'POST':
        score = request.POST.get('score')
        feedback = request.POST.get('feedback')

        if latest_grade:
            # Update the latest grade instead of creating a duplicate
            latest_grade.score = score
            latest_grade.feedback = feedback
            latest_grade.save()
        else:
            # Create new grade
            Grade.objects.create(enrollment=enrollment, score=score, feedback=feedback)

        return redirect('enrollment_detail', enrollment_id=enrollment.id)

    return render(request, 'grades/assign_grade.html', {
        'enrollment': enrollment,
        'grade': latest_grade
    })
@login_required
def view_grades(request):
    profile = request.user.profile
    if profile.role == 'student':
        grades = Grade.objects.filter(enrollment__student=profile)
    else:
        grades = Grade.objects.none()
    return render(request, 'grades/view_grades.html', {'grades': grades})