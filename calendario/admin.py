from django.contrib import admin

# Register your models here.
from django import forms
from .models import Event
class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "color": forms.TextInput(attrs={"type": "color"}),
        }


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm

    list_display = ('title', 'type', 'start_date', 'end_date', 'semester', 'course', 'turma', 'color')
    list_filter = ('type', 'semester', 'course', 'turma')
    search_fields = ('title', 'course', 'turma')
    ordering = ('start_date',)
    date_hierarchy = 'start_date'

    fieldsets = (
        ('Informações do Evento', {
            'fields': ('title', 'type', 'color')  # ✔ color aqui
        }),
        ('Datas', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',)
        }),
        ('Classificação', {
            'fields': ('semester', 'course', 'turma'),
            'classes': ('collapse',)
        }),
    )