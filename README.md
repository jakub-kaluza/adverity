# Star Wars Explorer

Simple django application enabling exploring the world of our favourite franchise.

## Configuration

`settings.py` file defines full run configuration.

## How to run Star Wars Explorer

Simplest way to run the app is to use docker-compose. As explained below.

### Docker

Initialization scripts should set up the application and the database.

1. Change `DATA_PATH` environmental variable in `docker-compose.yml` in the web section. It's where datasets are going to be downloaded on your machine.
2. Run all the containers with `docker-compose up`.

### As a standalone app

1. In `settings.py` set `DATA_PATH` to a convenient location.
2. Setup postgres database. You can inspire yourself with `init-database.sh` script.
3. `python -m pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver 0.0.0.0:8000`

## Testing

App is provided with some unittests, written in django testing framework. To run the tests:

1. Setup virtualenv.
2. Change `.env` file and source it `export $(grep -v '^#' .env | xargs)`
3. Setup your `PYTHONPATH` to the projects directory.
4. `python manage.py test starwars_explorer`

## Possible Improvments

This application is a rather simple but it could be imprved in following ways:

1. Rewrite frontend in React or similar modern framework.
2. Use docker secrets to make passwords more secure.
3. Create authentication and authorisation and create datasets per user.
4. Create permissions to access files.
5. Use Celery or Redis Queue to download datasets so the user does not need to wait for the fetch response.
6. Could be rewritten as REST api for example in DRF.