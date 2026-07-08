# -*- coding: utf-8 -*-
"""
Created on Fri May  8 11:39:23 2026

@author: jeann2e
"""

from pathlib import Path
import re
import time
import numpy as np

# In the code, a lot of the parts will be timed
t0 = time.time()
t1 = time.time()

# The documents, already processed, are in a folder called 'corpus1'. The files are named with 
# the code of the texts and contain a string of characters corresponding to th characters of the
# documents
p = Path('corpus1')
paths = list(p.glob('**/*.txt'))

# This is the process of the tokenization of the documents. The text is split at every space and
# every punctuation, and then every superfluous character, including the numerals, is removed.
# Every token is kept in a list of lists.
documents = [0 for i in range(len(paths))]
for i in range(len(paths)) :
    with open(paths[i], 'r' , encoding='utf-8') as file :
        lines1 = file.readlines()
        lines2 = []
        for line1 in lines1[1:] :
            line2 = re.split('''<|'|’|ʼ|ʾ|′|:|·|ˊ|ˈ|ꞌ|‘|ʿ|‵|ˋ|>|´| ''',line1)
            for word2 in line2 :
                lines2.append(word2)
        lines3 = {}
        for wrd in lines2 :
            new_wrd = wrd.strip('''“”&~º·"#ª'{([-|`_\^)…]—=}+°,?;.:/!§*1234567890''')
            if len(new_wrd)>0 :
                if new_wrd in lines3 :
                    lines3[new_wrd] += 1
                else :
                    lines3[new_wrd] = 1
        documents[i] = [ str(paths[i])[8:-4] , lines3 ]

t2 = time.time()

# Everything is printed
print('\n'+"The words in the documents have been tokenized.")
print("It took",round(t2-t1,2),"seconds.")
token_time = round(t2-t1,2)

# The informations of all of the documents, in a txt document, are retrieved because, for example,
# the year of each text is needed because of the histogram and the Getis-Ord matrix.
infos_doc = []
for i in range(len(paths)) :
    with open(paths[i],'r',encoding='utf-8') as file :
        lines = file.readlines()
        if str(paths[i])[12:-13] == 'POS' :
            year = int(str(paths[i])[16:-8])
        else :
            year = int(str(paths[i])[13:-8])
        info_doc = [ str(paths[i])[8:-4] , 0 , 0 , year , 0 , 0 , 0 , 0 , 0 ]
    infos_doc.append(info_doc)
infos_doc = np.array(infos_doc)

f = open('infos_doc.txt','w+',encoding='utf-8')
for info in infos_doc :
    for truc in info :
        f.write(str(truc)+'\n')
f.close()
