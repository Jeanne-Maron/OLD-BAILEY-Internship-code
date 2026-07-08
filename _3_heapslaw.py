# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 11:33:03 2026

@author: jeann2e
"""

# Verifying Heap's law in a given set of documents - OLD-BAILEY

# Importing the libraries and creating useful lists
from pathlib import Path
import re
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy.stats import linregress
dico , count = {} , 0
list_x , list_y = [] , []

# The right documents to verify Zipf's law on are retrieved
p = Path('corpus1')
paths = list(p.glob('**/*.txt'))

# The program goes through all of the documents again
for i in tqdm(range(len(paths))) :
    with open(paths[i], 'r' , encoding='utf-8') as file :
        lines1 = file.readlines()
        lines2 = []
        for line1 in lines1[1:] :
            line2 = re.split('''<|'|’|ʼ|ʾ|′|:|·|ˊ|ˈ|ꞌ|‘|ʿ|‵|ˋ|>|´| ''',line1)
            for word2 in line2 :
                lines2.append(word2)
        for wrd in lines2 :
            new_wrd = wrd.strip('''“”&~º·"#ª'{([-|`_\^)…]—=}+°,?;.:/!§*1234567890''')
            if len(new_wrd)>0 :
                count += 1
                wrd2 = new_wrd.lower()
                if wrd2 not in dico :
                    dico[wrd2] = 1
                elif wrd2 in dico :
                    dico[wrd2] += 1
                if count%100 == 0 :
                    list_x.append(count)
                    list_y.append(len(dico))

# Plotting Heap's law without linear regress
print("Now Heap's law will be plotted.")
plt.plot( list_x , list_y , color='deeppink' )
plt.xlabel('Number of tokens')
plt.ylabel('Number of types')
plt.title("Heap's law")
plt.show()

# Doing a linear regress to verify Heap's law
Results = linregress(np.log(np.array(list_x)),np.log(np.array(list_y)))
beta , K , r = Results.slope , np.exp(Results.intercept) , Results.rvalue
rval = 'r² = '+str(round(r**2,2))

# Plotting Heap's law with linear regress
plt.plot( list_x , list_y , color='deeppink' , label='Data' , marker=',' , markersize=2 , linewidth=0 )
plt.plot( list_x , K* (np.array(list_x))**beta , label='Linear regression, y = '+str(round(K,2))+' x^'+str(round(beta,2)) , color='palegreen')
plt.xlabel('Number of tokens')
plt.ylabel('Number of types')
plt.title("Heap's law with linear regression ("+rval+")")
plt.legend()
plt.show()





















