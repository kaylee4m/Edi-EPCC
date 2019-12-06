# Documents for TTDS coursework1
*This file does not include dataset. The process is for txt data file.*

Requirement: Python 3.7, nltk

In the file, there are three main .py documents: *get_index.py*, *query.py* and *tfidf.py*, with the utility documents *utility.py*. Besides, there is a stop worlds list which will be used in the process.

get_index.py: This file will do the preprocessing and create the index file. The result format is:
  term
      ID: pos1,pos2...

query_search.py:
	This file handles the boolean search, phrase search and proximity search.

tfidf.py:
	This file will implement the ranked IR based on TFIDF.


#How to Run
First, run the 'get index.py', you should input the orginal dataset and define the index file name you want to save. 
These can be done as the parameters in the commmand line.
Here is an example (dataset neme is 'trec.5000.txt' and saving the index file as 'index.txt')
The index file will be created after this step and this will be needed in the following steps.
----------------------------------------------
$ python get_index.py trec.5000.txt index.txt
----------------------------------------------

Second, run the 'query_search.py', you should input the index file name and the query file name. Here is an example:
-------------------------------------------------------
$ python query_search.py index.txt queries.boolean.txt
-------------------------------------------------------

Third, run the 'tfidf.py' to do the rank process based on TFIDF. You need to input the index file and calculation query file name. Here is an example:
-----------------------------------------------
$ python tfidf.py index.txt queries.ranked.txt
-----------------------------------------------
