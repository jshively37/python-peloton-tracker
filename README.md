# Peloton API Wrapper

**Work In Progress**

This project will interact with the Peloton API to retrieve data using the [unofficial Peloton API](https://app.swaggerhub.com/apis/DovOps/peloton-unofficial-api/0.3.0#/)

Project is focused on graphing data returned from the Peloton API.

Current state: Return all workouts from the Peloton API as a list of dictionaries, and the ability to query a specific workout based on the ID. This logic is handled in `peloton/client.py` which acts as a API wrapper.

## Requirements

```
Python 3.10.4
Requests 2.28.1
```

## Consuming

Create a Python virtual environment and install the dependencies using `pip install -r requirements.txt`

If you are using Pipenv a Pipfile has been included. To install the dependencies use `pipenv install`

Rename `.env.example` to `.env` and populate your variables in this file. The .env is included in the .gitignore to ensure it does not accidently get checked into a git repo.

A main.py file has been included that will return all workouts to validate success.

## License

MIT

See [license.MD](license.MD) for the full text.
