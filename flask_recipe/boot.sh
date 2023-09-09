#!/bin/bash
source venv/bin/activate
exec gunicorn -b :5000 --timeout 600 --access-logfile - --error-logfile - chatbot_flask:app