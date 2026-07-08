# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:32:39 2026

@author: jeann2e
"""

# Verifying Zipf's law in a given set of documents - OLD-BAILEY

# Importing the libraries and creating useful lists
from pathlib import Path
import re
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy.stats import linregress
dico = {}

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
                new_wrd = new_wrd.lower()
                if new_wrd in dico :
                    dico[new_wrd] += 1
                else :
                    dico[new_wrd] = 1

# Plotting Zipf's law without linear regress
occurence = []
for wrd in dico :
    occurence.append(dico[wrd])
occurence.sort(reverse=True)
list_x = np.array([ i for i in range(1,len(occurence)+1) ])
plt.loglog( list_x , np.array(occurence)/sum(occurence) , color='maroon' )
plt.xlabel("Rank of the word")
plt.ylabel("Frequency of the word")
plt.title("Zipf's law")
plt.show()

# Doing a linear regress to verify Zipf's law
print("Now Zipf's law will be verified with a linear regression.")
Results = linregress(np.log(list_x) , np.log(np.array(occurence)/sum(occurence)) )
a , b , r = Results.slope , Results.intercept , Results.rvalue
rval = 'r² = '+str(round(r**2,2))

# Plotting Zipf's law with linear regress
plt.loglog( list_x , np.array(occurence)/sum(occurence) , color='maroon' , label='Data' , marker=',' , markersize=2 , linewidth=0 )
plt.loglog( list_x , np.exp(np.array([ a*i+b for i in np.log(list_x) ])) , label='Linear regression, y = '+str(round(a,2))+' x - '+str(round(-b,2)) , color='darkviolet' )
plt.xlabel("Rank of the word")
plt.ylabel("Frequency of the word")
plt.legend()
plt.title("Zipf's law with linear regression ("+rval+")")
plt.show()