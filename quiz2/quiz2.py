import csv
import matplotlib.pyplot as plt
from types import SimpleNamespace

csv_file = '/Applications/PyCharm CE.app/Contents/bin/github.com/QiaoLin22/qtm385/quiz2/cs_courses_2008_2018.csv'

def skip(i, row):
    return i == 0 or \
           int(row[11]) == 0 or \
           row[12].strip() == '' or \
           row[14].strip() != 'Active'
with open(csv_file) as fin:
    reader = csv.reader(fin)
    course_info = [row for i, row in enumerate(reader) if not skip(i, row)]

def info(row):
    r = row[0]
    term = (2000 + int((int(r) - 5000) / 10), int(r[-1]))
    r = row[12].split(',')
    instructor = (r[0].strip(), r[1].strip())

    return SimpleNamespace(
        term=term,
        subject=row[3].strip(),
        catalog=row[4].strip(),
        section=row[5].strip(),
        title=row[6].strip(),
        min_hours=int(row[8]),
        max_hours=int(row[9]),
        enrollment=int(row[11]),
        instructor=instructor)

def load_course_info(csv_file):
    with open(csv_file) as fin:
        reader = csv.reader(fin)
        course_info = [info(row) for i, row in enumerate(reader) if not skip(i, row)]

    return course_info

def term_to_year(term):
    return term[0] if term[1] == 9 else term[0] - 1

def enrollment_by_term(course_info):
    enroll = {}
    for c in course_info:
        term = c.term
        enroll[term] = enroll.get(term, 0) + c.enrollment

    return enroll

def enrollment_by_academic_year(course_info):
    enroll = {}
    for c in course_info:
        year = term_to_year(c.term)
        enroll[year] = enroll.get(year, 0) + c.enrollment

    return enroll

def instructor_by_term(course_info):
    inst = {}
    for c in course_info:
        if c.term in inst:
            inst[c.term].add(c.instructor)
        else:
            inst[c.term] = {c.instructor}

    return inst

def instructor_by_academic_year(course_info):
    inst = {}
    for c in course_info:
        year = term_to_year(c.term)
        if year in inst:
            inst[year].add(c.instructor)
        else:
            inst[year] = {c.instructor}

    return inst

def plot_dict(d):
    xs, ys = zip(*[(k, len(v)) for k, v in sorted(d.items())])
    plt.scatter(xs, ys)
    plt.plot(xs, ys)
    plt.grid(b='on')
    plt.show()

if __name__ == '__main__':
    csv_file = '/Applications/PyCharm CE.app/Contents/bin/github.com/QiaoLin22/qtm385/quiz2/cs_courses_2008_2018.csv'
    course_info = load_course_info(csv_file)
    d = instructor_by_academic_year(course_info)
    for k, v in sorted(d.items()): print(k, len(v))
    plot_dict(d)