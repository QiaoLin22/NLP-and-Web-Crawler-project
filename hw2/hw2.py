import csv
from types import SimpleNamespace
from collections import Counter
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
csv_file = '/Applications/PyCharm CE.app/Contents/bin/github.com/QiaoLin22/qtm385/hw2/cs_courses_2008_2018.csv'


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
        instructor=instructor,
        courseid = row[3].strip()+ row[4].strip())


def load_course_info(csv_file):
    with open(csv_file) as fin:
        reader = csv.reader(fin)
        course_info = [info(row) for i, row in enumerate(reader) if not skip(i, row)]

    return course_info


def is_research_course(catalog):
    return catalog != '130R' and 'R' in catalog


def is_grad_course(catalog):
    return int(catalog[0]) > 4


def professor_frequency(prof_course_dict):
    return Counter([k for v in prof_course_dict.values() for k in v.keys()])


def course_by_instructor(course_info, lastname, include_research=False):
    def match(c):
        return c.instructor[0] == lastname and \
               (include_research or not is_research_course(c.catalog)) and \
               (is_grad_course(c.catalog))

    courses = {(*c.term, c.subject, c.catalog) for c in course_info if match(c)}
    return Counter([t[2:] for t in courses])


def courses_by_instructors(course_info, include_research=False):
    d = {}
    for c in course_info:
        if include_research or not is_research_course(c.catalog) and is_grad_course(c.catalog):
            key = c.instructor
            val = (*c.term, c.subject, c.catalog)
            if key in d: d[key].add(val)
            else: d[key] = {val}

    return {k: Counter([t[2:] for t in v]) for k, v in d.items()}


def what_is_prof_x_special_courses(course_info, lastname):
    prof_course_dict = courses_by_instructors(course_info)
    prof_freq = professor_frequency(prof_course_dict)
    prof_courses = course_by_instructor(course_info, lastname)  # this is inefficient
    N = len(prof_course_dict)

    for k, v in prof_courses.items():
        prof_courses[k] *= math.log(N / prof_freq[k])

    return prof_courses


def prof_to_vec(course_info, normalize=True, include_research=False):
    prof_course_dict = courses_by_instructors(course_info, include_research)
    prof_freq = professor_frequency(prof_course_dict)
    N = len(prof_freq)
    course_dict = {c: i for i, c in enumerate(sorted(list(prof_freq.keys())))}
    p2v = {}

    for prof_name, counts in prof_course_dict.items():
        vec = np.zeros(len(course_dict))

        for k, v in counts.items():
            if k in course_dict:
                i = course_dict[k]
                vec[i] = v * math.log(N / prof_freq[k])

        if normalize: vec /= np.sum(vec)
        p2v[prof_name] = vec

    return p2v


#Below is the three functions for hw2


def course_trend(course_info):

    trend = {}
    spring = 0
    summer = 0
    fall = 0
    for c in course_info:
        key = c.courseid
        if key in trend:
            if c.term[1] == 1:
                spring += 1
                trend[key] = (spring, summer, fall)
            elif c.term[1] == 6:
                summer += 1
                trend[key] = (spring, summer, fall)
            elif c.term[1] == 9:
                fall += 1
                trend[key] = (spring, summer, fall)
        else:
            trend[key] = (spring,summer,fall)

    for k,v in trend.items():
        sum = v[0] + v[1] + v[2]
        trend[k] = (v[0] / sum, v[1] / sum, v[2] / sum)
    return trend


def special_topics(course_info):
    topics = dict()
    for c in course_info:
        if int(c.catalog[0]) > 4:
            key = c.instructor[1]+ " "+ c.instructor[0]
            topics[key] = what_is_prof_x_special_courses(course_info, c.instructor[0])

    return topics


def vector_plot(course_info):
    p2v = prof_to_vec(course_info)
    profs = sorted(p2v.keys())
    vectors = np.array([p2v[p] for p in profs])
    xy = TSNE(n_components=2).fit_transform(vectors)
    fig, ax = plt.subplots()
    fig.set_size_inches(14, 10)
    x = xy[:, 0]
    y = xy[:, 1]
    ax.scatter(x, y)
    for i, p in enumerate(profs):
        ax.annotate(p[0], (x[i], y[i]))
    plt.show()
    pass

csv_file = '/Applications/PyCharm CE.app/Contents/bin/github.com/QiaoLin22/qtm385/hw2/cs_courses_2008_2018.csv'
course_info = load_course_info(csv_file)
prof_course_dict = courses_by_instructors(course_info)
d = course_trend(course_info)
for k, v in sorted(d.items()): print(k,v)
a = special_topics(course_info)
for k, v in sorted(a.items()):print(k,v)
vector_plot(course_info)