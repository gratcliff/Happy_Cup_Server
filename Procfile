web: python manage.py runserver
web: gunicorn Happy_Cup.wsgi --log-file -
heroku ps:scale web=1