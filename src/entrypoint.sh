#!/bin/sh

if [ "$ENV" = "dev" ]
then
  exec uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
else
  exec gunicorn backend.main:app
fi