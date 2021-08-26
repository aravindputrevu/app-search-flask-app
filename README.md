# app-search-flask-app
 This is a example of Elastic App Search with App Search Python Client

# Running App

> gunicorn --workers 2 --bind 0.0.0.0:5000 main:app --log-level info --error-logfile app.log --capture-output