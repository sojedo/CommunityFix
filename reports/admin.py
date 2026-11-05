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
        'status',
        'date_reported',
    )