# Quotes Web Application (Django & MongoDB Migration)

A full-featured Web Application built with Django that allows users to explore, search, and manage famous quotes, authors, and tags. The project features full user authentication, custom user profiles, email password reset capabilities, and an automated migration utility to import legacy data from MongoDB Atlas into a relational database.

---

## Features

- **Quote Management**: Browse quotes with pagination, view detailed author profiles, and filter quotes by tags.
- **User Authentication**: Complete user lifecycle including Sign Up, Login, Logout (via POST request for security), and Profile management.
- **Password Reset**: Email-based password recovery via SMTP integration.
- **Data Migration Tool**: Automated script using PyMongo and Django ORM to migrate legacy MongoDB data (`authors` & `quotes` collections) directly into PostgreSQL/SQLite without duplicating records.
- **Secure Configuration**: Environment variables managed via `.env` files for security and easy deployment.
- **Modern UI**: Clean and responsive layout built with Bootstrap 5.

---

## Tech Stack

- **Backend**: Python 3.14, Django 6.1
- **Databases**: Relational DB (PostgreSQL / SQLite) for Django ORM, MongoDB Atlas (Source for data migration)
- **Dependency Management**: Poetry
- **Containerization**: Docker & Docker Compose (Optional for local PostgreSQL setup)
- **Frontend**: HTML5, CSS3, Bootstrap 5

---

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- **Python** (v3.11 or higher)
- **Poetry** (Python package manager)
- **Git**

---

### 1. Installation

Clone the repository and navigate to the project directory:

######################################TBD##################################################################

```bash
git clone [https://github.com/your-username/Quotes_Django.git](https://github.com/your-username/Quotes_Django.git)
cd Quotes_Django
```

Install the dependencies using Poetry:

```bash
poetry install
```
### 2. Environment Setup
Create a .env file in the root directory of the project and configure the required environment variables:

```bash
# Django Settings
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings (PostgreSQL / SQLite)
DATABASE_NAME=quotes_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# MongoDB Atlas (Legacy Source Data for Migration)
MONGO_USER=your_mongo_username
MONGO_PASS=your_mongo_password
MONGO_DB_NAME=quote_db
MONGO_DOMAIN=cluster_domain.mongodb.net

# Email Settings (for Password Reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```


### 3. Database Setup & Migrations
Run Django migrations to create the relational database schema:

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```
Create an administrative superuser account:

```bash
poetry run python manage.py createsuperuser
```
### 4. Data Migration from MongoDB (Optional)
If you have legacy data in a MongoDB cluster, you can run the built-in migration utility to transfer authors and quotes into your Django database:

i. You can scrap data from http://quotes.toscrape.com/
```bash
cd mgr_django/utils/scraping/scrap_quotes_authors/
poetry run scrapy crawl authors_quotes_spider
```
This will create 2 jsons files in mgr_django/utils/scraping/json (authors.json and quotes.json)


ii. Seed Data into MongoDB

a. **Set up MongoDB Atlas**:
   - Create an account on [MongoDB Atlas](https://www.mongodb.com/atlas/database) and launch a cluster.
   - Obtain your connection URI and database details for `quote_db`.
   - Update your `.env` file with your MongoDB credentials (`MONGO_USER`, `MONGO_PASS`, `MONGO_DOMAIN`, `MONGO_DB_NAME`).

b. **Run the Import Script**:
   From the project root directory, execute:

   ```bash
   poetry run python mgr_django/utils/scrapped_json_to_mongo/quotes_and_authors_to_mongoDB.py
   ```


iii. Django Migration

Run poetry run python -m mgr_django.utils.migration to parse records from MongoDB and insert them into Django's relational database (PostgreSQL)

```bash
poetry run python -m mgr_django.utils.migration
```
### 5. Running the Application
Start the local Django development server:

```bash
poetry run python manage.py runserver
```

Open your browser and visit:

Web App: http://127.0.0.1:8000/

Admin Panel: http://127.0.0.1:8000/admin/

## Project Structure

The project follows a modular architecture separating web application logic, user management, web scraping, and database migration tasks:

```text
Quotes_Django/
├── mgr_django/                     # Main Django configuration directory
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
│   └── utils/                      # Core utility packages
│       ├── conect.py               # MongoDB connection helper
│       ├── migration.py            # Migration script (MongoDB -> PostgreSQL/Django ORM)
│       ├── scraping/               # Scrapy module for quotes/authors web scraping
│       │   ├── json/               # Output JSON files from scraping
│       │   └── scrap_quotes_authors/ # Scrapy spider setup
│       └── scrapped_json_to_mongo/ # MongoEngine script to seed JSON data to MongoDB
├── quotes/                         # Main Django app (Quotes, Authors, Tags management)
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── templatetags/               # Custom Django template tags
├── users/                          # User authentication & profile management app
│   ├── models.py
│   ├── views.py
│   ├── signals.py                  # Automatic profile creation signals
│   └── templates/                  # Login, Signup, and Password Reset views
├── media/                          # User-uploaded files and default avatars
├── docker-compose.yml              # Container setup for local DB and services
├── manage.py                       # Django management runner
├── pyproject.toml                  # Poetry dependencies file
└── README.md