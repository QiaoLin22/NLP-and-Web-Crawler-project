import requests

url = 'http://registrar.emory.edu/faculty-staff/exam-schedule/spring-2019.html'
r = requests.get(url)
from bs4 import BeautifulSoup

html = BeautifulSoup(r.text, 'html.parser')
tbody = html.find('tbody')
schedule = []

for tr in tbody.find_all('tr'):
    tds = tr.find_all('td')
    class_time = tds[0].string.strip()
    exam_day = tds[1].string.strip()
    exam_date = tds[2].string.strip()
    exam_time = tds[3].string.strip()
    schedule.append([class_time, exam_day, exam_date, exam_time])

import re

TIME_DAYS = re.compile('(\d{1,2}):(\d\d)\s+([A-Za-z]+)')

from typing import Optional


def norm_time(hour: str, minute: str) -> int:
    h = int(hour)
    m = int(minute)

    if h:
        if h < 8:
            h += 12

    return h * 100 + m


def norm_days(days: str) -> int:
    DAYS = [('M', 0), ('TU', 1), ('W', 2), ('TH', 3), ('F', 4)]
    days = days.upper()
    b = ['0'] * 5

    for d, i in DAYS:
        if d in days:
            b[i] = '1'
            days = days.replace(d, '')

    if 'T' in days:
        b[1] = '1'
        days = days.replace('T', '')

    return int(''.join(b), 2)


from typing import Dict, Tuple


def extract_exam_schedule(url) -> Dict[Tuple[int, int], Tuple[str, str, str]]:
    r = requests.get(url)
    html = BeautifulSoup(r.text, 'html.parser')
    tbody = html.find('tbody')
    schedule = {}

    for tr in tbody.find_all('tr'):
        tds = tr.find_all('td')
        class_time = tds[0].string.strip()
        m = TIME_DAYS.match(class_time)
        if m:
            time = norm_time(int(m.group(1)), int(m.group(2)))
            days = norm_days(m.group(3))
            key  = (time, days)
            exam_day  = tds[1].string.strip()
            exam_date = tds[2].string.strip()
            exam_time = tds[3].string.strip()
            schedule[key] = (exam_day, exam_date, exam_time)

    return schedule


if __name__ == '__main__':
    url = 'http://registrar.emory.edu/faculty-staff/exam-schedule/spring-2019.html'
    exam_schedule = extract_exam_schedule(url)
    for k, v in exam_schedule.items():
        print('%s : %s' % (k, v))