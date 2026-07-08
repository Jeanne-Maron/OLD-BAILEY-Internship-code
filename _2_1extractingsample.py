# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:59:58 2026

@author: jeann2e
"""

# This has to be changed to analyze the right sample, in the right place.
sample = '1'
sample_path = "C:\\Users\\jeann\\Documents\\masters_internship\\old-bailey\\_sample_"+sample+"\\"

# To extract all of the informations of a given sample, this can be used in the other files of 
# Part 2.
import numpy as np

# Extracting the informations of infos_doc
infos_doc = []
with open("infos_doc.txt",'r',encoding='utf-8') as file :
    count , info_doc = 0 , []
    for line in file :
        count , line = count+1 , line.strip()
        if count < 10 :
            if count == 4 :
                line = int(line)
            info_doc.append(line)
        if count == 10 :
            infos_doc.append(info_doc)
            info_doc , count = [ line ] , 1
    infos_doc.append(info_doc)
infos_doc = np.array(infos_doc)

# Extracting the lexicon, the total occurences and the document occurences
dico , tot_occ , doc_occ = [] , [] , []
with open(sample_path+"dico_filtered.txt",'r',encoding='utf-8') as file :
    count = 0
    for line in file :
        count , line = count+1 , line.strip()
        if count == 1 :
            dico.append(line)
        elif count == 2 :
            tot_occ.append(int(line))
        elif count == 3 :
            doc_occ.append(int(line))
            count = 0

#  Extracting additional informations like the names of the documents selected and their lengths
doc_selected = []
with open(sample_path+"doc_selected.txt",'r',encoding='utf-8') as file:
    for line in file:
        doc_selected.append(line.strip('\n'))
len_selected = []
with open(sample_path+"len_documents.txt",'r',encoding='utf-8') as file:
    for line in file:
        len_selected.append(line.strip('\n'))

# The matrices are extracted
matrix_doc = np.loadtxt(sample_path+"matrix_doc.txt", dtype=float)
matrix_go = np.loadtxt(sample_path+"matrix_go.txt", dtype=float)
matrix_doc , matrix_go = np.transpose(matrix_doc) , np.transpose(matrix_go)

# The relevant information is shown
print('\n')
f = open(sample_path+"Console Python.txt",'r',encoding='utf-8')
lines = f.readlines()
f.close()
for i in lines :
    print(i[:-1])












