import json

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse

from base.mixins import TenantRequiredMixin, ManagerRequiredMixin
from .models import EditalProvisorio, NIVEL_BOLSA_CONFIG
from .forms import EditalProvisorioForm, CronogramaEventoFormSet, DistribuicaoBolsaFormSet
from accounts.models import Tenant


class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = EditalProvisorio.STATUS_CHOICES
        context['nivel_config_json'] = json.dumps(NIVEL_BOLSA_CONFIG)
        return context


class EditalProvisorioListView(TenantRequiredMixin, ContextMixin, ListView):
    model = EditalProvisorio
    template_name = 'edital_provisorio/edital_list.html'
    context_object_name = 'editais'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = EditalProvisorio.objects.all().select_related('criado_por')
        else:
            qs = EditalProvisorio.objects.filter(tenant=self.request.tenant).select_related('criado_por')
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


class EditalProvisorioCreateView(ManagerRequiredMixin, ContextMixin, CreateView):
    model = EditalProvisorio
    template_name = 'edital_provisorio/edital_form.html'
    form_class = EditalProvisorioForm
    success_url = reverse_lazy('edital_provisorio:list')

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
            self.object.tenant = self.request.tenant or Tenant.objects.filter(ativo=True).first()
            self.object.save()
            cronograma_formset.instance = self.object
            cronograma_formset.save()
            distribuicao_formset.instance = self.object
            distribuicao_formset.save()
            messages.success(self.request, 'Edital provisório criado com sucesso!')
            return redirect(self.get_success_url())
        import logging
        logger = logging.getLogger(__name__)
        logger.error('Formset errors - cronograma: %s, distribuicao: %s',
                     cronograma_formset.errors, distribuicao_formset.errors)
        return self.render_to_response(context)


class EditalProvisorioUpdateView(ManagerRequiredMixin, ContextMixin, UpdateView):
    model = EditalProvisorio
    template_name = 'edital_provisorio/edital_form.html'
    form_class = EditalProvisorioForm

    def get_queryset(self):
        if self.request.user.is_superuser:
            return EditalProvisorio.objects.all()
        return EditalProvisorio.objects.filter(tenant=self.request.tenant)

    success_url = reverse_lazy('edital_provisorio:list')

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
            messages.success(self.request, 'Edital provisório atualizado com sucesso!')
            return redirect(self.get_success_url())
        import logging
        logger = logging.getLogger(__name__)
        logger.error('Formset errors - cronograma: %s, distribuicao: %s',
                     cronograma_formset.errors, distribuicao_formset.errors)
        return self.render_to_response(context)


class EditalProvisorioDetailView(TenantRequiredMixin, ContextMixin, DetailView):
    model = EditalProvisorio
    template_name = 'edital_provisorio/edital_detail.html'
    context_object_name = 'edital'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return EditalProvisorio.objects.all().select_related('criado_por')
        return EditalProvisorio.objects.filter(tenant=self.request.tenant).select_related('criado_por')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cronograma'] = self.object.cronograma.all()
        return context


class EditalProvisorioDeleteView(ManagerRequiredMixin, ContextMixin, DeleteView):
    model = EditalProvisorio
    template_name = 'edital_provisorio/edital_confirm_delete.html'
    success_url = reverse_lazy('edital_provisorio:list')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return EditalProvisorio.objects.all()
        return EditalProvisorio.objects.filter(tenant=self.request.tenant)

    def form_valid(self, form):
        messages.success(self.request, 'Edital provisório removido com sucesso!')
        return super().form_valid(form)


def edital_pdf_view(request, pk):
    if request.user.is_superuser:
        edital = EditalProvisorio.objects.select_related('criado_por').prefetch_related('distribuicoes', 'cronograma').get(pk=pk)
    else:
        edital = EditalProvisorio.objects.filter(tenant=request.tenant).select_related('criado_por').prefetch_related('distribuicoes', 'cronograma').get(pk=pk)
    cronograma = edital.cronograma.all()
    html_string = render(request, 'edital_provisorio/edital_pdf.html', {
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
