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

'''


'''
data = pd.read_csv('/Users/Tim/PycharmProjects/qiao/project/201707.csv', error_bad_lines=False);
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
dictionary.filter_extremes(no_below=10, no_above=0.5, keep_n=100000)
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
bow_corpus[270]
from gensim import corpora, models
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]
from pprint import pprint

for doc in corpus_tfidf:
    pprint(doc)
    break
lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=5, id2word=dictionary, passes=2, workers=4)
for idx, topic in lda_model_tfidf.print_topics(-1):
    print(type(topic))
    print('Topic: {} Word: {}'.format(idx, topic))
for index, score in sorted(lda_model_tfidf[bow_corpus[20]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))
unseen_document = '*Premise*\\n\\n*In 1962, a mute janitor and her colleague work in a government laboratory and eventually discover an amphibious creature in a water tank, known as "The Asset". The janitor, out of loneliness, befriends the creature and falls in love.*\\n\\n\\nCurrently sitting at 97% on RT with 60 reviews. Really excited for this one.'

bow_vector = dictionary.doc2bow(preprocess(unseen_document))

for index, score in sorted(lda_model_tfidf[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda_model_tfidf.print_topic(index, 5)))
    
'''


import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

data = pd.read_csv('/Users/Tim/PycharmProjects/qiao/project/201707.csv', error_bad_lines=False);
data_text = data[['comment']]
data_text['index'] = data_text.index
documents = data_text

import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import pyLDAvis.gensim
import matplotlib.pyplot as plt
import seaborn as sns
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

processed_docs = documents['comment'].map(preprocess)
print(processed_docs[:10])
dictionary = gensim.corpora.Dictionary(processed_docs)
count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break
dictionary.filter_extremes(no_below=5, no_above=1, keep_n=100000)
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

bow_doc_4310 = bow_corpus[22]
from gensim import corpora, models
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]
from pprint import pprint

for doc in corpus_tfidf:
    pprint(doc)
    break

lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)
lda_model_tfidf.show_topics(10, num_words=10, formatted=False)



# get term relevance
viz = pyLDAvis.gensim.prepare(lda_model_tfidf, bow_corpus, dictionary, sort_topics=False)

name_dict = {   0: "topic1", # 1 on the chart
                1: "topic2",    # 2 on the chart
                2: "topic3",  # 3 on the chart
                3: "topic4", # 1 on the chart
                4: "topic5",    # 2 on the chart
                5: "topic6",  # 3 on the chart
                6: "topic7", # 1 on the chart
                7: "topic8",    # 2 on the chart
                8: "topic9",  # 3 on the chart
                9: "topic10",  # 3 on the chart
            }

for_viz = {}
# specify parameter
lambda_ = 0.4
viz_data = viz.topic_info
viz_data['relevance'] = lambda_ * viz_data['logprob'] + (1 - lambda_) * viz_data['loglift']
# plot the terms
plt.rcParams['figure.figsize'] = [20, 11]
fig, ax_ = plt.subplots(nrows=1, ncols=10)
ax = ax_.flatten()
for j in range(lda_model_tfidf.num_topics):
    df = viz.topic_info[viz.topic_info.Category=='Topic'+str(j+1)].sort_values(by='relevance', ascending=False).head(30)
    print(j)
    df.set_index(df['Term'], inplace=True)

    sns.barplot(y="Term", x="Freq",  data=df, ax=ax[j])
    sns.set_style({"axes.grid": False})
    print(j)
    ax[j].set_xlim([df['Freq'].min()-1, df['Freq'].max()+1])
    ax[j].set_ylabel('')
    ax[j].set_title(name_dict[j], size=15)
    ax[j].tick_params(axis='y', labelsize=13)
plt.show()

df = viz.topic_info[viz.topic_info.Category=='Topic'+str(1+1)].sort_values(by='relevance', ascending=False).head(30)
df.set_index(df['Term'], inplace=True)
sns.barplot(y="Term", x="Freq",  data=df, ax=ax[1])
sns.set_style({"axes.grid": False})

ax[1].set_xlim([df['Freq'].min()-1, df['Freq'].max()+1])
ax[1].set_ylabel('')
ax[1].set_title(name_dict[1], size=15)
ax[1].tick_params(axis='y', labelsize=13)
plt.show()


'''


for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))
for index, score in sorted(lda_model_tfidf[bow_corpus[22]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))
unseen_document = 'James Bond slaughtered the daughter of the king'
bow_vector = dictionary.doc2bow(preprocess(unseen_document))
'''