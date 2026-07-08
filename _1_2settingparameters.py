# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:50:26 2026

@author: jeann2e
"""

### Setting parameters :
# Here is the part where the parameters of both matrices wil be chosen.

# The name of the sample. The files associated with the sample will be in a folder with this name.
sample_name = 'test'    

# These parameters are the ones used to create the lexicon used in the analyses. The first one is 
# to remove the proper names, meaning the words that begin with a capital letter more than n% of
# the time. The second one is to remove the words present in more than n% of the documents. The 
# last one is to remove the words in less than n documents.
proper_names_threshold = 80
n = 50
ndoc_min = 150

# This is the parameter used as the standard deviation of the gaussian used as the neighbouring 
# function for the Getis-Ord matrix.
sig = 5

### Printing the parameters :

print('\n'+'Parameters of the dictionary :')
print('\t'+'Proper names threshold :',proper_names_threshold)
print('\t'+'Minimum of documents :',ndoc_min)
print('\t'+'Percentage maximum :',n,'%')

print('\n'+'''Criteria for the neighborhood in Getis Ord's zscore :''',sig)

print('\n'+'_________________________________________________________________')

### Beginning the processus

# This has to be changed, so the folder where the sample will be placed is chosen. Here, the folder
# of the sample is created.
import os
sample_path = 'C:\\Users\\jeann\\Documents\\ENS\\masters_internship\\old-bailey\\_sample_'+sample_name
if not os.path.exists(sample_path):
    os.makedirs(sample_path)
sample_path = sample_path+'\\'

# Here, I create of txt document so I can keep in the sample folder the parameters used to create
# the lexicon and the matrices.
f = open(sample_path+"Console Python.txt",'w+',encoding='utf-8')
f.write('\n\nParameters of the dictionary :')
f.write('\n\tProper names threshold : '+str(proper_names_threshold))
f.write('\n\tMinimum of documents : '+str(ndoc_min))
f.write('\n\tPercentage maximum : '+str(n)+'%')
f.write('''\n\nCriteria for the neighborhood in Getis Ord's zscore : '''+str(sig))
f.write('\n\n_____________________________________________________________________')
f.close()

# Here, the tokenization done is imported.
from _1tokenization import documents, infos_doc, t0, token_time
import time
from tqdm import tqdm
import matplotlib.pyplot as plt


# Now, every parameter written before is applied.
doc_selected = list(infos_doc[:,0])
list_code = list(infos_doc[:,0])

# Now we will create a list containing all the tokens of all the documents selected 
# This is possible because the documents have already been tokenized before.
t1 = time.time()
doc_bd , doc_done = [] , []

# Here, we keep the names and lengths of all the documents selected in the sample folder
f = open(sample_path+"doc_selected.txt",'w+',encoding='utf-8')
g = open(sample_path+"len_documents.txt",'w+',encoding='utf-8')
for i in tqdm(range(len(documents))) :
    if documents[i][0] in doc_selected :
        code = documents[i][0]
        f.write(code+'\n')
        g.write(str(len(documents[i][1]))+'\n')
        doc_bd.append([ code , {} ])
        doc_done.append(code)
        for wrd in documents[i][1]:
            pos_doc = doc_done.index(code)
            doc_bd[pos_doc][1][wrd] = documents[i][1][wrd]
f.close()
g.close()

t2 = time.time()


# Printing everything that happened during the filtration process.
print('\n'+'Original number of documents :',len(documents))
print("Number of documents after processing :",len(doc_bd))
print("The selection of the documents took",round(t2-t1,2),"seconds.")



# Now, the histograms characterizing the sample. Three histograms will be plotted : the 
# repartition in years, in lengths, and in tokens.

# Here the lists for plotting the graphs are created
list_years = [ int(infos_doc[list_code.index(doc[0]),3]) for doc in doc_bd ]
list_NoWords = [ sum([doc[1][wrd] for wrd in doc[1]]) for doc in doc_bd ]

# The repartition of years is plotted
edges_year = [1720+i*10 for i in range(0,21)]
plt.hist( list_years , bins=edges_year, edgecolor='black', color='goldenrod' )
plt.title('Repartition across the years')
plt.xlabel('Year')
plt.ylabel('Number of documents')
plt.savefig(sample_path+'Repartition of years.png')
plt.show()

# The repartition of lengths is plotted
max_words = max(list_NoWords)
edges_words = [ i*10000 for i in range(0,(max_words//10000)+1) ]
plt.hist( list_NoWords , bins=edges_words, edgecolor='black', color='cornflowerblue' )
plt.title('Repartition of the number of tokens')
plt.xlabel('Number of tokens')
plt.ylabel('Number of documents')
plt.savefig(sample_path+'Repartition of lengths.png')
plt.show()

# The repartition of tokens is plotted
yearmax , yearmin = 1920 , 1720
size_bin = 10
n_bins = (yearmax - yearmin)//size_bin
edges_year = [ yearmin+(i*size_bin) for i in range(0,n_bins+1) ]
list_tokens = [ 0 for i in range(len(edges_year)-1) ]
list_code = list(infos_doc[:,0])
len_selected = []
with open(sample_path+"len_documents.txt",'r',encoding='utf-8') as file:
    for line in file:
        len_selected.append(line.strip('\n'))
for i in range(len(doc_selected)) :
    code = doc_selected[i]
    pos = list_code.index(code)
    year , length = int(infos_doc[pos,3]) , int(len_selected[i])
    bin_number = (year - yearmin)//size_bin
    list_tokens[bin_number] += length
list_tokens.append(list_tokens[-1])
plt.plot( edges_year , list_tokens , color='mediumseagreen' , drawstyle='steps-post' )
plt.title('Number of tokens depending on the year')
plt.xlabel('Year')
plt.ylabel('Total number of tokens')
plt.grid()
plt.savefig(sample_path+'Repartition of tokens.png')
plt.show()

# Here, every information that could be useful is written in a txt document to be kept
f = open(sample_path+"Console Python.txt",'r',encoding='utf-8')
lines = f.readlines()
f.close()
f = open(sample_path+"Console Python.txt",'w+',encoding='utf-8')
for line in lines :
    f.write(line)
f.write('\n\nThe words in the documents have been tokenized.')
f.write('\nIt took '+str(token_time)+' seconds.')
f.write('\n\nOriginal number of documents : '+str(len(documents)))
f.write('\nNumber of documents after processing : '+str(len(doc_bd)))
f.write('\nThe selection of the documents took '+str(round(t2-t1,2))+" seconds.")
f.close()






