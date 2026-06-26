from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import EditalProvisorio, CronogramaEvento, DistribuicaoBolsa, NIVEL_BOLSA_CONFIG


class DistribuicaoBolsaForm(forms.ModelForm):
    class Meta:
        model = DistribuicaoBolsa
        fields = ['experiencia', 'quantidade', 'valor_unitario']
        widgets = {
            'experiencia': forms.Select(attrs={'class': 'form-select form-select-sm distrib-experiencia'}),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm distrib-quantidade',
                'min': 0, 'step': 1,
            }),
            'valor_unitario': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm distrib-valor',
                'step': '0.01', 'min': '0',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'edital' in kwargs.get('initial', {}):
            self._set_experiencia_choices(kwargs['initial']['edital'])

    def _set_experiencia_choices(self, edital):
        config = NIVEL_BOLSA_CONFIG.get(getattr(edital, 'modalidade_bolsa', ''), {})
        choices = config.get('experiencia', [])
        if choices:
            self.fields['experiencia'].choices = [('', '--- Selecione ---')] + choices
        else:
            self.fields['experiencia'].choices = [('', 'N/A')]
        self.fields['experiencia'].required = False

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data or cleaned_data.get('DELETE'):
            return cleaned_data
        experiencia = cleaned_data.get('experiencia')
        quantidade = cleaned_data.get('quantidade') or 0
        valor_unitario = cleaned_data.get('valor_unitario') or 0

        if not experiencia and (quantidade or valor_unitario):
            raise forms.ValidationError('Selecione a experiência quando quantidade ou valor unitário estiver preenchido.')

        modalidade = self.data.get('modalidade_bolsa')
        if not modalidade:
            try:
                if self.instance.edital_id:
                    modalidade = self.instance.edital.modalidade_bolsa
            except Exception:
                pass

        if experiencia and valor_unitario and modalidade:
            config = NIVEL_BOLSA_CONFIG.get(modalidade)
            if config:
                valores = config.get('experiencia_valores', {}).get(experiencia)
                if valores:
                    min_v, max_v = valores
                    if valor_unitario < min_v or valor_unitario > max_v:
                        raise forms.ValidationError(
                            f'O valor unitário para "{experiencia}" deve estar entre '
                            f'R$ {min_v:.2f} e R$ {max_v:.2f}.'
                        )
                elif config.get('valor_minimo') is not None:
                    min_v, max_v = config['valor_minimo'], config['valor_maximo']
                    if valor_unitario < min_v or valor_unitario > max_v:
                        raise forms.ValidationError(
                            f'O valor unitário deve estar entre '
                            f'R$ {min_v:.2f} e R$ {max_v:.2f}.'
                        )
        return cleaned_data


class BaseDistribuicaoFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        if commit:
            obj.save()
        return obj

    def clean(self):
        if any(self.errors):
            return
        total = sum(
            (form.cleaned_data.get('quantidade', 0) or 0) *
            (form.cleaned_data.get('valor_unitario', 0) or 0)
            for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
        )
        edital_total = self.instance.valor_total_bolsa if self.instance.pk else 0
        if self.data.get('valor_total_bolsa'):
            try:
                edital_total = float(self.data['valor_total_bolsa'])
            except (ValueError, TypeError):
                pass
        if total > edital_total:
            raise forms.ValidationError(
                f'A soma da distribuição (R$ {total:.2f}) excede o valor total da bolsa (R$ {edital_total:.2f}).'
            )


class EditalProvisorioForm(forms.ModelForm):
    vigencia_meses = forms.IntegerField(
        label='Vigência (meses)',
        min_value=1,
        max_value=36,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 36,
            'placeholder': 'Ex: 12',
        }),
    )

    class Meta:
        model = EditalProvisorio
        fields = [
            'nome_edital', 'area_estudo', 'detalhes_edital',
            'nome_instituto', 'email_solicitante',
            'documento_anexo',
            'numero_vagas', 'valor_total_bolsa',
            'modalidade_bolsa', 'modalidade_atuacao',
            'plataforma_tecnologica', 'vigencia', 'endereco_atuacao',
            'qualificacao_minima', 'detalhes_qualificacao_minima',
            'conhecimento_desejavel',
            'conteudo_prova_teorica', 'entrevista', 'criterios_desempate',
            'valor_minimo', 'valor_maximo',
            'status',
        ]
        widgets = {
            'nome_edital': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Edital de Inovação Tecnológica 2026'}),
            'area_estudo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Ciência da Computação, Biotecnologia'}),
            'detalhes_edital': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalhes adicionais sobre o edital (opcional)'}),
            'nome_instituto': forms.Select(attrs={'class': 'form-select'}),
            'email_solicitante': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'solicitante@instituto.br', 'readonly': True}),
            'documento_anexo': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'numero_vagas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'readonly': True}),
            'valor_total_bolsa': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0',
                'placeholder': 'Ex: 50000.00',
            }),
            'modalidade_bolsa': forms.Select(attrs={'class': 'form-select'}),
            'modalidade_atuacao': forms.Select(attrs={'class': 'form-select'}),
            'plataforma_tecnologica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Python, Django, React'}),
            'vigencia': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 15, 'max': 1095,
                'placeholder': 'Ex: 180',
            }),
            'endereco_atuacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Local onde as atividades serão realizadas'}),
            'qualificacao_minima': forms.Select(attrs={'class': 'form-select'}),
            'detalhes_qualificacao_minima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Ciência da Computação, Engenharia, ...'}),
            'conhecimento_desejavel': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'conteudo_prova_teorica': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'entrevista': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'criterios_desempate': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valor_minimo': forms.HiddenInput(),
            'valor_maximo': forms.HiddenInput(),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['valor_minimo'].required = False
        self.fields['valor_maximo'].required = False
        self.fields['documento_anexo'].required = False
        self.fields['status'].required = False
        self.fields['vigencia'].required = False
        self.fields['vigencia'].widget = forms.HiddenInput()

        if self._user:
            if not self.is_bound and not self.initial.get('email_solicitante'):
                self.initial['email_solicitante'] = self._user.email

        if not (self._user and self._user.is_superuser):
            self.fields['status'].disabled = True
            if not self.is_bound and not self.initial.get('status'):
                self.initial['status'] = 'em_analise'

        if not self.is_bound and self.instance and self.instance.pk and self.instance.vigencia:
            self.initial['vigencia_meses'] = max(1, self.instance.vigencia // 30)
        elif not self.is_bound and not self.initial.get('vigencia_meses'):
            self.initial['vigencia_meses'] = 6

        self._update_dynamic_fields()

    def _update_dynamic_fields(self):
        nivel = self.initial.get('modalidade_bolsa') or self.data.get('modalidade_bolsa')
        if not nivel or nivel not in NIVEL_BOLSA_CONFIG:
            self.fields['qualificacao_minima'].choices = [('', '--- Selecione a modalidade primeiro ---')]
            return

        config = NIVEL_BOLSA_CONFIG[nivel]
        self.fields['qualificacao_minima'].choices = [('', '--- Selecione ---')] + config['qualificacao']

    def clean(self):
        cleaned_data = super().clean()
        nivel = cleaned_data.get('modalidade_bolsa')
        config = NIVEL_BOLSA_CONFIG.get(nivel)

        if nivel and config:
            cleaned_data['valor_minimo'] = config.get('valor_minimo', 0)
            cleaned_data['valor_maximo'] = config.get('valor_maximo', 0)

        modalidade_atuacao = cleaned_data.get('modalidade_atuacao')
        endereco_atuacao = cleaned_data.get('endereco_atuacao')
        if modalidade_atuacao == 'remota' and not endereco_atuacao:
            self.add_error('endereco_atuacao', 'Endereço de atuação é obrigatório para modalidade remota.')

        vigencia_meses = cleaned_data.get('vigencia_meses')
        if vigencia_meses is not None:
            cleaned_data['vigencia'] = vigencia_meses * 30
        else:
            cleaned_data['vigencia'] = 180

        vigencia = cleaned_data.get('vigencia')
        if vigencia is not None:
            if vigencia < 15:
                self.add_error('vigencia_meses', 'A vigência mínima é de 15 dias.')
            elif vigencia > 1095:
                self.add_error('vigencia_meses', 'A vigência máxima é de 36 meses (1095 dias).')

        if not (self._user and self._user.is_superuser):
            if cleaned_data.get('status') and cleaned_data['status'] != 'em_analise':
                self.add_error('status', 'Apenas superusuários podem alterar o status. O status será mantido como "Em Análise".')
                cleaned_data['status'] = 'em_analise'
            else:
                cleaned_data['status'] = 'em_analise'

        return cleaned_data


DistribuicaoBolsaFormSet = inlineformset_factory(
    EditalProvisorio,
    DistribuicaoBolsa,
    form=DistribuicaoBolsaForm,
    formset=BaseDistribuicaoFormSet,
    extra=1,
    can_delete=True,
)


class BaseCronogramaFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        if commit:
            obj.save()
        return obj


class CronogramaEventoForm(forms.ModelForm):
    class Meta:
        model = CronogramaEvento
        fields = ['evento', 'data_referencia', 'observacao', 'ordem']
        widgets = {
            'evento': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'data_referencia': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ex: A partir da data de publicação deste edital',
            }),
            'observacao': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Observação (opcional)',
            }),
            'ordem': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evento'].required = False
        self.fields['data_referencia'].required = False
        self.fields['ordem'].required = False

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data or cleaned_data.get('DELETE'):
            return cleaned_data
        evento = cleaned_data.get('evento')
        data = cleaned_data.get('data_referencia')
        if not evento and data:
            raise forms.ValidationError('Selecione o evento quando a data de referência estiver preenchida.')
        if evento and not data:
            raise forms.ValidationError('Informe a data de referência para o evento selecionado.')
        return cleaned_data


CronogramaEventoFormSet = inlineformset_factory(
    EditalProvisorio,
    CronogramaEvento,
    form=CronogramaEventoForm,
    formset=BaseCronogramaFormSet,
    extra=1,
    can_delete=True,
)
