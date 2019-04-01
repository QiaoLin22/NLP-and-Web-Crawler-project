import re
import codecs
import os
import glob
import requests
import bibtexparser
from collections import Counter

from types import SimpleNamespace

def load_map(map_file):
    fin = open(map_file)
    d = {}

    for i, line in enumerate(fin):
        l = line.strip().split('\t')
        if len(l) == 3:
            key = l[0]
            d[key] = SimpleNamespace(weight=float(l[1]), series=l[2])

    return d
def get_entry_dict(bib_map, bib_dir):
    """
    :param bib_map: the output of load_map().
    :param bib_dir: the input directory where the bib files are stored.
    :return: a dictionary where the key is the publication ID (e.g., 'P17-1000') and the value is its bib entry.
    """
    re_pages = re.compile('(\d+)-{1,2}(\d+)')

    def parse_name(name):
        if ',' in name:
            n = name.split(',')
            if len(n) == 2: return n[1].strip() + ' ' + n[0].strip()
        return name

    def get(entry, weight, series):
        entry['author'] = [parse_name(name) for name in entry['author'].split(' and ')]
        entry['weight'] = weight
        entry['series'] = series
        return entry['ID'], entry

    def valid(entry, weight):
        if weight == 1.0:
            if 'pages' in entry:
                m = re_pages.search(entry['pages'])
                return m and int(m.group(2)) - int(m.group(1)) > 4
            return False

        return 'author' in entry

    bibs = {}
    for k, v in bib_map.items():
        fin = open(os.path.join(bib_dir, k+'.bib'))
        bib = bibtexparser.loads(fin.read())
        bibs.update([get(entry, v.weight, v.series) for entry in bib.entries if valid(entry, v.weight)])

    return bibs

def get_email_dict(txt_dir):

    def chunk(text_file, page_limit=2000):
        fin = codecs.open(text_file, encoding='utf-8')
        doc = []
        n = 0

        for line in fin:
            line = line.strip().lower()
            if line:
                doc.append(line)
                n += len(line)
                if n > page_limit: break

        return ' '.join(doc)

    re_email = re.compile('[({\[]?\s*([a-z0-9\.\-_]+(?:\s*[,;|]\s*[a-z0-9\.\-_]+)*)\s*[\]})]?\s*@\s*([a-z0-9\.\-_]+\.[a-z]{2,})')
    email_dict = {}

    for txt_file in glob.glob(os.path.join(txt_dir, '*.txt')):
        try:
            doc = chunk(txt_file)
        except UnicodeDecodeError:
            # print(txt_file)
            continue
        emails = []

        for m in re_email.findall(doc):
            ids = m[0].replace(';', ',').replace('|', ',')
            domain = m[1]

            if ',' in ids:
                emails.extend([ID.strip()+'@'+domain for ID in ids.split(',') if ID.strip()])
            else:
                emails.append(ids+'@'+domain)

        if emails:
            key = os.path.basename(txt_file)[:-4]
            email_dict[key] = emails

    return email_dict


def print_emails(entry_dict, email_dict, email_file):
    fout = open(email_file, 'w')
    for k, v in sorted(entry_dict.items()):
        n = len(v['author'])
        l = [k, str(n)]
        if k in email_dict: l.extend(email_dict[k][:n])
        fout.write('\t'.join(l) + '\n')

    fout.close()

def load_emails(email_file):
    fin = open(email_file)
    d = {}

    for line in fin:
        l = line.split('\t')
        d[l[0]] = SimpleNamespace(num_authors=int(l[1]), emails=l[2:])

    return d

def load_institutes(institute_file):
    fin = open(institute_file)
    d = {}

    for line in fin:
        l = line.split('\t')
        d[l[1]] = SimpleNamespace(name=l[0], city=l[2], state=l[3])

    fin.close()
    return d

def match_institutes(email_dict, institute_dict):
    for ID, v in email_dict.items():
        for email in v.emails:
            idx = email.rfind('@')
            domain = email[idx+1:]
            if domain.endswith('edu') and domain not in institute_dict:
                while True:
                    fidx = domain.find('.')
                    ridx = domain.rfind('.')
                    if fidx != ridx: domain = domain[fidx+1:]
                    else: break
            if domain.endswith('edu') and domain not in institute_dict:
                print(domain)

def change_email_dict(email_dict):
    for k, v in sorted(email_dict.items()):
        try:
                if v[0][0:9] == "firstname":
                    domin = v[0][18:]
                    del v[0]
                    for i in range(0,len(entry_dict[k]['author'])):
                        entry_dict[k]['author'][i]=entry_dict[k]['author'][i].replace(" ",".")
                        v.append(entry_dict[k]['author'][i]+domin)
                elif v[0][0:10] == "first-name":
                    domin = v[0][20:]
                    del v[0]
                    for i in range(0,len(entry_dict[k]['author'])):
                        entry_dict[k]['author'][i]=entry_dict[k]['author'][i].replace(" ",".")
                        v.append(entry_dict[k]['author'][i]+domin)
                elif v[0][0:5] == "first":
                    domin = v[0][10:]
                    del v[0]
                    for i in range(0,len(entry_dict[k]['author'])):
                        entry_dict[k]['author'][i]=entry_dict[k]['author'][i].replace(" ",".")
                        v.append(entry_dict[k]['author'][i]+domin)
        except IndexError:
            continue
        except KeyError:
            continue
def weight(email_dict):
    w = {}
    for k, v in email_dict.items():
        try:
            for email in v.emails:
                idx = email.rfind('@')
                domain = email[idx + 1:-2]  # to deal with the /n recount problem
                w[domain] = w.get(domain, 0) + 1
        except:
            length = len(w[k])
            KeyError
        try:
            for i in w[k]:

                w[k][i] = w[k][i]/length
        except:
            KeyError

    return w

MAP_FILE = '/Users/mycomputer/Desktop/qtm385data science/nlp-ranking/dat/bib_map.tsv'
BIB_DIR = '/Users/mycomputer/Desktop/qtm385data science/nlp-ranking/bib/'
bib_map = load_map(MAP_FILE)
entry_dict = get_entry_dict(bib_map, BIB_DIR)
TXT_DIR = '/Users/mycomputer/Desktop/qtm385data science/nlp-ranking/dat/txt/'
email_dict = get_email_dict(TXT_DIR)

change_email_dict(email_dict)
EMAIL_FILE = '/Users/mycomputer/Desktop/qtm385data science/nlp-ranking/dat/email_map.tsv'
email_dict2 = load_emails(EMAIL_FILE)
INSTITUTE_FILE = '/Users/mycomputer/Desktop/qtm385data science/nlp-ranking/dat/us_institutes.tsv'
institute_dict = load_institutes(INSTITUTE_FILE)
print_emails(entry_dict, email_dict, EMAIL_FILE)

weight = weight(email_dict2)
print(weight)


