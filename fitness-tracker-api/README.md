# 🏋️ Fitness Tracker API

A RESTful API built with Django and Django REST Framework that allows users to log, update, delete, and view their fitness activities. This API helps users track workouts, monitor progress, and view activity history.

---

## 📌 Project Overview

The Fitness Tracker API provides endpoints to manage fitness activities, including:

- Creating fitness activities
- Viewing activity history
- Updating activities
- Deleting activities
- Managing user authentication

This project uses Django ORM for database interactions and Django REST Framework for API development.

---

## 🚀 Features

- User authentication with Token Authentication
- CRUD operations for fitness activities
- Activity history endpoint
- Secure user-specific data handling
- RESTful API design
- SQLite database (default Django database)

---

## 🛠️ Technologies Used

- Python 3.x
- Django
- Django REST Framework
- SQLite
- Git & GitHub

---

## 📁 Project Structure

fitness-tracker-api/
│
├── api/
│ ├── migrations/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
├── fitness_tracker/
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ ├── wsgi.py
│
├── manage.py
├── db.sqlite3
└── README.md
