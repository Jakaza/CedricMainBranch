@echo off
echo Creating Superuser...
call venv\Scripts\activate
python manage.py createsuperuser
pause
