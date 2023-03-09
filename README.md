## Problem statement

In this problem we’ll create a micro-service to address some functionality which is useful to
derive simplified summary statistics (mean, min, max) on a dataset. The dataset that you’ll be
working with can be found later in the document and yes, it’s been kept very simple by design.
In our view, depending on your speed and how elegantly you want to solve this problem, it could
take you anywhere between 2 - 4 hours to implement this.
NOTE: Whenever we mention <SS> we mean summary statistics which essentially means 3
values (mean, min, max)
For this assignment, we are looking for following functionality to be implemented:
1. An API to add a new record to the dataset.
2. An API to delete a new record to the dataset.
3. An API to fetch SS for salary over the entire dataset. You can ignore the currency (if not
mentioned otherwise) of the salary and simply treat salary as a number.
4. An API to fetch SS for salary for records which satisfy "on_contract": "true". 5. An
API to fetch SS for salary for each department. This means that whatever you’ll do in Step
3, should be done for each department. The return of this API should have 1 SS available
for each unique department.
6. An API to fetch SS for salary for each department and sub-department combination. This
is similar to Case 5 but 1 level of nested aggregation.

## Installation
After you have unzipped the code, you want to create a virtual environment, so you have a clean python installation.
You can do this by running the command
```
python -m venv env
```

After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running
```
pip install -r requirements.txt
```

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.

In our case, we have one single resource, `employee`, so we will use the following URLS - `/employee/create` and `/employee/<name>` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`employee/?type=all` | GET | READ | Get SS for salary over the entire dataset.
`employee/?type=contract` | GET | READ | Get SS for salary where "on_contract": "true".
`employee/?type=department` | GET | READ | Get SS for salary for each department.
`employee/?type=sub_department` | GET | READ | Get SS for salary for each department and sub-department combination.
`employee/create`| POST | CREATE | Create a new employee
`employee/:emp_name` | DELETE | DELETE | Delete an employee by name

## Use
We can test the API using [curl](https://curl.haxx.se/) or [httpie](https://github.com/jakubroztocil/httpie#installation), or we can use [Postman](https://www.postman.com/)

Postman collection is attached in the project's root directory for reference

First, we have to start up Django's development server.
```
python manage.py runserver
```
Only authenticated users can use the API services, for that reason if we try this:
```
http  http://127.0.0.1:8000/api/v1/employee/?type=sub_department
```
we get:
```
{
    "detail": "Authentication credentials were not provided."
}
```

## Create users and Tokens

First we need to create a user, so we can log in
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"ckent@email.com",
"username": "ckent",
"password": "Today@22",
"password2": "Today@22",
"first_name": "Clark",
"last_name": "Kent"
}'
```

After we create an account we can use those credentials to get a token

To get a token first we need to request
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/auth/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
"username": "ckent",
"password": "Today@22"
}'
```
after that, we get the token
```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NTYyODUzNCwiaWF0IjoxNjc1NTQyMTM0LCJqdGkiOiJjMDFkYjgwZTQ4ODM0NTY0OWQxNWI1NjdiZGI1ZjhkYiIsInVzZXJfaWQiOjF9.ZCcsAu70ZW3DhXF9rY-_Dogb9iZCVkjU12Hw32tvuV8",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1NTQyNDM0LCJpYXQiOjE2NzU1NDIxMzQsImp0aSI6IjA3MTk5MmViOWRiNTQyMzNiNzQzNTNlN2ZkODJmN2I5IiwidXNlcl9pZCI6MX0.bTWha0YLfD0qBlVjGt8nv8LaNEYRPxVZjHYe9BpdpYQ"
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.
We can use the refresh token to request a need access token.


The APIs have been made with some assumptions:
- Employee names are unique
- Deletion on an employee can be by passing the name (case insensitive)


### Commands
```
Get SS for salary over the entire dataset
curl --location --request GET 'http://127.0.0.1:8000/api/v1/employee/?type=all' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1NTQyNDM0LCJpYXQiOjE2NzU1NDIxMzQsImp0aSI6IjA3MTk5MmViOWRiNTQyMzNiNzQzNTNlN2ZkODJmN2I5IiwidXNlcl9pZCI6MX0.bTWha0YLfD0qBlVjGt8nv8LaNEYRPxVZjHYe9BpdpYQ' \
--data-raw ''

Get SS for salary where "on_contract": "true"
curl --location --request GET 'http://127.0.0.1:8000/api/v1/employee/?type=contract' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1NTQyNDM0LCJpYXQiOjE2NzU1NDIxMzQsImp0aSI6IjA3MTk5MmViOWRiNTQyMzNiNzQzNTNlN2ZkODJmN2I5IiwidXNlcl9pZCI6MX0.bTWha0YLfD0qBlVjGt8nv8LaNEYRPxVZjHYe9BpdpYQ' \
--data-raw ''

Get SS for salary for each department
curl --location --request GET 'http://127.0.0.1:8000/api/v1/employee/?type=department' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1NTQyNDM0LCJpYXQiOjE2NzU1NDIxMzQsImp0aSI6IjA3MTk5MmViOWRiNTQyMzNiNzQzNTNlN2ZkODJmN2I5IiwidXNlcl9pZCI6MX0.bTWha0YLfD0qBlVjGt8nv8LaNEYRPxVZjHYe9BpdpYQ' \
--data-raw ''

Get SS for salary for each department and sub-department combination
curl --location --request GET 'http://127.0.0.1:8000/api/v1/employee/?type=sub_department' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1NTQyNDM0LCJpYXQiOjE2NzU1NDIxMzQsImp0aSI6IjA3MTk5MmViOWRiNTQyMzNiNzQzNTNlN2ZkODJmN2I5IiwidXNlcl9pZCI6MX0.bTWha0YLfD0qBlVjGt8nv8LaNEYRPxVZjHYe9BpdpYQ' \
--data-raw ''

Create a new employee
curl --location --request POST 'http://127.0.0.1:8000/api/v1/employee/create' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1NTQyNDM0LCJpYXQiOjE2NzU1NDIxMzQsImp0aSI6IjA3MTk5MmViOWRiNTQyMzNiNzQzNTNlN2ZkODJmN2I5IiwidXNlcl9pZCI6MX0.bTWha0YLfD0qBlVjGt8nv8LaNEYRPxVZjHYe9BpdpYQ' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "Vivek",
"salary": "145000",
"currency": "USD",
"department": "Engineering",
"sub_department": "Platform"
}'

Delete an employee by name
curl --location --request DELETE 'http://127.0.0.1:8000/api/v1/employee/ViveK' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1NTQyNDM0LCJpYXQiOjE2NzU1NDIxMzQsImp0aSI6IjA3MTk5MmViOWRiNTQyMzNiNzQzNTNlN2ZkODJmN2I5IiwidXNlcl9pZCI6MX0.bTWha0YLfD0qBlVjGt8nv8LaNEYRPxVZjHYe9BpdpYQ' \
--data-raw ''
```
