# Django Backend Subscription Project

## Overview

Welcome to the Django Backend Subscription Project! This project showcases a backend application built with Django that allows users to create accounts and select different subscription plans. The aim of this project is to demonstrate my proficiency in backend development, including user authentication, subscription management, and API design.

## Features

- **User Registration and Authentication**: Secure user registration and login system with Django's built-in authentication.
- **Subscription Plans**: Users can view and select from various subscription plans.
- **API Endpoints**: RESTful API endpoints for user and subscription management.
- **Admin Panel**: Django's powerful admin panel for managing users and subscriptions.


## Technologies Used

- **Django**: ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
- **Django REST Framework**: ![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=for-the-badge&logo=django&logoColor=white)
- **SQLite**: ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
- **PostgreSQL**: ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
- **Docker**: ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
- **GitHub Actions**: ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
- **Railway**: ![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)
- **Git**: ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

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

## Future Enhancements

Add more subscription features like trial periods and discounts.
Integrate payment gateway for subscription purchases.
Enhance the API with more detailed user and subscription analytics.
Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements. Your contributions are always welcome!

## Contact
If you have any questions or would like to discuss the project, please contact me at athravtonape1001@gmail.com
