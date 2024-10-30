# Pull base image
FROM python:3.12-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy
# Copy project
WORKDIR /ChatBotSA/
COPY . /ChatBotSA/

