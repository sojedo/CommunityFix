from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_report, name='submit_report'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('officer/', views.officer_reports, name='officer_reports'),
    path(
    'officer/update/<int:report_id>/',
    views.update_report_status,
    name='update_report_status'
    ),
]