import datetime
import io
import json

import requests
from django.http import HttpResponse

from requests.auth import HTTPBasicAuth
from xlsxwriter import Workbook

from utils import intervals
from utils.intervals import get_all_issue_statuses, delta_time


def _get_auth():
    # change your credentials here user and password for JIRA
    return HTTPBasicAuth("", "")


def _get_issues(user, days, project, without_documentations, status=None):
    auth = _get_auth()

    headers = {
        "Accept": "application/json",
    }

    user_filter = ''
    if user:
        user_filter = f'and assignee = {user}'

    without_documentations_filter = ''
    if without_documentations:
        without_documentations_filter = 'and type != Documentation'

    status_query = f'and status changed during (startofDay(-{days}d) ,endofDay())'
    if status is not None:
        status_query = f' and status = \'{status}\''

    query = {
        'jql': f'project = OSRCH and component = {project} {user_filter} '
               f'{status_query} {without_documentations_filter} ',
        'maxResults': 10000,
        'fields': '*all',
        'expand': 'changelog',
    }

    r = requests.request(
        'GET',
        'https://jit.o3.ru/rest/api/2/search',
        headers=headers,
        auth=auth,
        params=query
    )

    return json.loads(r.text)


def get_issues_pipeline(request):
    selected_user = request.GET.get('user', '')
    days = request.GET.get('days', '14')
    project = request.GET.get('project', 'runtime-base')

    issues = _get_issues(selected_user, days, project)

    result = dict()
    for i in issues['issues']:
        statuses = get_all_issue_statuses(i['changelog']['histories'])
        statuses = set(filter(lambda x: x not in ('To Do', 'Done'), statuses))
        for j in statuses:
            result[j] = result.setdefault(j, 0) + intervals.interval_sums(i['changelog']['histories'], (j,))

    return HttpResponse(json.dumps(result))


def get_issues_estimation(request):
    selected_user = request.GET.get('user', '')
    days = request.GET.get('days', '14')
    project = request.GET.get('project', 'runtime-base')
    without_documentations = request.GET.get('withoutDocumentations', 'false') == 'true'

    issues = _get_issues(selected_user, days, project, without_documentations)

    result = []
    for i in issues['issues']:
        total = intervals.interval_sums(i['changelog']['histories'], ('in progress', 'In Progress', 'In progress', 'В РАБОТЕ',))
        # In Review | Ready For Testing | Release Testing | Testing | Ready To Deploy | Development Done
        review_total = intervals.interval_sums(i['changelog']['histories'], ('In Review',))
        ready_for_testing_total = intervals.interval_sums(i['changelog']['histories'], ('Ready For Testing',))
        testing_total = intervals.interval_sums(i['changelog']['histories'], ('Testing',))
        release_testing_total = intervals.interval_sums(i['changelog']['histories'], ('Release Testing',))
        ready_to_deploy_total = intervals.interval_sums(i['changelog']['histories'], ('Ready To Deploy',))
        development_done_total = intervals.interval_sums(i['changelog']['histories'], ('Development Done',))

        # fixme remove all magic numbers
        estimation = None
        if i['fields']['timeoriginalestimate'] is not None:
            estimation = int(i['fields']['timeoriginalestimate']) / 60 / 60

        if estimation is None and i['fields']['customfield_10002'] is not None:
            estimation = i['fields']['customfield_10002']

        # if estimation is not None:
        #     estimation /= 0.7

        assigned = ''
        if i['fields']['assignee']:
            assigned = i['fields']['assignee']['displayName']

        techcom_status = ''
        if i['fields']['customfield_18200'] and i['fields']['customfield_18200']['value']:
            techcom_status = i['fields']['customfield_18200']['value']

        techcom_est = ''
        if i['fields']['customfield_20505'] and i['fields']['customfield_20505']['value']:
            techcom_est = i['fields']['customfield_20505']['value']

        issue = {
            'issue_key': i['key'],
            'summary': i['fields']['summary'],
            'timespent': total,
            'review_total': review_total,
            'ready_for_testing_total': ready_for_testing_total,
            'testing_total': testing_total,
            'release_testing_total': release_testing_total,
            'ready_to_deploy_total': ready_to_deploy_total,
            'development_done_total': development_done_total,
            'estimation': estimation,
            'status': i['fields']['status']['name'],
            'labels': ", ".join(i['fields']['labels']),
            'epic': i['fields']['customfield_11501'],
            'techcom_status': techcom_status,
            'techcom_est': techcom_est,
            'duedate': i['fields']['duedate'],
            'assigned': assigned,
        }
        result.append(issue)

    return HttpResponse(json.dumps(result))


def get_users(request):
    auth = _get_auth()

    headers = {
        "Accept": "application/json",
    }

    project = request.GET.get('project', 'runtime-base')

    query = {
        'jql': f'project = OSRCH and component = {project} '
               f'and status changed during (startofDay(-100d) ,endofDay())',
        'maxResults': 100,
        'fields': '*all',
        'expand': 'changelog',
    }

    r = requests.request(
        'GET',
        'https://jit.o3.ru/rest/api/2/search',
        headers=headers,
        auth=auth,
        params=query
    )

    m = json.loads(r.text)
    result = {}
    for i in m['issues']:
        if i['fields']['assignee'] is not None:
            # result[i['fields']['assignee']['key']] = i['fields']['assignee']['displayName']
            result[i['fields']['assignee']['name']] = i['fields']['assignee']['displayName']

    return HttpResponse(json.dumps(result))


def get_issue(request):
    auth = _get_auth()

    headers = {
        "Accept": "application/json",
    }

    query = {
        'expand': 'changelog'
    }

    # customfield_10074
    r = requests.get(
        'https://jit.o3.ru/rest/api/2/issue/OSRCH-23417',
        headers=headers,
        auth=auth,
        params=query,
    )

    print(r.text)

    return HttpResponse(r.text)


def report(request):
    output = io.BytesIO()

    selected_user = request.GET.get('user', '')
    days = request.GET.get('days', '600')
    project = request.GET.get('project', 'runtime-base')
    status = request.GET.get('status', None)

    # issues = _get_issues(selected_user, days, project, status)
    issues = _get_issues(selected_user, days, project, None)

    # customfield_10010 - sprint field

    sprints = set()
    for i in issues['issues']:
        if i['fields']['customfield_10010'] is not None:
            sprints.add(i['fields']['customfield_10010'][0]['name'])

    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    line = 2
    total_estimation = 0
    for i in issues['issues']:
        # fixme remove all magic numbers
        estimation = 0
        if i['fields']['timeoriginalestimate'] is not None:
            estimation = int(i['fields']['timeoriginalestimate']) / 60 / 60

        if not estimation and i['fields']['customfield_10074'] is not None:
            estimation = i['fields']['customfield_10074'] * 8

        if estimation:
            estimation /= 0.7

        total_estimation += estimation

        assigned = ''
        if i['fields']['assignee']:
            assigned = i['fields']['assignee']['displayName']

        worksheet.write(f'A{line}', i['key'])
        worksheet.write(f'B{line}', estimation)
        worksheet.write(f'C{line}', i['fields']['status']['name'])
        worksheet.write(f'D{line}', assigned)

        line += 1

    end_time = delta_time(datetime.datetime.now(), total_estimation)
    worksheet.write(f'B{line + 1}', datetime.datetime.strftime(end_time, '%Y-%m-%d'))
    worksheet.write(f'B{line + 2}', f'=sum(B2:B{line})')

    worksheet.autofilter(f'A1:D{line}')

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=test.xlsx"

    output.close()

    return response
