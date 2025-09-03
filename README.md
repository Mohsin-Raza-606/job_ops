# JobOps API

JobOps is a **Django REST Framework (DRF)** based backend service for managing jobs, tasks, and assignments.  
It includes role-based access control (Admin, Sales Agent, Technician), overdue job tracking with Celery,  
and modern API documentation powered by drf-spectacular.

---

## 🚀 Tech Stack

- **Python**: Python 3.12.11  
- **Backend Framework**: Django 5.2.5  
- **API Layer**: Django REST Framework 3.16.1  
- **Database**: PostgreSQL + psycopg2-binary  
- **Task Queue**: Celery 5.5.3  
- **Message Broker**: Redis 6.4.0  
- **Auth**: JWT (djangorestframework-simplejwt)  
- **API Docs**: drf-spectacular 0.28.0  
- **Configuration**: django-environ  

---

## ✨ Features

- 🔐 **JWT Authentication** with role-based permissions (Admin, Sales Agent, Technician).  
- 📋 **Job Management** with status, priority, and scheduling.  
- 🛠️ **Task Management** with equipment assignments.  
- 👷 **Job Assignments** for technicians.  
- ⚡ **Overdue Job Detection** with scheduled Celery tasks.  
- 📑 **Interactive API Docs** (Swagger & Redoc via drf-spectacular).  
- 🔎 **Filtering & Search** (status, priority, overdue, etc).  
- 🗑️ **Soft Delete / Reactivation** for jobs, tasks, and assignments.  

---

## ⚙️ Installation

Clone the repository:

    git clone https://github.com/your-org/jobops.git
    cd jobops

Create and activate a virtual environment:

    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

Apply migrations:

    python manage.py migrate

Create a superuser:

    python manage.py createsuperuser

Run the development server:

    python manage.py runserver

---

## 🔑 Environment Variables

We use **django-environ**. Create a `.env` file in the project root:

    DEBUG=True
    SECRET_KEY=your_secret_key_here

    # Database
    DATABASE_URL=postgres://user:password@localhost:5432/jobops

    # Redis
    REDIS_URL=redis://localhost:6379/0

    # Django settings
    ALLOWED_HOSTS=127.0.0.1,localhost

    # JWT
    SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=3600
    SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=86400

---

## ⏱️ Celery & Redis

Start a Redis server:

    redis-server

Start Celery worker:

    celery -A config worker -l info

Start Celery beat (for scheduled tasks like overdue jobs):

    celery -A config beat -l info

---

## 📖 API Documentation

Once the server is running, you can access:

- **ReDoc UI** → http://127.0.0.1:8000/api/docs/  
- **Schema JSON** → http://127.0.0.1:8000/api/schema/  

---

## 🧪 Running Tests

Run tests:

    python manage.py test

(Optional: with coverage)

    coverage run manage.py test
    coverage report -m

---

## 📝 Coding Style

- Follow **PEP8** guidelines.  
- Use **black** for code formatting:

    pip install black
    black .

---

## 📂 Project Structure

    jobops/
    ├── config/              # Django project settings & Celery config
    ├── jobs/                # Job, Task, and Assignment app
    ├── users/               # Custom User model & permissions
    ├── requirements.txt
    ├── manage.py
    └── README.md

---

## 🤝 Contributing

1. Fork the repo  
2. Create your feature branch (`git checkout -b feature/my-feature`)  
3. Commit your changes (`git commit -m 'Add my feature'`)  
4. Push to the branch (`git push origin feature/my-feature`)  
5. Open a Pull Request  

---


