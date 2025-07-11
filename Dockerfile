# Use official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run Django using Gunicorn (you can change this if needed)
CMD ["gunicorn", "student_mgmt.wsgi:application", "--bind", "0.0.0.0:8000"]
