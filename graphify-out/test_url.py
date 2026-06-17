import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, '.')
django.setup()

from django.urls import resolve, reverse

try:
    url = reverse('edital_provisorio:list')
    print(f'URL reverse works: {url}')
except Exception as e:
    print(f'Reverse error: {e}')

try:
    match = resolve('/edital-provisorio/')
    print(f'Resolve works: view_name={match.view_name}')
except Exception as e:
    print(f'Resolve error: {e}')
