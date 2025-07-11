# grades/models.py

from django.db import models
from enrollments.models import Enrollment

class Grade(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)
    graded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grade: {self.enrollment.student.user.username} - {self.enrollment.course.title}"
