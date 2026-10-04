from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_report, name='submit_report'),
    path('signup/', views.signup, name='signup'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('issue/<int:issue_id>/', views.issue_detail, name='issue_detail'),
    path('account/', views.account, name='account'),
    path('officer/', views.officer_dashboard, name='officer_dashboard'),
    path('officer/issue/<int:issue_id>/', views.officer_issue, name='officer_issue'),
]