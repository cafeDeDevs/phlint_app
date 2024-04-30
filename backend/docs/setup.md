# Django With PosgreSQL Inside Of Docker

This simple repository instructs the user on how to setup a Django Instance with
a Virtualized instance of a PostgreSQL database inside of a Docker Container!

## Quick Start

### Project Dependencies

- Git
- [Python](https://wiki.python.org/moin/BeginnersGuide/Download)
- [Django](https://docs.djangoproject.com/en/5.0/topics/install/#installing-official-release)
- [Docker](https://docs.docker.com/get-docker/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

### Setup Instructions

Clone project locally and navigate to project

```sh
git clone https://github.com/tomit4/django_with_postgres && cd django_with_postgres
```

Create virtual Environment.

> Whenever starting a new python project, you'll then need to utilize commands
> associated with virtualenv, otherwise you could install dependencies globally.

```sh
python3 -m virtualenv django_postgres_docker
```

Activate the the virtual environment

```sh
source django_postgres_docker/bin/activate
```

Install local environment requirements

```sh
pip install -r requirements.txt
```

Copy env-sample to .env (this will be updated later)

```sh
cp env-sample .env
```

Spin Up PostgreSQL in Docker

> This config file will spin up the docker instance of a basic PostgreSQL database. Because of the provided setup.sql and .env files, a very simple database is instantiated for Django to interact with.

```sh
docker-compose -f ./docker-compose.yml up -d
```

Migrate the Database via Django's API:

> This should be run any time there are changes to your model

```sh
python manage.py makemigrations && python manage.py migrate
```

That takes care of the initial setup

### Verifying The Existence Of Our PostgreSQL Database

Check the existence of our database using docker:

```sh
docker exec -it django_db sh
```

Once inside of our docker instance via shell, we can utilize Postgres's built-in
command line interface, `psql` to check the existence of our database:

```sh
psql -d django_db -U admin
```

The name of our database here is the default found in our env-sample file, it is our user.

Within the psql CLI, we see that our database is populated with the default django tables:

```psql
\dt
```

The output should look similar to the following:

```psql
                  List of relations
 Schema |            Name            | Type  | Owner
--------+----------------------------+-------+-------
 public | auth_group                 | table | admin
 public | auth_group_permissions     | table | admin
 public | auth_permission            | table | admin
 public | auth_user                  | table | admin
 public | auth_user_groups           | table | admin
 public | auth_user_user_permissions | table | admin
 public | django_admin_log           | table | admin
 public | django_content_type        | table | admin
 public | django_migrations          | table | admin
 public | django_session             | table | admin
(10 rows)
```

Exit PostgreSQL

```psql
\q
```

### Quick Exit

Deactivate the virtual environment

```sh
deactivate
```

Thats it! For additional information on the above steps continue reading.

## Specifics Of Django With Postgres/Docker

This project uses a `.env` file, a `setup.sql` file, a `docker-compose.yml` file, and
also makes adjustments to the `settings.py` file within the `myproject` directory to quickly
setup a very basic postgres database within a docker container that Django can
interact with. At this time there are no models and/or mock data.

Adjust the following in your `settings.py` file first:

```python
# at the top of the file:
import os
from dotenv import load_dotenv

load_dotenv()
# ...
# And here we change the database configuration to use postgresql and our secret
# environment variables:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_DB'),
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASS'),
        'HOST': os.getenv('PG_HOST'),
        'PORT':
        os.getenv('PG_PORT'),
        #  'ALLOWED_HOSTS': [''],
    }
}
```

Like most dotenv middleware, you need a .env file which holds onto these environment variables, I have provided a basic `env-sample` file that you can copy and then change based off your project needs:

```sh
cp env-sample .env
# Change env variables as you see fit in your text editor of choice
```

To exit the docker shell session

```sh
exit
```

### Spinning Up PostgreSQL in Docker

Now all that's needed is to run `docker-compose` to instantiate the postgresql database:

```sh
docker-compose -f ./docker-compose.yml up -d
```

This config file will spin up the docker instance of a basic PostgreSQL database. Because of the provided `setup.sql` and `.env` files, a very simple database is instantiated for Django to interact with.

### Migrating the Database via Django's API

Django provides a very simple API to migrate a database quickly. Simply invoke these two commands to connect Django to our Virtualized PostgreSQL instance:

```sh
python manage.py makemigrations && python manage.py migrate
```

Because we don't have any Models defined yet, Django will set up a basic table in the database we just spun up.

## Resources

- [How To Use PostgreSQL with your Django Application on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04)
- [VirtualEnv Virtual Guide](https://virtualenv.pypa.io/en/latest/user_guide.html)
