# Bank API

A simple local server, that query the data from the Narodowy Bank Polski's public APIs and returns relevant information from them.

## Endpoints:

- `http://localhost:8000/api/v1/average/<currency code>/<date>/` 
This function takes a date (YYYY-MM-DD) and a currency code as arguments and returns the average exchange rate for the given date. Note that the bank does not provide data for weekends or holidays.
```
http://localhost:8000/api/v1/average/usd/2023-03-01/
```
E.g. the above query returns `{"average rate": 4.4094}`

- `http://localhost:8000/api/v1/minimax/<currency code>/<number of records>/`
This function takes a currency code and a number of records as arguments and returns the minimum and maximum average exchange rates for the requested period. The maximum number of records is 255, and the minimum is 1.
```
http://localhost:8000/api/v1/minimax/usd/255/
```
The above query returns `{"minimum average value": 4.1905, "maximum average value": 5.0381}`

- `http://localhost:8000/api/v1/diff/<currency code>/<number of records>/`
This function takes a currency code and a number of records as arguments and returns the bid-ask spread for the requested period. The maximum number of records is 255, and the minimum is 1.
```
http://localhost:8000/api/v1/diff/usd/60/
```
This query returns `{"major difference": 0.09}`

- `http://localhost:8000/api/v1/codes/`
This function returns a list of currency codes supported by the bank.

## Setup project using Docker
(see Makefile for additional information)

#### Create and activate a virtual environment

- `make venv`
OR
- `python3 -m venv venv && source venv/bin/activate`


#### Create an image

- `make image`
OR
- `docker build -t nbp .`

#### Build a container

- `make container`
OR
- `docker run --name nbp_cont -dp 8000:8000 nbp`

#### Apply migrations and use the application

- `make migrate`
OR
- `docker exec -it nbp_cont python nbp_api/manage.py makemigrations`
- `docker exec -it nbp_cont python nbp_api/manage.py migrate`

The application is accessible on `http://127.0.0.1:8000/` or `http://localhost:8000/`.

#### To run unit tests

- `make test`
OR
- `cd nbp_api/ && python manage.py test`

#### To stop the container

- `make stop_cont`
OR
- `docker stop nbp_cont`

#### To destroy the container

- `make delete_cont`
OR
- `docker rm nbp_cont`

#### To destroy the image

- `make delete_image`
OR
- `docker rmi nbp:latest`


## Setup project on Windows

#### Create and activate a virtual environment on Windows

- `python -m venv venv`
- `venv\Scripts\activate`

#### Create and activate a virtual environment on Linux

- `python3 -m venv venv && source venv/bin/activate`

#### Install dependencies

- `pip install --upgrade pip`
- `pip install -r requirements.txt`

#### Apply migrations

- `python nbp_api/manage.py makemigrations`
- `python nbp_api/manage.py migrate`

#### Run the server

- `python nbp_api/manage.py runserver`

The application is accessible on `http://127.0.0.1:8000/` or `http://localhost:8000/`.

#### To run unit tests

- `cd .\nbp_api\`
- `python manage.py test`