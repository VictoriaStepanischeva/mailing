mailing
=======

This application provides a simple mail exchange service. The following actions are implemented:
* User sign up, login and logout
* Message listing (both inbox and sent), fetching the given message, its deletion and toggling tag whether the incomming message is read or not.

## Deploy

The application can be deployed with `./mailing.start` script that builds and starts two containers (db and app).

## Requirements

All packages and modules required for the application are installed within the corresponding docker images. Only docker and docker-compose are required on the host machine.

## Technologies

The application is implemented using Django Python framework (3.0) and the next addons:
* mysql-connector-python (8.0.19)
* mysqlclient (1.4.6)
* djangorestframework (3.11.0)
* djangorestframework-jwt (1.11.0)
* drf-yasg (1.17.1)

Also MySQL (8.0) is used as a DBMS for the project.

## Docs

Documentation is based on project docstrings and converted to html with swagger. It is available via http://0.0.0.0:8000/swagger/ when the service is running.

![image](/swagger.jpg)

## Testing

To run existing test suite just run `docker-compose run app python manage.py test`