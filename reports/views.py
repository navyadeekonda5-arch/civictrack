from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReportForm, SignUpForm, UpdateForm
from .models import Report, Issue, IssueUpdate
from .utils import find_or_create_issue

DONE = ['resolved', 'closed']


def is_officer(user):
    return hasattr(user, 'officerprofile')


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('my_reports')
    return render(request, 'registration/signup.html', {'form': form})


# ---------- Citizen ----------

@login_required
def submit_report(request):
    if is_officer(request.user):
        return redirect('officer_dashboard')
    form = ReportForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        issue, joined = find_or_create_issue(
            data['category'], data['latitude'], data['longitude'])
        Report.objects.create(
            issue=issue, citizen=request.user, photo=data['photo'],
            description=data['description'],
            latitude=data['latitude'], longitude=data['longitude'])
        if joined:
            messages.info(request, f"This problem was already reported by others. "
                                   f"Your report was added. Total reports: {issue.report_count}.")
        else:
            messages.success(request, "Your report has been submitted. Thank you!")
        return redirect('my_reports')
    return render(request, 'reports/submit.html', {'form': form})


@login_required
def my_reports(request):
    if is_officer(request.user):
        return redirect('officer_dashboard')
    reports = (Report.objects.filter(citizen=request.user)
               .select_related('issue', 'issue__category')
               .order_by('-created_at'))
    return render(request, 'reports/my_reports.html', {'reports': reports})


@login_required
def issue_detail(request, issue_id):
    if is_officer(request.user):
        return redirect('officer_dashboard')
    mine = Issue.objects.filter(reports__citizen=request.user).distinct()
    issue = get_object_or_404(mine, id=issue_id)
    return render(request, 'reports/issue_detail.html', {
        'issue': issue, 'updates': issue.updates.order_by('updated_at')})


# ---------- Officer ----------

@login_required
def officer_dashboard(request):
    if not is_officer(request.user):
        return redirect('my_reports')
    dept = request.user.officerprofile.department
    issues = (Issue.objects.filter(category__department=dept)
              .select_related('category').order_by('-priority_score'))
    open_issues = issues.exclude(status__in=DONE)
    return render(request, 'reports/officer_dashboard.html', {
        'dept': dept,
        'issues': open_issues,
        'count_open': open_issues.count(),
        'count_done': issues.filter(status__in=DONE).count(),
    })


@login_required
def officer_issue(request, issue_id):
    if not is_officer(request.user):
        return redirect('my_reports')
    dept = request.user.officerprofile.department
    issue = get_object_or_404(Issue, id=issue_id, category__department=dept)

    form = UpdateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        if data['status'] == 'resolved' and not data['proof_photo']:
            messages.error(request, "Upload an 'after' photo as proof to mark it resolved.")
        else:
            IssueUpdate.objects.create(
                issue=issue, status=data['status'], note=data['note'],
                proof_photo=data['proof_photo'], updated_by=request.user)
            issue.status = data['status']
            issue.save()
            messages.success(request, "Status updated.")
            return redirect('officer_dashboard')

    return render(request, 'reports/officer_issue.html', {
        'issue': issue, 'form': form, 'reports': issue.reports.all(),
        'updates': issue.updates.order_by('updated_at')})


# ---------- Account (both roles) ----------

@login_required
def account(request):
    if is_officer(request.user):
        dept = request.user.officerprofile.department
        issues = Issue.objects.filter(category__department=dept)
        stats = {'total': issues.count(),
                 'active': issues.exclude(status__in=DONE).count(),
                 'resolved': issues.filter(status__in=DONE).count()}
        return render(request, 'reports/account.html', {'stats': stats, 'officer': True})

    mine = (Report.objects.filter(citizen=request.user)
            .select_related('issue', 'issue__category').order_by('-created_at'))
    stats = {'total': mine.count(),
             'active': mine.exclude(issue__status__in=DONE).count(),
             'resolved': mine.filter(issue__status__in=DONE).count()}
    return render(request, 'reports/account.html', {'reports': mine[:5], 'stats': stats})