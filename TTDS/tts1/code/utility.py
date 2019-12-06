import re
import sys
from nltk.stem import PorterStemmer

#read index file
def preprocess(indexfile_name):
    file = open(indexfile_name, encoding = 'UTF-8-sig') 
    dic = {}
    for line in file.readlines():
        match = re.match(r'^(\S+):\n$',line)
        match2 = re.match(r'^\t(\S+): (.+)$',line)
        if match is not None:
            tem = match.group(1)
        elif match2 is not None:
            dic[tem,match2.group(1)]=match2.group(2)
    return dic


ps = PorterStemmer()

# return the dict constaining the docid and corresponding position(s)
def get_dic_term(phrase,dictionary,processed=False):
    if not processed:
        phrase = phrase.lower()
        phrase = ps.stem(phrase)
    dic_term = {}
    for v,k in dictionary.items():
        if phrase == v[0]:
            dic_term[v[1]]= k.split(',')
    return dic_term


# Stopwords
def remove_stop():
    stopwords = open("Stopwords.txt", encoding = 'UTF-8-sig') 
    tokenized_words = []
    for a in stopwords:
        a = a.strip('\n')
        tokenized_words.append(a)
    return tokenized_words


