# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:15:44 2026

@author: jeann2e
"""

from _1dictionary import dico, doc_occ, doc_bd, sample_path
from _1dictionary import t0, infos_doc, doc_selected, sig
import time
from tqdm import tqdm
import numpy as np
import math

# The definition used for the TimeFrequency-InverseDocumentFrequency representation is the one used in
# the article "Detecting Historical Turning Points in Italian Media: A Complex Systems Approach to a 
# Diachronic News Corpus", by Dario Zarcone, Salvatore Miccichè and David Sánchez

list_code = [ doc[0] for doc in doc_bd ]
ntot_doc = len(doc_bd)

# The TF-IDF is defined for every type in the lexicon for every document.
def tfidf(i,code_doc) :
    term = i
    idf = math.log( (1+ntot_doc) / (1+doc_occ[i]) ) + 1
    tf = 0
    pos_doc = list_code.index(code_doc)
    for word in doc_bd[pos_doc][1] :
        if word == term :
            tf += doc_bd[pos_doc][1][word]
    return tf*idf

# Now the TF-IDF matrix is computed with the lexicon defined previously, with the set of documents
# defined previously.
t1 = time.time()
print('\n'+'The TF-IDF matrix is created.')
matrix_doc , count = [] , 0
for i in dico :
    line_matrix = [ tfidf(i,doc[0]) for doc in doc_bd ]
    matrix_doc.append(line_matrix)
    count += 1
    print( count , '/' , len(dico) )
matrix_doc = np.array(matrix_doc)
np.savetxt(sample_path+"matrix_doc.txt",matrix_doc)
t2 = time.time()

# The information are printed in the console and saved in the sample folder.
print('The TF-IDF matrix was made in',(t2-t1)//60,'minutes and',round((t2-t1)%60,2),'seconds.')
f = open(sample_path+"Console Python.txt",'r',encoding='utf-8')
lines = f.readlines()
f.close()
f = open(sample_path+"Console Python.txt",'w+',encoding='utf-8')
for line in lines :
    f.write(line)
f.write('\n\nThe TF-IDF matrix is created.')
f.write('\nThe TF-IDF matrix was made in '+str(round((t2-t1)%60,2))+' seconds.')
f.close()