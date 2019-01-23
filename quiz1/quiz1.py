from gettext import install

import beautifulsoup4 as beautifulsoup4
import pip
import requests

url = 'http://registrar.emory.edu/faculty-staff/exam-schedule/spring-2019.html'
r = requests.get(url)
#print(r.text)


from bs4 import BeautifulSoup

html = BeautifulSoup(r.text, 'html.parser')
tbody = html.find('tbody')
schedule = []

for tr in tbody.find_all('tr'):
    tds = tr.find_all('td')
    class_time = tds[0].string.strip()
    exam_day   = tds[1].string.strip()
    exam_date  = tds[2].string.strip()
    exam_time  = tds[3].string.strip()
    schedule.append([class_time, exam_day, exam_date, exam_time])

print(schedule[0])
print(schedule[1])