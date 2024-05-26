# Initial Setup For Phlint App

## Introduction

This document covers the initial setup instructions for new contributors to
Phlint App! Before getting started, it is assumed you have a basic understanding
of the following project dependencies:

### Project Dependencies

- Git
- [Python](https://wiki.python.org/moin/BeginnersGuide/Download)
- [Django](https://docs.djangoproject.com/en/5.0/topics/install/#installing-official-release)
- [Docker](https://docs.docker.com/get-docker/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [NPM](https://www.npmjs.com/)
- [mkcert](https://github.com/FiloSottile/mkcert)

Should you have any questions or concerns, please feel free to reach out to the
[Project Lead](https://github.com/tomit4) or one of your fellow contributors in the Group Discord.

### Backend Setup

Clone project locally and navigate to project

```sh
git clone https://github.com/cafeDeDevs/phlint_app && cd backend
```

Create virtual Environment.

> Whenever starting a new python project, you'll then need to utilize commands
> associated with virtualenv, otherwise you could install dependencies globally.

```sh
python3 -m virtualenv env
```

Activate the the virtual environment

```sh
source env/bin/activate
```

Install local environment requirements

```sh
pip install -r requirements.txt
```

Copy env-sample to .env (this will be updated later)

```sh
cp env-sample .env
```

Providing Google OAuth2 Credentials

Within the .env file, you'll need to provide your Google OAuth2 credentials. You
can request these credentials by contacting the [Project Lead](https://github.com/tomit4).
Once you have said credentials, fill in the corresponding fields, specifically
the following fields:

```.env
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=""
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=""
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI =""
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

And Exit the Docker Container:

```sh
exit
```

### Generating Local SSL Certs

This project's development environment utilizes locally generated SSL
certificates to most closely mimic production level authentication strategies.

You'll need to utilize the [mkcert](https://github.com/FiloSottile/mkcert)
package to generate the necessary `cert.pem` and `key.pem` files. You can do
this from the command line by invoking the following from within the project's
`backend` directory:

```sh
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1 && \
mkcert -install
```

This will generate local SSL certificates that can be used on localhost, and
also install them into your browser's SSL registry so that they will be
recognized.

### Starting The Backend Server

For your convenience, the backend directory has a simple script called `start`,
which can be invoked from the command line regardless of which Operating
System you utilize. From within the `backend` directory, invoke the following:

```sh
./start
```

### Frontend Setup

By comparison to the Backend Setup, setting up the frontend is much more
straight forward. From the root directory of the project, navigate into the
`frontend` directory. You'll first need to install the dependencies using `npm`:

Install Dependencies

```sh
npm install
```

Next You'll need to copy the `env-sample` file as `.env`:

```sh
cp env-sample .env
```

Providing Google OAuth2 Credentials

Within the .env file, you'll need to provide your Google OAuth2 credentials. You
can request these credentials by contacting the [Project Lead](https://github.com/tomit4).
Once you have said credentials, fill in the corresponding fields, specifically
the following fields:

```.env
VITE_GOOGLE_OAUTH2_CLIENT_ID=
```

Note that this is the same client_id provided for the backend, so if you already
have set up those credentials, simply put the same client_id string from the
backend here in the frontend.A

Starting the Frontend Server

And that's it for the frontend! All that's left is to start the development
server:

```sh
npm run dev
```

This should start up the development server, note that this development server
also uses a local `https` server instead of `http`, but due to the use of a
package called `@vitejs/plugin-basic-ssl`, we don't have to do nearly as much
work to get `ssl` working here.

In your browser, enter the following URL:

```
https://localhost:5173
```

Note that during the backend installation/setup process we generated local `SSL`
certs and then provided them to our browser's recognized SSL registry using
`mkcert -install`. The browser will still warn you that the page you are
visiting is not private, but because we are solely working within a development
environment on our local machine, we will forego these warnings by clicking on
the <em>Advanced</em> key, and then twice clicking on the <em>Proceed to
localhost(unsafe)</em> link (or <em>Accept Risk And Continue</em> if using firefox).

### What To Do If Something Goes Wrong

Contributors are encouraged to first troubleshoot on their own should something
go wrong. Read the error messages, look over the documentation and code, and
give it an honest try when first encountering bugs, errors, and unexpected
behavior.

That said, this is a Group Project, and should your initial attempts to resolve
the issue fail, feel free to reach out to the [Project Lead](https://github.com/tomit4)
or other developers on the Group Project's Discord.
