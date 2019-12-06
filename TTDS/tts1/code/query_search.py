import re
import nltk
import sys
from nltk.stem import PorterStemmer
from utility import preprocess, get_dic_term,remove_stop
import time



indexfile = sys.argv[1]
outfile = open("results.boolean.txt",'w')
queryfile = open(sys.argv[2])

dic = preprocess(indexfile) # read index file into dict


# split phrase to get the id list 
def phrase_search(phrase,distance,flag_digit):
    phrase_idlist = []
    if(len(phrase) == 1):
        # if it is one word
        word_list = get_dic_term(phrase[0],dic)
        for i,j in word_list.items():
            phrase_idlist.append(i)       
    else:
        word_list1 = get_dic_term(phrase[0],dic)
        word_list2 = get_dic_term(phrase[1],dic)
        
        for id1,term1 in word_list1.items():
            if id1 in word_list2.keys():
                for i in term1:
                    for j in word_list2[id1]:
                        if flag_digit==1:
                            # proximity search 
                            if (abs(int(i)-int(j))<=distance):
                                if id1 not in phrase_idlist:
                                    phrase_idlist.append(id1)  
                        # phrase search            
                        elif int(j)-int(i)==1:
                            if id1 not in phrase_idlist:
                                    phrase_idlist.append(id1)

    return phrase_idlist


def func_query(query):
    # flag the key operation, if unchanged, then does not exist 
    op_and = -1
    op_or = -1
    op_not = -1
    distance = 1
    flag_digit = 0

    if 'AND' in query:
        op_and = query.index('AND')
    elif 'OR' in query:
        op_or = query.index('OR')    
    if 'NOT' in query:
        op_not = query.index('NOT') 
    
    if op_and==-1 and op_or==-1:
        # if no AND and no OR  
        if query[0][1:].isdigit():
            # if #(), then proximity search 
            flag_digit =1
            distance = int(query[0][1:])
            phrase_1 = query[1:]
        else:
            #one term
            phrase_1 = query
        return phrase_search(phrase_1,distance,flag_digit)
        
    elif op_and!=-1:
        phrase_1 = query[0:op_and]
        phrase_2 = query[op_and+1:]
    else:
        phrase_1 = query[0:op_or]
        phrase_2 = query[op_or+1:]

    if op_not!=-1:
        phrase_2 = phrase_2[1:]

        
    l1 = phrase_search(phrase_1, distance, flag_digit)
    l2 = phrase_search(phrase_2, distance, flag_digit)

    if op_not==-1:
        if op_and!=-1:
            return sorted(set(l1) & set(l2),key=int)
        elif op_or!=-1:
            return sorted(set(l1) | set(l2),key=int)
        else:
            return "wrong"
    else:
        if op_and!=-1:
            return sorted(set(l1) - set(l2),key=int)
        elif op_or!=-1:
            return sorted(set(l1) ^ set(l2),key=int)
        else:
            return "wrong"


def main():
    t = time.time()
    for i, line in enumerate(queryfile.readlines()):
        query = re.split(r'[;,&%-.\[\]\(\)\'\/"?!\s]\s*',line)
        query.remove(query[0]) # remove query id 
        while '' in query:
            query.remove('')
        for item in func_query(query):
            outfile.write(str(i+1)+" 0 "+item+' 0 1 0\n')

    print("runing time: ",end='')
    print(time.time()-t)
    queryfile.close()
    outfile.close()


main()

    


