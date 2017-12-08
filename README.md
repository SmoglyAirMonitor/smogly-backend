[![Build Status](https://travis-ci.org/SmoglyAirMonitor/smogly-backend.svg?branch=master)](https://travis-ci.org/SmoglyAirMonitor/smogly-backend)

# smogly-backend
API and simple web interface for SmoglyAirMonitor project. Powered by Django

**smogly-backend** provides backend API to which your air quality sensors can send data. It also provides monitoring station management, user management and simple frontend to present data. You can use this project to start awareness campaign in you local area.

# Development with Docker

## To start development:
1. install [docker](https://docs.docker.com/#/components) and [docker-compose](https://docs.docker.com/compose/install/)
2. run `docker-compose build` to build web container
3. run `docker-compose up web` to test web and db containers
5. run `docker-compose run web python manage.py migrate` to apply migrations
6. run `docker-compose run web python manage.py createsuperuser` to create admin account

## To run project:
1. run `docker-compose up web`
2. point your browser to `localhost:8080`
3. press `CTRL+C` to stop

## Notes:
1. To run command inside container you can use run entrypoint command. 
I.e. `docker-compose run web py.test -s --cov=. --cov-report=html` to run unit tests and check coverage.
I.e. `docker exec -it smoglybackend_web_db_1 psql -U docker -d docker` when you want access to database

2. We recommend setting up bash aliases to **increase productivity**:

```bash
#!/bin/bash
dcclear() {
    docker images -qf dangling=true | xargs -r docker rmi
    docker volume ls -qf dangling=true | xargs -r docker volume rm
}
alias dc='docker-compose'
alias dcrun='docker-compose run --rm'
alias dcmanagepy='dcrun web python manage.py'
```

## API documentaion:
Check http://localhost:8080/api/v1/docs/ to find full REST API documentation.
