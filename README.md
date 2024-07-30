# Django Backend Subscription Project

## Overview

Welcome to the Django Backend Subscription Project! This project showcases a backend application built with Django that allows users to create accounts and select different subscription plans. The aim of this project is to demonstrate my proficiency in backend development, including user authentication, subscription management, and API design.

## Features

- **User Registration and Authentication**: Secure user registration and login system with Django's built-in authentication.
- **Subscription Plans**: Users can view and select from various subscription plans.
- **API Endpoints**: RESTful API endpoints for user and subscription management.
- **Admin Panel**: Django's powerful admin panel for managing users and subscriptions.

## Technologies Used

- **Django**: The main framework used for development.
- **Django REST Framework**: For building RESTful APIs.
- **SQLite**: Default database for development and testing.
- **Docker**: For containerization (optional).
- **Git**: Version control.

## Installation and Setup

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/django-backend-subscription.git
    cd django-backend-subscription
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7. **Access the application**:
    - API: `http://127.0.0.1:8000/api/`
    - Admin Panel: `http://127.0.0.1:8000/admin/`

## API Endpoints

Here are some of the key API endpoints available in this project:

- **User Registration**: `POST /api/register/`
- **User Login**: `POST /api/login/`
- **Subscription Plans**: `GET /api/subscriptions/`
- **Select Subscription**: `POST /api/subscriptions/select/`

## Usage

1. **Register a new user** via the `/api/register/` endpoint.
2. **Login** with the registered user credentials using the `/api/login/` endpoint.
3. **View available subscription plans** using the `/api/subscriptions/` endpoint.
4. **Select a subscription plan** by sending a POST request to `/api/subscriptions/select/`.

## Docker Setup (Optional)

For a containerized setup, use Docker:

1. **Build the Docker image**:
    ```bash
    docker build -t django-backend-subscription .
    ```

2. **Run the Docker container**:
    ```bash
    docker run -p 8000:8000 django-backend-subscription
    ```

## Testing

To run tests, use the following command:
```bash
python manage.py test
