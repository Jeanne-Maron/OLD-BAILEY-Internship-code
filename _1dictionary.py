# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:37:26 2026

@author: jeann2e
"""


from _1_2settingparameters import doc_bd, proper_names_threshold, n, ndoc_min, sample_path
from _1_2settingparameters import t0, infos_doc, doc_selected, sig
import time
from tqdm import tqdm

# The lists of every useful information are created. There is: the dictionary, the number of total
# occurences, and the number of occurences with capital letters.
dico , tot_occ , cap_occ = {} , {} , {}

t1 = time.time()

# The algorithm goes through the documents a first time to complete those first three lists.
print('\n'+'The dictionary is created.')
for i in tqdm(range(len(doc_bd))) :
    for wrd in doc_bd[i][1] :
        l_wrd = wrd.lower()
        if l_wrd not in dico :
            dico[l_wrd] = len(dico)
            tot_occ[l_wrd] = doc_bd[i][1][wrd]
            if wrd[:1].isupper() :
                cap_occ[l_wrd] = doc_bd[i][1][wrd]
            else :
                cap_occ[l_wrd] = 0
        elif l_wrd in dico :
            tot_occ[l_wrd] += doc_bd[i][1][wrd]
            if wrd[:1].isupper() :
                cap_occ[l_wrd] += doc_bd[i][1][wrd]

ndoc_max = int(len(doc_bd)*(n/100))
len_dicotot = len(dico)

# The algorithm goes through the dictionary to complete the list of the document occurences.
doc_occ , i = {} , 0
for l_wrd in dico :
    doc_occ[l_wrd] = 0
for wrd in dico :
    for doc in doc_bd :
        if wrd in doc[1] :
            doc_occ[wrd] += 1
    i += 1

# Now the parameters that were chosen in the setting_parameters file are applied. That is: the 
# threshold for too frequent words, for words not frequent enough, and for words that are proper
# words.
list_pop = {}
proper_names_count = 0

# txt documents are created to keep track of the words that are deleted because of the filtration
# parameters. With every word deleted is written the number of total occurences and, depending of
# the reason of the deleted word, the number of document occurences or the number of occurences
# with a capital letter.
f = open(sample_path+"maxi_words"+str(n)+".txt",'w+',encoding='utf-8')
g = open(sample_path+"mini_words.txt",'w+',encoding='utf-8')
h = open(sample_path+"proper_names.txt",'w+',encoding='utf-8')
for wrd in dico :
    i = wrd
    if (doc_occ[i] > ndoc_max) or (doc_occ[i] < ndoc_min) :
        list_pop[wrd] = True
    elif (cap_occ[i]/tot_occ[i] > (proper_names_threshold/100)) and tot_occ[i]>1 :
        list_pop[wrd] = True
        proper_names_count += 1
    if doc_occ[i] > ndoc_max :
        f.write(wrd+'\n'+str(tot_occ[i])+'\n'+str(doc_occ[i])+'\n')
    if doc_occ[i] < ndoc_min :
        g.write(wrd+'\n'+str(tot_occ[i])+'\n'+str(doc_occ[i])+'\n')
    if (cap_occ[i]/tot_occ[i] > (proper_names_threshold/100)) and tot_occ[i]>1 :
        h.write(wrd+'\n'+str(tot_occ[i])+'\n'+str(cap_occ[i])+'\n')
f.close()
g.close()
h.close()
for wrd in list_pop :
    word = dico.pop(wrd)
    tot_occ.pop(wrd)
    doc_occ.pop(wrd) 

# Now the filtered dictionary along with the numbers of total occurences, and the number of 
# documents occurences.
f = open(sample_path+'dico_filtered.txt',"w+",encoding="utf-8")
for wrd in dico :
    f.write(wrd+'\n'+str(tot_occ[wrd])+'\n'+str(doc_occ[wrd])+'\n')
f.close()

# Now everything is printed in the console and saved in the sample folder
t2 = time.time()
print('\n'+'Length of the non-filtered dictionary :',len_dicotot)
print('Length of the filtered dictionary :',len(dico))
print('The dictionary took',(t2-t1)//60,'minutes and',round((t2-t1)%60,1),'seconds to be made and saved.')

f = open(sample_path+"Console Python.txt",'r',encoding='utf-8')
lines = f.readlines()
f.close()
f = open(sample_path+"Console Python.txt",'w+',encoding='utf-8')
for line in lines :
    f.write(line)
f.write('\n\nThe dictionary is created.')
f.write('\nLength of the non-filtered dictionary : '+str(len_dicotot))
f.write('\nLength of the filtered dictionary : '+str(len(dico)))
f.write('\nThe dictionary took '+str((t2-t1)//60)+' minutes and '+str(round((t2-t1)%60,1))+' seconds to be made and saved.')
f.close()




