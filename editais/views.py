import json

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from base.mixins import (
    ManagerRequiredMixin, ManagerOrExecuteRequiredMixin,
    ViewUserRequiredMixin, GROUP_MANAGER, GROUP_EXECUTE_USER,
)
from .models import EditalProvisorio, AplicacaoEdital, NIVEL_BOLSA_CONFIG
from .forms import EditalProvisorioForm, CronogramaEventoFormSet, DistribuicaoBolsaFormSet


class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = EditalProvisorio.STATUS_CHOICES
        context['nivel_config_json'] = json.dumps(NIVEL_BOLSA_CONFIG)
        return context


class EditalProvisorioListView(LoginRequiredMixin, ContextMixin, ListView):
    model = EditalProvisorio
    template_name = 'editais/edital_list.html'
    context_object_name = 'editais'
    paginate_by = 10

    def get_queryset(self):
        qs = EditalProvisorio.objects.all().select_related('criado_por')
        busca = self.request.GET.get('busca', '')
        status = self.request.GET.get('status', '')
        if busca:
            qs = qs.filter(nome_instituto__icontains=busca)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busca'] = self.request.GET.get('busca', '')
        context['status_atual'] = self.request.GET.get('status', '')
        return context


class EditalProvisorioCreateView(ManagerOrExecuteRequiredMixin, ContextMixin, CreateView):
    model = EditalProvisorio
    template_name = 'editais/edital_form.html'
    form_class = EditalProvisorioForm
    success_url = reverse_lazy('edital_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['cronograma_formset'] = CronogramaEventoFormSet(
                self.request.POST, prefix='cronograma'
            )
            context['distribuicao_formset'] = DistribuicaoBolsaFormSet(
                self.request.POST, prefix='distribuicao'
            )
        else:
            context['cronograma_formset'] = CronogramaEventoFormSet(prefix='cronograma')
            context['distribuicao_formset'] = DistribuicaoBolsaFormSet(prefix='distribuicao')
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        cronograma_formset = context['cronograma_formset']
        distribuicao_formset = context['distribuicao_formset']
        if cronograma_formset.is_valid() and distribuicao_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.criado_por = self.request.user
            self.object.save()
            cronograma_formset.instance = self.object
            cronograma_formset.save()
            distribuicao_formset.instance = self.object
            distribuicao_formset.save()
            messages.success(self.request, 'Edital criado com sucesso!')
            return redirect(self.get_success_url())
        return self.render_to_response(context)


class EditalProvisorioUpdateView(ManagerRequiredMixin, ContextMixin, UpdateView):
    model = EditalProvisorio
    template_name = 'editais/edital_form.html'
    form_class = EditalProvisorioForm
    success_url = reverse_lazy('edital_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['cronograma_formset'] = CronogramaEventoFormSet(
                self.request.POST, instance=self.object, prefix='cronograma'
            )
            context['distribuicao_formset'] = DistribuicaoBolsaFormSet(
                self.request.POST, instance=self.object, prefix='distribuicao'
            )
        else:
            context['cronograma_formset'] = CronogramaEventoFormSet(
                instance=self.object, prefix='cronograma'
            )
            context['distribuicao_formset'] = DistribuicaoBolsaFormSet(
                instance=self.object, prefix='distribuicao'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        cronograma_formset = context['cronograma_formset']
        distribuicao_formset = context['distribuicao_formset']
        if cronograma_formset.is_valid() and distribuicao_formset.is_valid():
            self.object = form.save()
            cronograma_formset.instance = self.object
            cronograma_formset.save()
            distribuicao_formset.instance = self.object
            distribuicao_formset.save()
            messages.success(self.request, 'Edital atualizado com sucesso!')
            return redirect(self.get_success_url())
        return self.render_to_response(context)


class EditalProvisorioDetailView(LoginRequiredMixin, ContextMixin, DetailView):
    model = EditalProvisorio
    template_name = 'editais/edital_detail.html'
    context_object_name = 'edital'

    def get_queryset(self):
        return EditalProvisorio.objects.all().select_related('criado_por')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cronograma'] = self.object.cronograma.all()
        user = self.request.user
        context['tem_cadastro'] = hasattr(user, 'cadastro')
        context['is_view_user'] = user.groups.filter(name=GROUP_VIEW_USER).exists()
        if hasattr(user, 'cadastro'):
            context['ja_aplicou'] = AplicacaoEdital.objects.filter(
                bolsista=user.cadastro, edital=self.object
            ).exists()
        else:
            context['ja_aplicou'] = False
        return context


class EditalProvisorioDeleteView(ManagerRequiredMixin, ContextMixin, DeleteView):
    model = EditalProvisorio
    template_name = 'editais/edital_confirm_delete.html'
    success_url = reverse_lazy('edital_list')

    def form_valid(self, form):
        messages.success(self.request, 'Edital removido com sucesso!')
        return super().form_valid(form)


def edital_pdf_view(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse('Não autorizado', status=401)

    edital = get_object_or_404(
        EditalProvisorio.objects.select_related('criado_por').prefetch_related('distribuicoes', 'cronograma'),
        pk=pk,
    )
    cronograma = edital.cronograma.all()
    html_string = render(request, 'editais/edital_pdf.html', {
        'edital': edital,
        'cronograma': cronograma,
    }).content.decode('utf-8')

    from xhtml2pdf import pisa
    import io

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_string.encode('utf-8')), result)
    if pdf.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    filename = f'edital_{edital.get_nome_instituto_display().replace(" ", "_")}_{edital.pk}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


class AplicarEditalView(ViewUserRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        from decimal import Decimal
        from cadastro.utils import calcular_pontuacao_previa
        from classificacao.models import CriterioClassificacao

        edital = get_object_or_404(EditalProvisorio, pk=kwargs['pk'])

        if edital.status != 'aberto':
            messages.error(request, 'Este edital não está aberto para candidaturas.')
            return redirect('edital_detail', pk=edital.pk)

        if not hasattr(request.user, 'cadastro'):
            messages.warning(request, 'Complete seu cadastro antes de se candidatar.')
            return redirect('cadastro_create')

        bolsista = request.user.cadastro
        if AplicacaoEdital.objects.filter(bolsista=bolsista, edital=edital).exists():
            messages.warning(request, 'Você já se candidatou a este edital.')
        else:
            AplicacaoEdital.objects.create(bolsista=bolsista, edital=edital)

            criterios = CriterioClassificacao.objects.filter(ativo=True)
            _, pontuacao_total = calcular_pontuacao_previa(bolsista, criterios)
            bolsista.pontuacao_previa = Decimal(str(pontuacao_total))
            bolsista.save(update_fields=['pontuacao_previa'])

            messages.success(request, 'Candidatura realizada com sucesso!')
        return redirect('edital_detail', pk=edital.pk)
