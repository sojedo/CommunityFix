from django.shortcuts import redirect, render
from .forms import ReportForm
from django.contrib.auth.decorators import login_required

@login_required
def submit_report(request):

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
        return redirect('submit_report')

    else:
        form = ReportForm()

    return render(
        request,
        'reports/submit_report.html',
        {'form': form}
    )