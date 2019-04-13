import pandas as pd
from textblob import TextBlob
import nltk
nltk.download('punkt')

from collections import Counter
'''
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
    

nltk.download()
'''


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

comment = pd.read_csv('/Users/Tim/PycharmProjects/qiao/project/dataframe1.csv')

a = []
for k in comment.values:
    c = k
    print(str(c))
    a.append(str(c))


a


TB = TextBlob(''.join(a))
print(TB.words)
print(len(TB.words))

counter = Counter(TB.words)
counter.most_common()[60:100]
TB.sentiment