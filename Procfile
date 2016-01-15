web: gunicorn movietix.wsgi --log-file -
worker: celery -A movietix worker -l info -B