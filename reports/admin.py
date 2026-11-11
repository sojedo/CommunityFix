from django.contrib import admin
from .models import Category, Report, ReportUpdate
from django import forms
from django.contrib.auth import get_user_model

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ReportAdminForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        User = get_user_model()

        self.fields['assigned_officer'].queryset = User.objects.filter(
            role='officer'
        )
        if self.instance.status == 'submitted':
            self.fields['status'].choices = [
                ('submitted', 'Submitted'),
                ('under_review', 'Under Review'),
            ]
        
        elif self.instance.status == 'under_review':
            self.fields['status'].choices = [
                ('under_review', 'Under Review'),
                ('assigned', 'Assigned'),
                ('rejected', 'Rejected'),
            ]
        elif self.instance.status == 'assigned':
            self.fields['status'].choices = [
                ('assigned', 'Assigned'),
                ('in_progress', 'In Progress'),
            ]
        elif self.instance.status == 'in_progress':
            self.fields['status'].choices = [
                ('in_progress', 'In Progress'),
                ('pending_verification', 'Pending_verification'),
            ]
        elif self.instance.status == 'pending_verification':
            self.fields['status'].choices = [
                ('pending_verification', 'Pending Verification'),
                ('resolved', 'Resolved'),
            ]

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        assigned_officer = cleaned_data.get('assigned_officer')

        if status == 'assigned' and assigned_officer is None:
            raise forms.ValidationError(
                'A Field Officer must be assigned before the report can be marked as Assigned.'
            )

        if status == 'rejected' and not cleaned_data.get('rejection_reason'):
            raise forms.ValidationError(
                'You must provide a reason for rejecting this report.'
            )
        return cleaned_data

    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_report = Report.objects.get(pk=obj.pk)
            old_status = old_report.status

        super().save_model(request, obj, form, change)

        if old_status != obj.status:
            ReportUpdate.objects.create(
                report=obj,
                status=obj.status,
                changed_by=request.user
            )

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    form = ReportAdminForm

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