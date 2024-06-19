# sms-fast-api

## Local development

### Database

For setting up a local database follow below instruction.
To run the application locally, you need to setup a postgres database on your system.
Install postgres

```
sudo apt install postgresql libpq-dev
```

Login as the 'postgres' user and start postgres shell

```
sudo su - postgres
psql
```

Create a database

```
create database smscampaigner;
```

Create a user

```
create user username with password ‘pswd’
```

Grant all privileges to user

```
grant all privileges on database smscampaigner to username;
```

Follow below instructions after setting up database.

create a .env file and replace your DATABASE_URL

```
cp env.example .env
```

Whenever a database migration needs to be made. Run the following commands

```
alembic revision --autogenerate -m "initial migration"
```

This will generate a new migration script. Then run

```
alembic upgrade head
```

### TO RUN

```
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### API Docs

```
http://127.0.0.1:8000/docs
```

### TO RUN TEST

```
 python scrpt.py
```

```
 pytest --cov=app --cov-report=html
```

now you can access the report using the below url

```
http://127.0.0.1:5500/htmlcov/z_6549c0330f733809_auth_py.html
```

### TO ACCESS LOGS

```
tail -f app.log
```

### TO RUN USING DOCKER

```
bash run.sh
```

to stop container

```
docker ps
docker stop <containerid>
```
