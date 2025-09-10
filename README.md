# Stacc Homework

## Setup

- Clone the repo.
- Make a new python virtual environment and activate it.
- Install required dependencies.
```
pip install -r requirements.txt
```
- Build the container images.
```
docker build -t webapi . && docker build -t db ./db
```
## Running

To run the project, just invoke docker compose up.
```
docker compose up -d
```

## Tests

Tests can be run using pytest. The containers must be up to run the tests.
```
pytest
```

## Potential improvements

I would've liked to set up a CI pipeline but I'm not familiar with it enough to have attempted it for this project. I would look into using testcontainers library for doing that.

I'm not satisfied with how the database gets initialised. Currently the base dataset gets added to the database every time when containers are started. It would be better to just insert the dataset upon the creation of the table. Maybe it would be better to create the dataset outside of the container images, but that depends on the project's requirements.

Using the same database connection for cursors causes all commands to be executed serially. For an api, it might be better to be able to execute the commands concurrently.

Use query parameters instead of string concatenation or string interpolation.
