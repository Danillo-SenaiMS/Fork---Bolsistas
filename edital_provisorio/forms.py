from django import forms
from django.forms import inlineformset_factory
from .models import EditalProvisorio, CronogramaEvento, NIVEL_BOLSA_CONFIG


class EditalProvisorioForm(forms.ModelForm):
    class Meta:
        model = EditalProvisorio
        fields = [
            'nome_instituto', 'email_solicitante', 'telefone', 'endereco',
            'numero_vagas', 'modalidade_bolsa', 'modalidade_atuacao',
            'plataforma_tecnologica', 'vigencia', 'endereco_atuacao',
            'qualificacao_minima', 'detalhes_qualificacao_minima',
            'experiencia_minima', 'conhecimento_desejavel',
            'conteudo_prova_teorica', 'entrevista', 'criterios_desempate',
            'valor_bolsa', 'valor_minimo', 'valor_maximo',
            'status',
        ]
        widgets = {
            'nome_instituto': forms.Select(attrs={'class': 'form-select'}),
            'email_solicitante': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'solicitante@instituto.br'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(67) 99999-9999'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Rua, número, bairro, cidade - UF'}),
            'numero_vagas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'modalidade_bolsa': forms.Select(attrs={'class': 'form-select'}),
            'modalidade_atuacao': forms.Select(attrs={'class': 'form-select'}),
            'plataforma_tecnologica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Python, Django, React'}),
            'vigencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: De 01/07/2026 a 30/06/2027'}),
            'endereco_atuacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Local onde as atividades serão realizadas'}),
            'qualificacao_minima': forms.Select(attrs={'class': 'form-select'}),
            'detalhes_qualificacao_minima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Ciência da Computação, Engenharia, ...'}),
            'experiencia_minima': forms.Select(attrs={'class': 'form-select'}),
            'conhecimento_desejavel': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'conteudo_prova_teorica': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'entrevista': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'criterios_desempate': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valor_bolsa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'valor_minimo': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True, 'step': '0.01'}),
            'valor_maximo': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True, 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._update_dynamic_fields()

    def _update_dynamic_fields(self):
        nivel = self.initial.get('modalidade_bolsa') or self.data.get('modalidade_bolsa')
        if not nivel or nivel not in NIVEL_BOLSA_CONFIG:
            self.fields['qualificacao_minima'].choices = []
            self.fields['experiencia_minima'].choices = []
            return

        config = NIVEL_BOLSA_CONFIG[nivel]
        self.fields['qualificacao_minima'].choices = config['qualificacao']

        if config['experiencia']:
            self.fields['experiencia_minima'].choices = [('', '--- Selecione ---')] + config['experiencia']
            self.fields['experiencia_minima'].required = True
            self.fields['experiencia_minima'].widget.attrs.pop('readonly', None)
            self.fields['experiencia_minima'].widget.attrs.pop('style', None)
        else:
            self.fields['experiencia_minima'].choices = [('', 'N/A - Sem experiência exigida')]
            self.fields['experiencia_minima'].required = False
            self.fields['experiencia_minima'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        nivel = cleaned_data.get('modalidade_bolsa')
        config = NIVEL_BOLSA_CONFIG.get(nivel)

        if nivel and config:
            experiencia = cleaned_data.get('experiencia_minima')
            if config['experiencia'] and experiencia:
                valores = config['experiencia_valores'].get(experiencia, config)
                cleaned_data['valor_minimo'] = valores[0]
                cleaned_data['valor_maximo'] = valores[1]
            else:
                cleaned_data['valor_minimo'] = config['valor_minimo']
                cleaned_data['valor_maximo'] = config['valor_maximo']

            valor = cleaned_data.get('valor_bolsa')
            if valor is not None:
                vmin = cleaned_data['valor_minimo']
                vmax = cleaned_data['valor_maximo']
                if valor < vmin or valor > vmax:
                    self.add_error('valor_bolsa',
                        f'O valor deve estar entre R$ {vmin} e R$ {vmax} para o nível e experiência selecionados.')

        return cleaned_data


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


CronogramaEventoFormSet = inlineformset_factory(
    EditalProvisorio,
    CronogramaEvento,
    form=CronogramaEventoForm,
    extra=1,
    can_delete=True,
)
