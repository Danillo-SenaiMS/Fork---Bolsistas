from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import csv

from base.mixins import ManagerOrExecuteRequiredMixin, GROUP_MANAGER, GROUP_EXECUTE_USER
from cadastro.models import CadastroBolsista, FormacaoAcademica


class PainelBolsistasListView(ManagerOrExecuteRequiredMixin, ListView):
    model = CadastroBolsista
    template_name = 'painel/lista_bolsistas.html'
    context_object_name = 'bolsistas'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('user').prefetch_related('formacoes')
        sort = self.request.GET.get('sort', 'nome')
        if sort == 'pontuacao':
            qs = qs.order_by('-pontuacao_previa')
        elif sort == 'nome':
            qs = qs.order_by('user__nome_completo')
        else:
            qs = qs.order_by('user__nome_completo')
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['sort'] = self.request.GET.get('sort', 'nome')
        return ctx


class PainelBolsistaDetailView(ManagerOrExecuteRequiredMixin, DetailView):
    model = CadastroBolsista
    template_name = 'painel/detalhe_bolsista.html'
    context_object_name = 'bolsista'

    def get_queryset(self):
        return super().get_queryset().select_related('user').prefetch_related('formacoes')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['formacoes'] = self.object.formacoes.order_by('-ano_conclusao')
        return ctx


def painel_download_csv(request):
    if not request.user.is_authenticated:
        return HttpResponse('Nao autorizado', status=401)

    if not (
        request.user.is_superuser
        or request.user.groups.filter(name__in=[GROUP_MANAGER, GROUP_EXECUTE_USER]).exists()
    ):
        return HttpResponse('Nao autorizado', status=401)

    bolsistas = CadastroBolsista.objects.select_related('user').prefetch_related('formacoes').order_by('user__nome_completo')

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="candidatos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'E-mail', 'Telefone', 'Cidade', 'Estado',
                     'Ultima Formacao', 'Area', 'Ano Conclusao',
                     'Projetos (anos)', 'Congressos', 'Resumo Anais',
                     'Artigo Anais', 'Artigo Nacional', 'Artigo Internacional',
                     'Livro/Patente', 'Minicurso', 'Treinamento',
                     'Pontuacao Previa'])

    for b in bolsistas:
        ultima = b.formacoes.order_by('-ano_conclusao').first()
        writer.writerow([
            b.user.nome_completo,
            b.user.email,
            b.telefone or '',
            b.cidade or '',
            b.estado or '',
            ultima.get_tipo_display() if ultima else '',
            ultima.area if ultima else '',
            ultima.ano_conclusao if ultima else '',
            b.participacao_projetos_anos,
            'Sim' if b.participacao_congressos else 'Nao',
            'Sim' if b.resumo_anais else 'Nao',
            'Sim' if b.artigo_completo_anais else 'Nao',
            'Sim' if b.artigo_cientifico_nacional else 'Nao',
            'Sim' if b.artigo_cientifico_internacional else 'Nao',
            'Sim' if b.livro_patente else 'Nao',
            'Sim' if b.participacao_minicurso else 'Nao',
            'Sim' if b.treinamento else 'Nao',
            str(b.pontuacao_previa),
        ])

    return response
