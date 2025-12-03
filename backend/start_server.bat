@echo off
echo Starting Django Server...
call venv\Scripts\activate
python manage.py runserver
pause
