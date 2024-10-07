## Task 1:

Requires a running MongoDB instance. Can be started with:

```
docker compose up
```

Consists of two parts with the following entrypoints:

1. `data_fetcher.py` - Fetches data and populates MongoDB
2. `main.py` - Entry point for serving Fast API

### Install dependencies:

```
poetry install
```

### Run data fetcher

Data fetcher can be run from `src` folder using:

```
poetry run python data_fetcher.py
```

This script will fetch data from https://jsonplaceholder.typicode.com endpoints `/posts` and `/comments` and store it in respective collection `posts` and `comments` in a db named `task1`

### Serving Fast API

From `src` folder run:

```
poetry run python main.py
```

The api is documented and can be tested locally on: http://127.0.0.1:8000/docs
