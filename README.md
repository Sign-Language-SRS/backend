# backend
Sign Language SRS Backend

## Structure of backend:
1. `Dockerfiles/` contains the different 
2. `src/` contains all the source code that the Dockerfiles read from
  a. `api/app.py` is where the factory for the application is
  b. `api/models` contains all the different models
  c. `api/route` contains the different blueprints and routes that'll contain the logic

## Database migrations:
First, go into database migrations and change to the src/ folder

Then perform:
If migrations is not present for some reason
1. flask db init
2. flask db migrate
3. flask db upgrade

If migrations are present
1. flask db upgrade
