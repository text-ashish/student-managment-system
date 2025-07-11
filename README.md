# 🎓 Django Student Management System

A feature-rich, full-stack **Student Management System** built with **Django**, offering seamless user registration, role-based dashboards, course management, and enrollment tracking for students and teachers. Admins can manage user roles and access levels efficiently.

---

## 🚀 Features

### 🢑 User Authentication & Roles

* Custom user registration with `username`, `email`, `password`, and **role selection** (`student`, `teacher`)
* Secure login/logout using Django's auth system
* CSRF-protected forms
* Role-based access control:

  * **Student**: Can view enrolled courses and grades
  * **Teacher**: Can view and manage enrollments in their courses
  * **Admin**: Can view all users, assign roles, and delete accounts

### 📚 Course Management

* Teachers can **create and manage courses**
* Teachers can view all **student enrollments** in their courses
* Students can enroll in available courses

### 🎯 Dashboard & Profiles

* Custom **dashboard views** for each user type
* Profile page with dynamic content:

  * **Teachers**: See courses they teach and enrolled students
  * **Students**: See enrolled courses and grades

### 🛡 Admin Controls

* Admin panel with:

  * User listing with roles
  * Edit user role page
  * Delete user confirmation

---

## 🛠 Tech Stack

| Layer     | Technology                             |
| --------- | -------------------------------------- |
| Framework | Django 5.x                             |
| Language  | Python 3.13                            |
| Frontend  | HTML5, CSS3                            |
| Templates | Django Templates + `widget_tweaks`     |
| DB Models | Django ORM                             |
| Styling   | Custom CSS + minimal responsive design |

---

## 🏧 Project Structure (Highlights)

```
student_mgmt/
│
├── accounts/
│   ├── views.py                # All role-based views
│   ├── models.py               # Profile with user roles
│   ├── forms.py                # Custom registration form
│   └── templates/accounts/     # HTML templates for registration, login, dashboard, etc.
│
├── courses/
│   ├── models.py               # Course model
│   ├── views.py                # Course creation logic
│
├── enrollments/
│   ├── models.py               # Enrollment and Grade models
│
├── templates/
│   └── base.html               # Shared layout
│
└── manage.py
```

---

## 🧹 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/student-mgmt.git
cd student-mgmt
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Migrate Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (for Admin)

```bash
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

Now visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Usage Guide

### 🔐 Registration Flow

* Visit `/accounts/register/`
* Choose role: `Student` or `Teacher`
* On registration, the system creates a `Profile` and logs the user in

### 🧑‍🏫 Student Dashboard

* View enrolled courses
* View grades (if available)

### 🧑‍🏫 Teacher Dashboard

* View courses created
* View enrolled students per course

### 🛡 Admin Panel

* Go to `/accounts/user-list/`
* Edit or delete users
* Assign roles (`student`, `teacher`, `admin`)

---

## 🎨 Screenshots (Optional)

Add screenshots of:

* Dashboard for Student and Teacher
* Admin User Management
* Registration form

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contribution

Feel free to fork and contribute! Pull requests are welcome.

---

## 👨‍💼 Author

**Ashish Kumar**
💼 [LinkedIn](https://linkedin.com) • 📧 [ashish@example.com](mailto:ashish@example.com)

---
