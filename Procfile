web: gunicorn todolistapi.wsgi
DISABLE_COLLECTSTATIC=1
release: python manage.py makemigrations --noinput
#release: python manage.py collecstatic --noinput
release: python manage.py migrate --noinput

