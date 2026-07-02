#!/bin/sh
set -e

echo "Aguardando banco de dados..."
python - <<PY
import socket, sys, os, time
host = os.environ.get('DB_HOST', '')
port = int(os.environ.get('DB_PORT', '5432'))
if not host or host == 'localhost' or host == '127.0.0.1':
    sys.exit(0)
for _ in range(30):
    try:
        with socket.create_connection((host, port), timeout=1):
            sys.exit(0)
    except OSError:
        time.sleep(1)
print('Banco de dados nao respondeu a tempo.')
sys.exit(1)
PY

echo "Aplicando migracoes..."
python manage.py migrate --noinput

echo "Coletando arquivos estaticos..."
python manage.py collectstatic --noinput --clear

exec "$@"
