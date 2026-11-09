from django.contrib import admin
from .models import Category, Report


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'reporter',
        'assigned_officer',
        'status',
        'date_reported',
    )

    list_filter = ('status', 'category')

    search_fields = ('title', 'description', 'location')