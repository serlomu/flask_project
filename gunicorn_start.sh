#!/bin/bash
source venv/bin/activate
exec gunicorn -w 3 -b :8000 app1:app

