from django.shortcuts import redirect, render
from .forms import ReportForm
from .models import Report, ReportUpdate
from django.contrib.auth.decorators import login_required

@login_required
def submit_report(request):

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            
            print("CREATING REPORT HISTORY")

            ReportUpdate.objects.create(
                report=report,
                status=report.status,
                changed_by=request.user
            )
            return redirect('submit_report')

    else:
        form = ReportForm()

    return render(
        request,
        'reports/submit_report.html',
        {'form': form}
    )

@login_required
def my_reports(request):
    reports = request.user.reports.all()
    
    return render(
    request,
    'reports/my_reports.html',
    {'reports': reports}
)

@login_required
def officer_reports(request):
    reports = Report.objects.filter(
        assigned_officer=request.user,
        status__in=['assigned', 'in_progress']
    )
    return render(
        request,
        'reports/officer_reports.html',
        {'reports': reports}
    )

@login_required
def update_report_status(request, report_id):
    report = Report.objects.get(
        id=report_id,
        assigned_officer=request.user
    )

    if report.status == 'assigned':
        report.status = 'in_progress'
        report.save()
        
        ReportUpdate.objects.create(
        report=report,
        status=report.status,
        changed_by=request.user
    )

    elif report.status == 'in_progress':
        report.status = 'pending_verification'
        report.save()
        
        ReportUpdate.objects.create(
        report=report,
        status=report.status,
        changed_by=request.user
    )

    return redirect('officer_reports')