# Task 2

Requires a running MongoDB instance. Can be started with:

```
docker compose up
```

## 1. Backend

Handles parsing CSV data and data with Fast API. Has the following entrypoints:

-   `data_parser.py` - Parse CSV data from `/data` and populates MongoDB
-   `main.py` - Entry point for serving Fast API

### Install dependencies:

```
cd backend
poetry install
```

### Run data parser:

```
cd src
poetry run python data_fetcher.py
```

The script will parse the CSV data and populate db named `task2`

## 2. Frontend

Fetches data from backend and displays it in a graph

### Install dependencies:

```
cd frontend
pnpm install
```

### Run frontend

```
pnpm run dev
```

The frontend will be served locally on: http://localhost:5173/
