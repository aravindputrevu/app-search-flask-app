FROM python:3.8-slim-buster

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app


RUN useradd appuser && chown -R appuser /app
USER appuser


CMD ["gunicorn","--workers", "2", "--bind", "0.0.0.0:5000", "main:app", "--log-level", "info", "--error-logfile", "app.log", "--capture-output"]
