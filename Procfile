release: python manage.py makemigrations
release: python manage.py migrate --noinput
release: python manage.py loaddata data.json
web: gunicorn blog.wsgi
