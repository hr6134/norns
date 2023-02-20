from django.urls import path

from urd.views import get_issues_estimation, get_issues_pipeline, get_issue, get_users, report

urlpatterns = [
    path('issues-estimation', get_issues_estimation),
    path('issues-pipeline', get_issues_pipeline),
    path('get-issue', get_issue),
    path('get-users', get_users),
    path('report', report),
]
