# Module Manager

A web application built with **Django** for managing subject modules. The system allows authenticated users to create, view, edit, and manage their own modules and generate a PDF document from module data.

## Architecture

The project follows Django’s **Model–View–Template (MVT)** architecture:

- **Models** define the data structure and database relations.
- **Views** handle HTTP requests and responses.
- **Templates** render the user interface.

This separation keeps the application modular and easier to maintain.

### Database

The application uses **PostgreSQL** as the database backend. Django’s ORM is used to define models and manage database migrations.

### Design Principles

The project applies the **Single Responsibility Principle**:

- **Models** handle data persistence.
- **Forms** handle validation of user input.
- **Views** handle request routing and responses.
- **Services** implement business logic such as module creation or PDF generation.

Each component is responsible for one clear task, improving readability, maintainability, and testability.

## Features

- User authentication
- Per-user module management
- Module creation and editing
- Viewing module data
- Deleting modules
- PDF generation from module information
- Basic front-end

## Dependencies
- Docker
- django>=6.0.5
- gunicorn>=26.0.0
- psycopg>=3.3.4
- reportlab>=4.5.1  
#### see `pyproject.toml`


## Setup

### Docker setup (recommended):

#### Install dependencies:
```bash
# Install docker:
yay -Syu docker-desktop
```
#### Run 

```bash
# Activate all containers
docker compose up --build
```
This will create a PostgreSQL container **modulemanager-db** published on port `5432:5432` with the following credentials:

- `POSTGRES_DB=djangodb`
- `POSTGRES_USER=djangouser`
- `POSTGRES_PASSWORD=django123`

And **modulemanager-app** container with django on port `8000:8000` with two seed accounts:
- Admin account: `admin:admin`
- User account: `user:user1234`

#### Then you can use the app
- http://localhost:8000/ - the app
- http://localhost:8000/admin - admin panel

#### You can also run database or app containters separately:
```bash
# Web app container
docker compose up web
docker compose up --build web # build the app
docker compose down web

# Database container
docker compose up db
docker compose down db
docker compose down -v db # remove the volume (delete the database)
```

#### To access Django manage.py CLI:
```bash
# after activating containers, run this:
docker exec modulemanager-app python3 manage.py <command>
# for example to run tests, run:
docker exec modulemanager-app python3 manage.py test
```

### Running from source:
You can also run code without docker. All the instructions are for Arch Linux x86_64. 
#### Install dependencies:
```bash
sudo pacman -Syu python postgresql python-psycopg
```
#### Prepare database (postgres):
1. Install the database:
```bash
sudo pacman -Syu postgresql 
```
2. Change user to postgres:
```bash 
sudo -i -u postgres
```
3. Init database:
```bash
initdb -D /var/lib/postgres/data
```
4. Start service:
```bash
sudo systemctl start postgresql.service
```
5. Create user (password django123):
```bash
createuser djangouser --pwprompt --createdb --no-superuser --no-createrole
```
6. Create database:
```bash
createdb djangodb --owner=djangouser
```
7. Create service file and passfile
#### Service file (~/.pg_service.conf):
```
[my_service]
host=localhost
port=5432
dbname=djangodb
user=djangouser
```
#### passfile (~/.my_pgpass):
```
localhost:5432:djangodb:djangouser:django123
```
#### Run Django
```bash
# migrate
python manage.py migrate
# create seed accounts (user:user1234, admin:admin)
python manage.py seed_accounts
# run debug server on 8000 port
python manage.py runserver 0.0.0.0:8000
