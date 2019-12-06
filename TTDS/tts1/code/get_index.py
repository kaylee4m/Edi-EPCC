import re
import sys
import nltk
from nltk.stem import PorterStemmer
from utility import remove_stop
import time


inputfile = open(sys.argv[1],encoding = 'UTF-8-sig')
dic = {}
file_lines = inputfile.readlines()
line = 0
for i in range(len(file_lines)//3):
    # split line of txt to get content, save in dict
    a = (file_lines[line+1].strip().split('HEADLINE: FT  ')[-1]+' '+file_lines[line+2].strip().split('TEXT: ')[-1]).lower()  #id
    dic[file_lines[line].strip().split(' ')[-1]] = re.sub('[!"#$%&()*+,-./:;<=>?@?！[\\]^_`{|}~\s]', " ", a)
    line+=3


def process(dic):
    # Stopwords
    stopword = remove_stop()

    # tokenisation and stemming
    ps = PorterStemmer()
    for docid, doc in dic.items():
        tmp = re.split(r'[;,&%-.\[\]\(\)\'\/"?!\s]\s*',doc)
        while '' in tmp:
            tmp.remove('')
        for stop in stopword:
            while stop in tmp:
                tmp.remove(stop)
        tmp = [ps.stem(i) for i in tmp]
        dic[docid]= tmp


    # get inverted_index
    inverted_index = {}
    for docid, doc in dic.items():
        for word in doc:
            if word not in inverted_index.keys():
                inverted_index[word] = [docid]
            elif docid not in inverted_index[word]:
                inverted_index[word].append(docid)

    return inverted_index


def main():
    t = time.time()
    savefile=sys.argv[2]
    outfile = open(savefile,'w')

    inverted_index = process(dic)

    for word, doclist in inverted_index.items():
        print(word,end=':\n',file = outfile)
        for doc in doclist:
            print('\t',end='',file = outfile)
            print(doc,end=': ',file = outfile)
            position = [str(i+1) for i,docword in enumerate(dic[doc]) if docword==word]
            if len(position)>1:
                print(",".join(position),file = outfile)
            else:
                print(position[0],file = outfile)         
        print('\n',file = outfile)

    print("runing time:",end='')
    print(time.time()-t)
    inputfile.close()
    outfile.close()
 
main()
   