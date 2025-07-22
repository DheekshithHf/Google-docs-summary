from django.contrib import admin
from .models import SlackSummary

@admin.register(SlackSummary)
class SlackSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'doc_url', 'summary', 'created_at')
