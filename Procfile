web: gunicorn samms.wsgi --log-file -

web: python manage.py collectstatic --noinput; gunicorn --workers=4 --bind=0.0.0.0:$PORT samms.settings