gunicorn app:app \
  -b $APP_URL \
  --workers=1 \
  --access-logfile access.txt \
  --error-logfile error.txt \
  -D