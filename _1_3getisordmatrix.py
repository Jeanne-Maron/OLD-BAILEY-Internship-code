# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:39:35 2026

@author: jeann2e
"""

from _1tfidfmatrix import matrix_doc, infos_doc, doc_selected, t0, sig, sample_path
import time
import numpy as np
from tqdm import tqdm

# The information used for the computation of the Getis-Ord matrix is gathered here.
list_code = list(infos_doc[:,0])
list_annee = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
N_doc = len(matrix_doc[0])

# The neighbouring function of the Getis-Ord's z-score is defined
def vois(code1,code2):
    a1 = list_annee[code1]
    a2 = list_annee[code2]
    return ( 1 / (sig * np.sqrt(2*np.pi)) ) * np.exp( - (a1-a2)**2 / (2* sig**2) )

# The Getis-Ord's z-score is defined
def gozscore(moy_w,sig_w,term,doc):
    sumtop , sumdown1 , sumdown2 = 0 , 0 , 0
    for code in range(N_doc) :
        w = vois(doc,code)
        sumtop += w * (matrix_doc[term,doc] - moy_w)
        sumdown1 += w**2
        sumdown2 += w
    return ( sumtop ) / ( sig_w * np.sqrt( (N_doc*sumdown1 - sumdown2**2) / (N_doc-1) ) )

# Now the Getis-Ord matrix is computed with the lexicon defined previously, with the set of 
# documents defined previously.       
t1 = time.time()
print('\n'+'''The Getis Ord's z-score matrix is created.''')
matrix_go = []
for i in tqdm(range(len(matrix_doc))) :
    list_word = list(matrix_doc[i])
    moy_w = np.mean(list_word)
    sig_w = np.std(list_word)
    matrix_go.append([ gozscore( moy_w , sig_w , i , j ) for j in range(N_doc) ])
matrix_go = np.array(matrix_go)
np.savetxt(sample_path+"matrix_go.txt",matrix_go)

t2 = time.time()

# The information are printed in the console and saved in the sample folder.
print('''The Getis Ord's z-score matrix was made in''',(t2-t1)//60,'minutes and',round((t2-t1)%60,2),'seconds.')
print('\nTotal time of the sample :',(t2-t0)//60,'minutes and',round((t2-t0)%60,2),'seconds.')
f = open(sample_path+"Console Python.txt",'r',encoding='utf-8')
lines = f.readlines()
f.close()
f = open(sample_path+"Console Python.txt",'w+',encoding='utf-8')
for line in lines :
    f.write(line)
f.write(''''\n\nThe Getis Ord's z-score matrix is created.''')
f.write(''''\nThe Getis Ord's z-score matrix was made in '''+str((t2-t1)//60)+' minutes and '+str(round((t2-t1)%60,2))+' seconds.')
f.write(''''\n\nTotal time of the sample : '''+str((t2-t0)//60)+' minutes and '+str(round((t2-t0)%60,2))+' seconds.')
f.close()
      

      
