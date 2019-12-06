import re
import math
import sys
from nltk.stem import PorterStemmer
from utility import preprocess, get_dic_term,remove_stop
import time



indexfile = sys.argv[1]
outfile = open("results.ranked.txt",'w')
queryfile = open(sys.argv[2])

dic = preprocess(indexfile) # read index file into dict
ps = PorterStemmer()

# function of calculating the tfidf score
def tfidf_score(queries,docID,dictionary):
    socre = 0
    for i, phase in enumerate(queries):
        terms_index = get_dic_term(phase,dictionary,processed=True)
        df_fren = len(terms_index)
        if docID in terms_index.keys():
            tf_fren = len(terms_index[docID])
        else:
            tf_fren = 0 
        if df_fren==0 or tf_fren==0:
            s = 0
        else:
            s = (1+math.log(tf_fren,10))*math.log((5000/df_fren),10)

        socre += s
    return socre

# reduce the size of dictionary to reduce the runing time
def get_small_dict(queries,old_dict,docIDs_set):
    small_dict = old_dict.copy()
    for key, _ in old_dict.items():
        if not key[0] in queries:
            small_dict.pop(key)
        elif not key[1] in docIDs_set:
            small_dict.pop(key)
    return small_dict

# obtain the union_set of the query term
def get_union_set(queries,old_dict):
    docID_set = set()
    for index ,item in enumerate(queries):
        tmp = item.lower()
        queries[index] = ps.stem(tmp)
        terms_index = get_dic_term(queries[index], old_dict, processed=True)
        docID_set = docID_set.union(set(terms_index.keys()))
    return docID_set

def main():
    t = time.time()
    maxsize = 1000
    stopword = remove_stop()

    for i, line in enumerate(queryfile.readlines()):
        result_list = []
        query = re.split(r'[;,&%-.\[\]\(\)\'\/"?!\s]\s*',line)
        query.remove(query[0])
        while '' in query:
            query.remove('')
        for stop in stopword:
            while stop in query:
                query.remove(stop)

        docIDs_set = get_union_set(query, dic)

        new_dict = get_small_dict(query,dic,docIDs_set)

        for s,docid in enumerate(docIDs_set):
            if s >= maxsize:
                break
            score = (i+1, docid, format(tfidf_score(query,docid,new_dict),'.4f'))
            # print(score)
            result_list.append(score)
        
        # sort the results    
        for item in sorted(result_list,key=lambda x:float(x[2]),reverse = True):
            outfile.write(str(item[0])+" 0 "+str(item[1])+' 0 '+str(item[2])+' 0\n')

    print("runing time: ",end='')
    print(time.time()-t)
    queryfile.close()
    outfile.close()
        

main()

