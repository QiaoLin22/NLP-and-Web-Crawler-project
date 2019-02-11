from typing import List
import requests

url = 'http://atlas.college.emory.edu/class-schedules/spring-2019.php'
r = requests.get(url)
from bs4 import BeautifulSoup
import re
TIME_DAYS = re.compile('(\d{1,2}):(\d\d)\s+([A-Za-z]+)')


TIME = re.compile('(\d{1,2}):(\d\d)')


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
            key = (time, days)
            exam_day = tds[1].string.strip()
            exam_date = tds[2].string.strip()
            exam_time = tds[3].string.strip()
            schedule[key] = (exam_day, exam_date, exam_time)

    return schedule


def extract_class_schedule(url) -> Dict[int, Tuple[str, str, str, str, int, str, str, str]]:
    r = requests.get(url)
    html = BeautifulSoup(r.text, 'html.parser')
    schedule = {}

    for tr in html.find_all('tr'):
        td1 = tr.find_all('td')
        if len(td1) < 10: continue

        program = td1[0].string.strip()
        number = td1[1].string.strip()
        section = td1[2].string.strip()
        title = td1[5].text.strip()
        opus = int(td1[6].string)
        course = td1[0].string.strip() + td1[1].string.strip() + '-' + td1[2].string.strip()

        td2 = td1[9].find_all('td')
        days = td2[0].string
        if days is None:
            continue
        else:
            days = days.strip()
        time = td2[1].text.strip()
        instructor = td2[3].string

        schedule[course] = (program, number, section, title, opus, days, time, instructor)

    return schedule


def get_exam_schedule(opus: int, exam_schedule: Dict[Tuple[int, int], Tuple[str, str, str]], class_schedule: Dict[int, Tuple[str, str, str, str, int, str, str, str]]) -> Tuple[str, str, str]:
    s = class_schedule.get(opus, None)
    if s is None: return None
    days = norm_days(s[5])
    m = TIME.match(s[6])
    time = norm_time(m.group(1), m.group(2))
    key = (time, days)
    return exam_schedule.get(key, None)


def generate_html_files(url_exam:str, url_class:str, html_dir: str):
    name = (html_dir).lower()+'.html'
    exam_schedule = extract_exam_schedule(url_exam)
    class_schedule = extract_class_schedule(url_class)
    soup = BeautifulSoup("<html></html>", 'html.parser')
    html = soup.html

    table = soup.new_tag('table')
    html.append(table)

    thead = soup.new_tag('thead')
    table.append(thead)

    tr = soup.new_tag('tr')
    thead.append(tr)

    for s in ['Course', 'Opus', 'Title', 'Instructor', 'Exam Schedule']:
        td = soup.new_tag('td')
        td.string = s
        tr.append(td)

    tbody = soup.new_tag('tbody')
    table.append(tbody)

    for k, v in class_schedule.items():
        if v[0] != html_dir: continue
        course = v[0] + v[1] + '-' + v[2]
        opus = str(v[4])
        title = v[3]
        instructor = str(v[-1])
        t = get_exam_schedule(k, exam_schedule, class_schedule)
        if t is None: continue
        ex_schedule = ', '.join(list(t))

        tr = soup.new_tag('tr')
        tbody.append(tr)

        for s in [course, opus, title, instructor, ex_schedule]:
            td = soup.new_tag('td')
            td.string = s
            tr.append(td)
    with open(name, 'w') as fout:
        fout.write(soup.prettify())
    pass


def print_exam_schedule(course_ids: List[str]):
    exam_schedule = extract_exam_schedule(url_exam)
    class_schedule = extract_class_schedule(url_class)
    for s in course_ids:
        s = class_schedule.get(s,None)
        if s is None: return None
        days = norm_days(s[5])
        m = TIME.match(s[6])
        time = norm_time(m.group(1), m.group(2))
        key = (time, days)
        print(exam_schedule.get(key, None))


def generate_list(url):
    r = requests.get(url)
    html = BeautifulSoup(r.text, 'html.parser')
    titles = []
    for a in html.find_all('a'):
        title = a.string.strip()
        titles.append(title)
    return titles


if __name__ == '__main__':
    url = "http://localhost:63342/qtm385/hw1/index.html?_ijt=vpejepesq6sbmt1rmq5lbnht43"
    url_exam = 'http://registrar.emory.edu/faculty-staff/exam-schedule/spring-2019.html'
    url_class = 'http://atlas.college.emory.edu/class-schedules/spring-2019.php'
    html_dir = generate_list(url)

for s in html_dir:
    generate_html_files(url_exam, url_class, s)

print_exam_schedule(['AAS100-1', 'QTM385-1'])






