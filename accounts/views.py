from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import Group
from django import forms

from base.mixins import (
    ManagerRequiredMixin, GROUP_MANAGER,
    GROUP_VIEW_USER, GROUP_EXECUTE_USER,
)

from .models import User, Perfil
from editais.models import EditalProvisorio, AplicacaoEdital
from cadastro.models import SolicitacaoEdicao


class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Crie uma senha'})
    )
    password2 = forms.CharField(
        label='Confirme a Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'})
    )

    class Meta:
        model = User
        fields = ['nome_completo', 'email']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('As senhas não conferem.')
        return p2


class LandingPageView(TemplateView):
    template_name = 'accounts/landing.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class RegistroView(FormView):
    template_name = 'accounts/registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('landing')

    def form_valid(self, form):
        user = User.objects.create_user(
            email=form.cleaned_data['email'],
            nome_completo=form.cleaned_data['nome_completo'],
            password=form.cleaned_data['password1'],
        )
        Perfil.objects.create(user=user)
        view_group, _ = Group.objects.get_or_create(name=GROUP_VIEW_USER)
        user.groups.add(view_group)
        messages.success(self.request, 'Conta criada com sucesso! Faça login.')
        return super().form_valid(form)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_superuser'] = user.is_superuser
        context['is_manager'] = user.groups.filter(name=GROUP_MANAGER).exists()
        context['is_view_user'] = user.groups.filter(name=GROUP_VIEW_USER).exists()
        context['is_execute_user'] = user.groups.filter(name=GROUP_EXECUTE_USER).exists()
        context['has_cadastro'] = hasattr(user, 'cadastro')

        if user.is_superuser or context['is_manager']:
            context['total_usuarios'] = User.objects.filter(is_active=True).count()
            context['total_pendentes'] = User.objects.filter(is_active=False).count()
            context['total_editais'] = EditalProvisorio.objects.count()
            context['total_editais_abertos'] = EditalProvisorio.objects.filter(status='aberto').count()
            context['total_aplicacoes'] = AplicacaoEdital.objects.count()
            context['total_pendentes_solicitacao'] = SolicitacaoEdicao.objects.filter(status='pendente').count()

        elif context['is_view_user']:
            context['total_editais_abertos'] = EditalProvisorio.objects.filter(status='aberto').count()
            if hasattr(user, 'cadastro'):
                context['total_aplicacoes'] = AplicacaoEdital.objects.filter(
                    bolsista=user.cadastro
                ).count()
            else:
                context['total_aplicacoes'] = 0

        return context


class AprovarUsuarioView(ManagerRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(
            User, pk=kwargs['pk']
        )
        user.is_active = True
        user.save()

        view_group, _ = Group.objects.get_or_create(name=GROUP_VIEW_USER)
        user.groups.add(view_group)

        messages.success(request, f'Usuário {user.nome_completo} aprovado.')
        if request.headers.get('HX-Request'):
            html = render_to_string(
                'accounts/partials/usuario_row.html',
                {'u': user},
                request=request,
            )
            return HttpResponse(html)
        return redirect('home')
