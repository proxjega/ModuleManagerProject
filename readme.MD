# PROJECT IS UNFINISHED
## Right now this works:
- Registration
- Login
- View profile
- Create module
- View modules
### More features are coming soon!

# Module Manager

A web application built with **Django** for managing subject modules. The system allows authenticated users to create, view, edit, and manage their own modules and generate a PDF document from module data.

## Architecture

The project follows Django’s **Model–View–Template (MVT)** architecture:

- **Models** define the data structure and database relations.
- **Views** handle HTTP requests and responses.
- **Templates** render the user interface.

This separation keeps the application modular and easier to maintain.

## Design Principles

The project applies the **Single Responsibility Principle**:

- **Models** handle data persistence.
- **Forms** handle validation of user input.
- **Views** handle request routing and responses.
- **Services** implement business logic such as module creation or PDF generation.

Each component is responsible for one clear task, improving readability, maintainability, and testability.

## Database

The application uses **PostgreSQL** as the database backend. Django’s ORM is used to define models and manage database migrations.

## Features

- User authentication
- Per-user module management
- Module creation and editing
- Viewing module data
- PDF generation from module information
## Instalation
### Install dependencies:
```bash
sudo pacman -Syu python postgresql python-psycopg
```
### Prepare database (postgres):
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
