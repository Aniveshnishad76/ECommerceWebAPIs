## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Built Using](#built_using)

## 🧐 About <a name = "about"></a>

This application will serve APIs to Ecommerce web application.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

1. [Python](https://www.python.org/downloads/release/python-390/)
2. [Pipenv](https://pypi.org/project/pipenv/)
3. [Redis](https://redis.io/)
4. [Celery](https://readthedocs.org/projects/celery/)


--------------
## Setup Process

- Clone the repository

    ```bash
    git clone https://github.com/Aniveshnishad76/ECommerceWebAPIs.git
    ```

- Create and setup the virtual env for [python](https://docs.python.org/3/library/venv.html).

```bash 
      python -m venv .venv
      .venv\Scripts\activate (for windows)
```

- Install all the dependencies in venv : this command will use the already present Pipfile to install dependencies.
    ```bash
    pip install -r requirements.txt
    ```

- Create a database and then either store the credentials in global variable from terminal, or create a .env file and store them there. This is required by alembic to make db connection.
- Optional : if alembic version is not present, generate one.
    ```bash
    alembic -c ./src/alembic.ini revision --autogenerate -m "1st version"
    ```
- Create database schema using alembic
    ```bash
    alembic -c ./src/alembic.ini upgrade head
    ```
    if there are any error in this command check
    - database connection and credentials
    - already present schema


- Run the fastapi server
    ```bash
    uvicorn --reload src.main:app
    ```
    ** mac users remove --reload form above command if it keeps reloading


- Run the celery worker and beat command
   ```bash
  celery -A src.tasks.tasks beat --loglevel=info
  celery -A src.tasks.tasks worker --loglevel=info
  ```
  
## ⛏️ Built Using <a name = "built_using"></a>

- [Postgres](https://www.postgresql.org/) - Database
- [FastAPI](https://fastapi.tiangolo.com/) - Python Framework
- [Uvicorn](https://www.uvicorn.org/) - Application Server
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Migration tool
- [Aioredis](https://aioredis.readthedocs.io/en/latest/) - Redis Library