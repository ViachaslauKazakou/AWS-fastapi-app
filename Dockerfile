# FROM python:3.10-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY . .

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

FROM 203918879825.dkr.ecr.us-east-1.amazonaws.com/python-3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Copy only pyproject.toml first for better cache
COPY pyproject.toml ./

# Generate poetry.lock and install dependencies (no virtualenv, install into container env)
RUN poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the app
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
