import pandas as pd
import nltk
'''
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

data = pd.read_csv('/Users/Tim/PycharmProjects/qiao/project/dataframe1.csv', error_bad_lines=False);
a = []
for k in data.values:
    c = str(k).split('&&')
    for i in c:
        a.append(i)
df = pd.DataFrame({'col':a})
df
df['index'] = df.index
documents = df
'''
data = pd.read_csv('/Users/Tim/PycharmProjects/qiao/project/2017_8.csv', error_bad_lines=False);
data = data["comment"]
data.head()
a = []
for k in data.values:
    c = str(k).split('&&')
    for i in c:
        a.append(i)
df = pd.DataFrame({'col':a})
df



df['index'] = df.index
documents = df

pip install paramiko
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)

nltk.download('wordnet')
stemmer = SnowballStemmer('english')
original_words = ['caresses', 'flies', 'dies', 'mules', 'denied','died', 'agreed', 'owned',
           'humbled', 'sized','meeting', 'stating', 'siezing', 'itemization','sensational',
           'traditional', 'reference', 'colonizer','plotted']
singles = [stemmer.stem(plural) for plural in original_words]
pd.DataFrame(data = {'original word': original_words, 'stemmed': singles})
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

doc_sample = documents[documents['index'] == 0].values[0][0]

print('original document: ')
words = []
for word in doc_sample.split(' '):
    words.append(word)
print(words)
print('\n\n tokenized and lemmatized document: ')
print(preprocess(doc_sample))

processed_docs = documents['col'].map(preprocess)
print(processed_docs[:10])
dictionary = gensim.corpora.Dictionary(processed_docs)
count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break
dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
bow_corpus[270]
from gensim import corpora, models
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]
from pprint import pprint

for doc in corpus_tfidf:
    pprint(doc)
    break
lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=8, id2word=dictionary, passes=2, workers=4)
for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))
for index, score in sorted(lda_model_tfidf[bow_corpus[270]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))
unseen_document = '*Premise*\\n\\n*In 1962, a mute janitor and her colleague work in a government laboratory and eventually discover an amphibious creature in a water tank, known as "The Asset". The janitor, out of loneliness, befriends the creature and falls in love.*\\n\\n\\nCurrently sitting at 97% on RT with 60 reviews. Really excited for this one.'

bow_vector = dictionary.doc2bow(preprocess(unseen_document))

for index, score in sorted(lda_model_tfidf[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda_model_tfidf.print_topic(index, 5)))