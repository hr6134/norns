from datetime import datetime, timedelta, timezone
from dateutil.parser import parse


def _indexes(collection, predicate):
    result = []
    n = 0

    for i in collection:
        if predicate(i):
            result.append(n)
        n += 1

    return result


def delta_time(since, add):
    days = add // 8

    while days > 0:
        since += timedelta(days=1)
        if since.weekday() not in (5, 6):
            days -= 1

    return since


def _delta_time(since, till):
    current_day = datetime.fromisoformat(since[:-5])
    until = datetime.fromisoformat(till[:-5])

    if current_day.day == until.day:
        return (until.timestamp() - current_day.timestamp()) / 60 / 60

    end_of_day = datetime(current_day.year, current_day.month, current_day.day, 18, 0, 0)
    total = (end_of_day.timestamp() - current_day.timestamp()) / 60 / 60
    while (until - current_day).days > 1:
        current_day += timedelta(days=1)
        if current_day.weekday() not in (5, 6):
            total += 8

    start_of_day = datetime(until.year, until.month, until.day, 9, 0, 0)
    total += (until.timestamp() - start_of_day.timestamp()) / 60 / 60

    return total


def _delta_to_current_time(since):
    # fixme reuse interval_sums
    # return (datetime.now(timezone(timedelta(hours=3))) - datetime.fromisoformat(since[:-5])).seconds / 60 / 60
    return (datetime.now(timezone(timedelta(hours=3))) - parse(since)).seconds / 60 / 60


def get_all_issue_statuses(issue_changelog):
    issue_changelog = [
        {'field': x['field'], 'toString': x['toString']}
        for y in issue_changelog
        for x in y['items']
    ]

    issue_changelog = list(filter(lambda x: x['field'] == 'status', issue_changelog))
    issue_changelog = set(map(lambda x: x['toString'], issue_changelog))

    return issue_changelog


def interval_sums(issue_changelog, statuses):
    issue_changelog = [
        {'field': x['field'], 'fromString': x['fromString'], 'toString': x['toString'], 'created': y['created']}
        for y in issue_changelog
        for x in y['items']
    ]
    issue_changelog = list(filter(lambda x: x['field'] == 'status', issue_changelog))
    indexes = _indexes(issue_changelog, lambda x: x['toString'] in statuses)
    total = 0

    for i in indexes:
        if i < len(issue_changelog) - 1:
            total += _delta_time(issue_changelog[i]['created'], issue_changelog[i + 1]['created'])
        else:
            total += _delta_to_current_time(issue_changelog[i]['created'])

    return total
