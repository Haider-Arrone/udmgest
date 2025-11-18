from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'type', 'semester', 'course', 'turma')
    list_filter = ('type', 'semester', 'course')
    search_fields = ('title', 'course', 'turma')
    ordering = ('-date',)
