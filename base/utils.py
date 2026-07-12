import secrets
from datetime import date, timedelta


def gerar_numero_serie(model, campo='numero_serie', tamanho=4):
    max_val = 10 ** tamanho - 1
    for _ in range(100):
        n = secrets.randbelow(max_val + 1)
        codigo = f'{n:0{tamanho}d}'
        if not model.objects.filter(**{campo: codigo}).exists():
            return codigo
    for i in range(max_val + 1):
        codigo = f'{i:0{tamanho}d}'
        if not model.objects.filter(**{campo: codigo}).exists():
            return codigo
    raise ValueError(
        f'Nao foi possivel gerar numero de serie unico de {tamanho} digitos para {model.__name__}'
    )


def dias_uteis_entre(inicio, fim, feriados=None):
    if inicio > fim:
        return 0
    if feriados is None:
        from django.conf import settings
        feriados = getattr(settings, 'FERIADOS_NACIONAIS', [])
    feriados_set = set()
    for f_str in feriados:
        try:
            partes = f_str.split('-')
            feriados_set.add(date(int(partes[0]), int(partes[1]), int(partes[2])))
        except (ValueError, IndexError):
            pass
    dias = 0
    atual = inicio
    while atual <= fim:
        if atual.weekday() < 5 and atual not in feriados_set:
            dias += 1
        atual += timedelta(days=1)
    return dias
