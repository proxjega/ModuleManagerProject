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