web: gunicorn todolistapi.wsgi
release: python manage.py makemigrations --noinput
release: heroku config:set DISABLE_COLLECTSTATIC=1
release: python manage.py collecstatic --noinput
release: python manage.py migrate --noinput

