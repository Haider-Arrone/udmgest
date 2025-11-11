from django import forms
from django.forms import inlineformset_factory
from ..models import Formatura, PontoAgenda
# from dal import autocomplete
from ckeditor.widgets import CKEditorWidget
# ================================
# FORMULARIO FORMATURA
# ================================
class FormaturaForm(forms.ModelForm):
    class Meta:
        model = Formatura
        fields = [
            "titulo",
            "data",
            "local",
            "hora_inicio",
            "hora_fim",
            "descricao",
            "observacoes",
            "publicado",
        ]
        descricao = forms.CharField(widget=CKEditorWidget())
        observacoes = forms.CharField(widget=CKEditorWidget())
        widgets = {
            # "data": forms.DateInput(attrs={
            #     "type": "date",
            #     "class": "form-control"
            # }),
            'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            "hora_inicio": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control"
            }),
            "hora_fim": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control"
            }),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            # "publicado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes de forma dinâmica
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


# ================================
# FORMULARIO PONTO AGENDA
# ================================
class PontoAgendaForm(forms.ModelForm):
    class Meta:
        model = PontoAgenda
        fields = [
            "ordem",
            "departamento",
            "responsavel",
            "titulo",
            "descricao",
            "status",
            "prioridade",
            "data_limite",
            # "percentual",
            # "justificativa",
            # "anexo",
            # "aprovado",
            # "comentario_avaliador"
        ]
        widgets = {
            # 'departamento': autocomplete.ModelSelect2(url='formatura:departamento-autocomplete'),
            # 'responsavel': autocomplete.ModelSelect2(url='formatura:responsavel-autocomplete'),
            # "data_limite": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'data_limite': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "justificativa": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "comentario_avaliador": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "aprovado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


# ================================
# FORMSET PONTOS AGENDA
# ================================
PontoAgendaFormSet = inlineformset_factory(
    Formatura,
    PontoAgenda,
    form=PontoAgendaForm,
    fields=PontoAgendaForm.Meta.fields,
    extra=1,
    can_delete=True
)