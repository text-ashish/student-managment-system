from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from courses.models import Course
from enrollments.models import Enrollment
from grades.models import Grade
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed the database with realistic data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write("🧹 Clearing old data...")
        User.objects.exclude(is_superuser=True).delete()
        Course.objects.all().delete()
        Enrollment.objects.all().delete()
        Grade.objects.all().delete()

        self.stdout.write("👩‍🏫 Creating teachers...")
        teachers = []
        for _ in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            user = User.objects.create_user(
                username=f"{first_name.lower()}.{last_name.lower()}",
                password="pass1234",
                first_name=first_name,
                last_name=last_name,
                email=fake.email()
            )
            profile = Profile.objects.create(user=user, role="teacher", bio=fake.text(max_nb_chars=100))
            teachers.append(profile)

        self.stdout.write("🎓 Creating students...")
        students = []
        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            user = User.objects.create_user(
                username=f"{first_name.lower()}.{last_name.lower()}",
                password="pass1234",
                first_name=first_name,
                last_name=last_name,
                email=fake.email()
            )
            profile = Profile.objects.create(user=user, role="student", bio=fake.sentence())
            students.append(profile)

        self.stdout.write("📚 Creating courses...")
        course_titles = [
            "Introduction to Psychology",
            "Advanced Machine Learning",
            "World History: 1500-Present",
            "Organic Chemistry",
            "Data Structures and Algorithms",
            "Creative Writing Workshop",
            "Microeconomics",
            "Modern Art Appreciation"
        ]

        courses = []
        for title in course_titles:
            course = Course.objects.create(
                title=title,
                description=fake.paragraph(nb_sentences=3),
                teacher=random.choice(teachers)
            )
            courses.append(course)

        self.stdout.write("📝 Enrolling students in courses...")
        for student in students:
            selected_courses = random.sample(courses, k=random.randint(2, 4))
            for course in selected_courses:
                Enrollment.objects.get_or_create(student=student, course=course)

        self.stdout.write("🏅 Assigning grades to enrolled students...")
        feedback_pool = [
            "Outstanding performance!",
            "Very good work.",
            "Satisfactory understanding.",
            "Needs improvement.",
            "Incomplete work."
        ]

        for enrollment in Enrollment.objects.all():
            Grade.objects.create(
                enrollment=enrollment,
                score=random.randint(50, 100),
                feedback=random.choice(feedback_pool)
            )

        self.stdout.write(self.style.SUCCESS("✅ Realistic data seeding complete!"))
