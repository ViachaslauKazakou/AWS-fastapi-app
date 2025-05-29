# FastAPI Application

This is a FastAPI application that provides endpoints for managing items and users. 

## Project Structure

```
fastapi-app
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   ├── items.py
│   │   │   └── users.py
│   │   └── dependencies.py
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   └── views
│       ├── __init__.py
│       └── templates
│           ├── index.html
│           └── api_docs.html
├── tests
│   ├── __init__.py
│   ├── test_items.py
│   └── test_users.py
├── pyproject.toml
├── .gitignore
└── README.md
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Running the Application

To run the FastAPI application, use the following command:

```
uvicorn app.main:app --reload
```

## API Endpoints

### Items

- **POST /items/**: Create a new item.
- **GET /items/**: Retrieve a list of items.

### Users

- **POST /users/**: Create a new user.
- **GET /users/**: Retrieve a list of users.

## Testing

To run the tests, use:

```
pytest
```

## License

This project is licensed under the MIT License.