# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:40:59 2026

@author: jeann2e
"""

# For this file to correctly function, it is important to change a few things in 
# the files _2_2svd_tfidf.py and _2_2svd_go.py. First, the n_sigwords parameter
# has to be set at 900, and, to not replot everything, the Boolean plot can be set
# to False.

# This file compares the lists of significant words for one given axis of the 
# TFIDF matrix and one given axis of the Getis-Ord matrix. It compares the
# similarity of the lists depending on the lengths taken. This allows us to see if
# axes that seem similar from one matrix to another are really caused by similar
# reasons or not.

# Importing the libraries and the previous results
import _2_2svd_tfidf as tfidf 
import _2_2svd_go as go
import matplotlib.pyplot as plt
import os

# Components to compare :
c_tfidf = 3
c_go = 2
numbers = [20*i for i in range(1,46)]

# Creating the folder
path_here = tfidf.sample_path+"Comp_JaccardI"
if not os.path.exists(path_here):
    os.makedirs(path_here)
path_here = path_here+'\\'

# Defining the Jaccard Index to compare the lists
def jaccard_index(list1 , list2):
    len_overlap , len_union = 0 , 0
    for word1 in list1 :
        for word2 in list2 :
            if word1 == word2 :
                len_overlap += 1
        if word1 not in list2 :
            len_union += 1
    for word2 in list2 :
        if word2 not in list1 :
            len_union += 1
    len_union += len_overlap
    return round(len_overlap / len_union,3)

# Defining another Index (simpler) to compare the lists
def new_index(list1 , list2):
    len_overlap , len_1 = 0 , len(list1)
    for word1 in list1 :
        for word2 in list2 :
            if word1 == word2 :
                len_overlap += 1
    return round(len_overlap / len_1,3)

# Retrieving the lists of significant words
pos_c_tfidf , neg_c_tfidf = tfidf.sig_wrds_pos[c_tfidf-1] , tfidf.sig_wrds_neg[c_tfidf-1]
pos_c_go , neg_c_go = go.sig_wrds_pos[c_go-1] , go.sig_wrds_neg[c_go-1]
for i in range(len(pos_c_go)) :
    pos_c_tfidf[i] , pos_c_go[i] = pos_c_tfidf[i][0] , pos_c_go[i][0]
    neg_c_tfidf[i] , neg_c_go[i] = neg_c_tfidf[i][0] , neg_c_go[i][0]

# Calculation of the Jaccard Indexes depending on the lengths
l_pp , l_nn , l_pn , l_np = [] , [] , [] , []
f = open(path_here+'comp_tfidf'+str(c_tfidf)+'_go'+str(c_go)+'.txt','w+',encoding='utf-8')
for number in numbers :
    pos_pos = jaccard_index(pos_c_tfidf[:number], pos_c_go[:number])
    neg_neg = jaccard_index(neg_c_tfidf[:number], neg_c_go[:number])
    pos_neg = jaccard_index(pos_c_tfidf[:number], neg_c_go[:number])
    neg_pos = jaccard_index(neg_c_tfidf[:number], pos_c_go[:number])
    l_pp.append(pos_pos)
    l_nn.append(neg_neg)
    l_pn.append(pos_neg)
    l_np.append(neg_pos)
    print('\nWith lists of',number,'words :')
    print('TFIDF',c_tfidf,'pos and GO',c_go,'pos :',pos_pos)
    print('TFIDF',c_tfidf,'neg and GO',c_go,'neg :',neg_neg)
    print('TFIDF',c_tfidf,'pos and GO',c_go,'neg :',pos_neg)
    print('TFIDF',c_tfidf,'neg and GO',c_go,'pos :',neg_pos)
    f.write('\n\nWith lists of '+str(number)+' words :')
    f.write('\nTFIDF '+str(c_tfidf)+' pos and GO '+str(c_go)+' pos : '+str(pos_pos))
    f.write('\nTFIDF '+str(c_tfidf)+' neg and GO '+str(c_go)+' neg : '+str(neg_neg))
    f.write('\nTFIDF '+str(c_tfidf)+' pos and GO '+str(c_go)+' neg : '+str(pos_neg))
    f.write('\nTFIDF '+str(c_tfidf)+' neg and GO '+str(c_go)+' pos : '+str(neg_pos))
f.close()

# Plotting and saving the Jaccard Indexes
plt.plot(numbers,l_pp,color='deeppink',label='pos_pos')
plt.plot(numbers,l_nn,color='magenta',label='neg_neg')
plt.plot(numbers,l_pn,color='lime',label='pos_neg')
plt.plot(numbers,l_np,color='mediumspringgreen',label='neg_pos')
plt.title('Evolution of the Jaccard Indexes for the TFIDF '+str(c_tfidf)+' and the GO '+str(c_go))
plt.legend()
plt.xlabel('Length of the lists of words compared')
plt.ylabel('Jaccard Index')
plt.ylim(0,1)
plt.grid()
plt.savefig(path_here+'comp_tfidf'+str(c_tfidf)+'_go'+str(c_go)+'.png')
plt.show()

# Calculation of the new Indexes depending on the lengths
l_pp , l_nn , l_pn , l_np = [] , [] , [] , []
f = open(path_here+'comp_tfidf'+str(c_tfidf)+'_go'+str(c_go)+'.txt','w+',encoding='utf-8')
for number in numbers :
    pos_pos = new_index(pos_c_tfidf[:number], pos_c_go[:number])
    neg_neg = new_index(neg_c_tfidf[:number], neg_c_go[:number])
    pos_neg = new_index(pos_c_tfidf[:number], neg_c_go[:number])
    neg_pos = new_index(neg_c_tfidf[:number], pos_c_go[:number])
    l_pp.append(pos_pos)
    l_nn.append(neg_neg)
    l_pn.append(pos_neg)
    l_np.append(neg_pos)
    print('\nWith lists of',number,'words :')
    print('TFIDF',c_tfidf,'pos and GO',c_go,'pos :',pos_pos)
    print('TFIDF',c_tfidf,'neg and GO',c_go,'neg :',neg_neg)
    print('TFIDF',c_tfidf,'pos and GO',c_go,'neg :',pos_neg)
    print('TFIDF',c_tfidf,'neg and GO',c_go,'pos :',neg_pos)
    f.write('\n\nWith lists of '+str(number)+' words :')
    f.write('\nTFIDF '+str(c_tfidf)+' pos and GO '+str(c_go)+' pos : '+str(pos_pos))
    f.write('\nTFIDF '+str(c_tfidf)+' neg and GO '+str(c_go)+' neg : '+str(neg_neg))
    f.write('\nTFIDF '+str(c_tfidf)+' pos and GO '+str(c_go)+' neg : '+str(pos_neg))
    f.write('\nTFIDF '+str(c_tfidf)+' neg and GO '+str(c_go)+' pos : '+str(neg_pos))
f.close()

# Plotting and saving the new Indexes
plt.plot(numbers,l_pp,color='deeppink',label='pos_pos')
plt.plot(numbers,l_nn,color='magenta',label='neg_neg')
plt.plot(numbers,l_pn,color='lime',label='pos_neg')
plt.plot(numbers,l_np,color='mediumspringgreen',label='neg_pos')
plt.title('Evolution of the overlapping for the TFIDF '+str(c_tfidf)+' and the GO '+str(c_go))
plt.legend()
plt.xlabel('Length of the lists of words compared')
plt.ylabel('Relative overlapping')
plt.ylim(0,1)
plt.grid()
plt.savefig(path_here+'new_comp_tfidf'+str(c_tfidf)+'_go'+str(c_go)+'.png')
plt.show()







