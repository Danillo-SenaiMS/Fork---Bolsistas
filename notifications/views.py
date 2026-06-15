from django.views.generic import ListView, TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string

from base.mixins import TenantRequiredMixin
from .models import Notificacao


class NotificacaoListView(TenantRequiredMixin, ListView):
    model = Notificacao
    template_name = 'notifications/notificacao_list.html'
    context_object_name = 'notificacoes'
    paginate_by = 20

    def get_queryset(self):
        return Notificacao.objects.filter(
            destinatario=self.request.user,
            tenant=self.request.tenant,
        )


class MarcarLidaView(TenantRequiredMixin, TemplateView):
    def post(self, request, pk):
        notificacao = get_object_or_404(
            Notificacao, pk=pk, destinatario=request.user, tenant=request.tenant
        )
        notificacao.lido = True
        notificacao.save(update_fields=['lido'])
        if request.headers.get('HX-Request'):
            html = render_to_string(
                'notifications/partials/notificacao_item.html',
                {'n': notificacao},
                request=request,
            )
            return HttpResponse(html)
        return redirect('notificacao_list')


class MarcarTodasLidasView(TenantRequiredMixin, View):
    def post(self, request):
        Notificacao.objects.filter(
            destinatario=request.user, tenant=request.tenant, lido=False
        ).update(lido=True)
        return redirect('notificacao_list')
