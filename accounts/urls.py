# student_mgmt/urls.py

from django.contrib import admin
from django.urls import path
from accounts.views import register, dashboard, user_login, CustomLogoutView
from accounts import views as account_views
from courses import views as course_views
from enrollments import views as enrollment_views
from grades import views as grade_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts
    path('register/', account_views.register, name='register'),
    path('dashboard/', account_views.dashboard, name='dashboard'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    path('login/', user_login, name='login'),

    # Courses
    path('courses/', course_views.course_list, name='course_list'),
    path('courses/create/', course_views.create_course, name='create_course'),

    # Enrollments
    path('enroll/<int:course_id>/', enrollment_views.enroll, name='enroll'),
    path('my-courses/', enrollment_views.my_courses, name='my_courses'),
    path('teacher/enrollments/', account_views.teacher_enrollments, name='teacher_enrollments'),

    # Grades
    path('grades/assign/<int:enrollment_id>/', grade_views.assign_grade, name='assign_grade'),
    path('grades/view/', grade_views.view_grades, name='view_grades'),

    path('profile/', account_views.profile_view, name='profile')
]
