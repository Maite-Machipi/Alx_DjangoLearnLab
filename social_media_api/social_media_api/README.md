Social Media API
Overview

The Social Media API is a Django REST Framework-based backend that provides user authentication and profile management functionality. It allows users to register, log in, receive authentication tokens, and manage their profiles securely.

This project is part of the Alx_DjangoLearnLab and demonstrates best practices in API development, authentication, and custom user models.

Features

Custom User Model

User Registration

User Login with Token Authentication

User Profile View and Update

Token-based Authentication using DRF

Secure password handling

Followers relationship between users


Technologies Used

Python 3

Django 6+

Django REST Framework

SQLite (default database)

Token Authentication

social_media_api/
│
├── social_media_api/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── manage.py
└── README.md


Testing with Postman

Steps:

1. Register a user

2. Copy token

3. Use token in Authorization header

4. Access profile endpoint

Security Features

Token Authentication

Password hashing

Permission-based access control

Future Improvements

Posts system

Comments system

Follow/Unfollow users

Like system

Messaging system

Author

Maite Marageni
ALX back-end project

Repository

GitHub:
https://github.com/YOUR_USERNAME/Alx_DjangoLearnLab

License
This project is for educational purposes

