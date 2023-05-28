# DJANGO POLLING APP API: Minimal stuffs

## Prerequisites

Install the following prerequisites:

1. [Python](https://www.python.org/downloads/)
2. [PostgreSQL](https://www.postgresql.org/download/)

## Installation

### 1. Create a virtual environment

From the **root** directory run:

```bash
python -m venv env
```

### 2. Activate the virtual environment

From the **root** directory run:

On macOS:

```bash
source env/bin/activate
```

On Windows:

```bash
env\scripts\activate
```

### 3. Install required dependencies

From the **root** directory run:

```bash
pip install -r requirements.txt
```

### 4. Set up a PostgreSQL database

With **PostgreSQL** up and running, in a new Terminal window run:

```bash
dropdb --if-exists django_polls
```

Start **psql**, which is a terminal-based front-end to PostgreSQL, by running the command:

```bash
psql postgres
```

Create a new PostgreSQL database:

```sql
CREATE DATABASE django_polls;
```

Create a new database admin user:

```sql
CREATE USER yourusername WITH SUPERUSER PASSWORD 'yourpassword';
```

To quit **psql**, run:

```bash
\q
```

### 5. Set up environment variables

Setup your database by editing `.env` config file. Replace `yourusername` by your postgresql username and
`yourpassword` by your postgresql password.

### 6. Run migrations

From the **root** directory run:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 7. Create an admin user to access the Django Admin interface

From the **root** directory run:

```bash
python manage.py createsuperuser
```

When prompted, enter a username, email, and password.

## Run the application

From the **root** directory run:

```bash
python manage.py runserver
```

### View the application

#### URLs

- Docs URL: <http://127.0.0.1:8000/api/docs/>
- UI Docs URL: <http://127.0.0.1:8000/api/docs/ui/>
- No base URL (<http://127.0.0.1:8000/> raises an Http404 Error)

## Add data to the application

Add data through Django Admin.

- Go to <http://127.0.0.1:8000/admin/> to access the Django Admin interface and sign in using the admin credentials.
- Or add data through the API while by sending a POST request to <http://127.0.0.1:8000/api/polls/>. It requires
an admin account. So you should send a request with login credentials.
