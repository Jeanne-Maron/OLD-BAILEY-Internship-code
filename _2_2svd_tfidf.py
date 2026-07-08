# -*- coding: utf-8 -*-
"""
Created on Wed May 13 17:29:24 2026

@author: jeann2e
"""

# To do the SVD of the right sample, the file '_2_1extractingsample.py' has to be modified
# accordingly.

# Theses are parameters that can be modified to plot the graphs. The first parameter is a Boolean
# that says wether the graphs will be plotted or not. limit1 and limit2 are limits corresponding
# to the graphs of the simple document weights and the top word weights. They are used so that
# the values too close (inferior in absolute value to the limit given) are not plotted. This helps
# clarify what is seen. The number of significant words tells how many of them will be saved in 
# the sample folder.
plot = True
# Limits commonly used : limit1 = 0 and limit2 = 0.5
limit1 , limit2 = 0 , 0.5
n_sigwords = 900

### Doing the SVD thanks to the NumPy library
from _2_1extractingsample import sample_path, infos_doc, dico, doc_selected, len_selected, matrix_doc
import numpy as np
import os
import matplotlib.pyplot as plt
U , s , Vh = np.linalg.svd( matrix_doc , full_matrices=True )
V = np.transpose( Vh )
print('\nSVD TFIDF done.')


### Plotting and saving the plots and results

# The folder is created
SVD_TFIDF_path = sample_path+"SVD_TFIDF"
if not os.path.exists(SVD_TFIDF_path):
    os.makedirs(SVD_TFIDF_path)
SVD_TFIDF_path = SVD_TFIDF_path+'\\'

# Preparing the plots

# The information of the documents and the SVD is retrieved
list_code = list(infos_doc[:,0])
list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
list_y1 = list( U[:,0] )
list_y2 = list( U[:,1] )
list_y3 = list( U[:,2] )
list_y4 = list( U[:,3] )

# The significant words are retrieved
sig_wrds_pos = []
sig_wrds_neg = []
for i in range(4):
    list_emax , list_emin , len_list = list(V[:,i]) , list(V[:,i]) , len(list(V[:,i]))
    dico_max , dico_min = [ i for i in range(len(dico)) ] , [ i for i in range(len(dico)) ]
    pos_words , neg_words = [] , []
    sorted_max = False
    while sorted_max == False :
        sorted_max = True
        for j in range(len_list-1) :
            if list_emax[j] < list_emax[j+1] :
                list_emax[j] , list_emax[j+1] = list_emax[j+1] , list_emax[j]
                dico_max[j] , dico_max[j+1] = dico_max[j+1] , dico_max[j]
                sorted_max = False
    sorted_min = False
    while sorted_min == False :
        sorted_min = True
        for j in range(len_list-1) :
            if list_emin[j] > list_emin[j+1] :
                list_emin[j] , list_emin[j+1] = list_emin[j+1] , list_emin[j]
                dico_min[j] , dico_min[j+1] = dico_min[j+1] , dico_min[j]
                sorted_min = False
    for j in range(n_sigwords) :
        pos_words.append([dico_max[j] , list_emax[j]])
        neg_words.append([dico_min[j] , list_emin[j]])
    sig_wrds_pos.append(pos_words)
    sig_wrds_neg.append(neg_words)

# The significant words are saved in the right folder
for i in range(4) :
    f = open(SVD_TFIDF_path+"sigwords_GO_comp"+str(i+1)+"_withvalues.txt","w+",encoding="utf-8")
    g = open(SVD_TFIDF_path+"sigwords_GO_comp"+str(i+1)+".txt","w+",encoding="utf-8")
    f.write("For component "+str(i+1)+' :\n')
    f.write("\nMost positive words :\n")
    g.write("For component "+str(i+1)+' :\n')
    g.write("\nMost positive words :\n")
    for inf in sig_wrds_pos[i] :
        f.write(dico[inf[0]]+' ('+str(round(inf[1],3))+')\n')
        g.write(dico[inf[0]]+'\n')
    f.write("\nMost negative words :"+'\n')
    g.write("\nMost negative words :"+'\n')
    for inf in sig_wrds_neg[i] :
        f.write(dico[inf[0]]+' ('+str(round(inf[1],3))+')\n')
        g.write(dico[inf[0]]+'\n')
    f.close()
    g.close()


### Plotting the results

# Here, plot_lengths is commented because it is only used to check wether the axes of variations
# are dependant of the lengths of the texts.
def plot_all(limit1 , limit2):
    plot_dw1D(limit1)
    plot_dw2D()
    plot_dw2Dp()
    plot_ww(limit2)
    #plot_lengths()

# This is used to separate the positive values from the negative ones, so they can be plotted with
# different colors
def separate( list_x , list_y ):
    list_xpos , list_xneg = [] , []
    list_ypos , list_yneg = [] , []
    for i in range(len(list_y)) :
        if list_y[i] > 0 :
            list_xpos.append(list_x[i])
            list_ypos.append(list_y[i])
        if list_y[i] < 0 :
            list_xneg.append(list_x[i])
            list_yneg.append(list_y[i])
    return list_xpos , list_xneg , list_ypos , list_yneg

# This is used to remove the values too close too zero like explained previously.
def remove_zeros( list_xb , list_y , limit ):
    list_pop = []
    for i in range(len(list_y)) :
        if abs(list_y[i]) < limit :
            list_pop.append(i)
    for i in reversed(list_pop):
        list_y.pop(i)
        list_xb.pop(i)
    return list_xb , list_y

# This is used to plot the positions of the documents along the four main axes of variation. The 
# year of each text is indicated by the x-axis.
def plot_dw1D(limit):    
    plt.grid()
    list_xpos , list_xneg , list_ypos , list_yneg = separate(list_x,list_y1)
    list_xpos , list_ypos = remove_zeros( list_xpos , list_ypos , limit )
    list_xneg , list_yneg = remove_zeros( list_xneg , list_yneg , limit )
    plt.plot( list_xpos , list_ypos , color='darkgreen' , marker='+' , linewidth=0 )
    plt.plot( list_xneg , list_yneg , color='darkgoldenrod' , marker='+' , linewidth=0 )
    plt.xlabel("Years")
    plt.title('Weights of the documents for the first component')
    plt.savefig(SVD_TFIDF_path+'1st component.png')
    plt.show()
    
    plt.grid()
    list_xpos , list_xneg , list_ypos , list_yneg = separate(list_x,list_y2)
    list_xpos , list_ypos = remove_zeros( list_xpos , list_ypos , limit )
    list_xneg , list_yneg = remove_zeros( list_xneg , list_yneg , limit )
    plt.plot( list_xpos , list_ypos , color='forestgreen' , marker='+' , linewidth=0 )
    plt.plot( list_xneg , list_yneg , color='goldenrod' , marker='+' , linewidth=0 )
    plt.xlabel("Years")
    plt.title('Weights of the documents for the second component')
    plt.savefig(SVD_TFIDF_path+'2nd component.png')
    plt.show()
    
    plt.grid()
    list_xpos , list_xneg , list_ypos , list_yneg = separate(list_x,list_y3)
    list_xpos , list_ypos = remove_zeros( list_xpos , list_ypos , limit )
    list_xneg , list_yneg = remove_zeros( list_xneg , list_yneg , limit )
    plt.plot( list_xpos , list_ypos , color='limegreen' , marker='+' , linewidth=0 )
    plt.plot( list_xneg , list_yneg , color='gold' , marker='+' , linewidth=0 )
    plt.xlabel("Years")
    plt.title('Weights of the documents for the third component')
    plt.savefig(SVD_TFIDF_path+'3rd component.png')
    plt.show()
    
    plt.grid()
    list_xpos , list_xneg , list_ypos , list_yneg = separate(list_x,list_y4)
    list_xpos , list_ypos = remove_zeros( list_xpos , list_ypos , limit )
    list_xneg , list_yneg = remove_zeros( list_xneg , list_yneg , limit )
    plt.plot( list_xpos , list_ypos , color='lightgreen' , marker='+' , linewidth=0 )
    plt.plot( list_xneg , list_yneg , color='yellow' , marker='+' , linewidth=0 )
    plt.xlabel("Years")
    plt.title('Weights of the documents for the fourth component')
    plt.savefig(SVD_TFIDF_path+'4th component.png')
    plt.show()

# This is used to plot the positions of the documents for every two axes out of the first three
# main axes of variation. The year of each text is indicated by color.
def plot_dw2D():
    plt.scatter( list_y1 , list_y2 , c=list_x , cmap='plasma' )
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.title('Weights of the documents for the 1st and 2nd components')
    plt.savefig(SVD_TFIDF_path+'1st and 2nd components.png')
    plt.colorbar()
    plt.show()
    
    plt.scatter( list_y1 , list_y3 , c=list_x , cmap='plasma' )
    plt.xlabel('Component 1')
    plt.ylabel('Component 3')
    plt.title('Weights of the documents for the 1st and 3rd components')
    plt.savefig(SVD_TFIDF_path+'1st and 3rd components.png')
    plt.colorbar()
    plt.show()
    
    plt.scatter( list_y2 , list_y3 , c=list_x , cmap='plasma' )
    plt.xlabel('Component 2')
    plt.ylabel('Component 3')
    plt.title('Weights of the documents for the 2nd and 3rd components')
    plt.savefig(SVD_TFIDF_path+'2nd and 3rd components.png')
    plt.colorbar()
    plt.show()

# This is used to plot the positions of the documents for every two axes out of the first three
# main axes of variation and the fourth one. The year of each text is indicated by color.
def plot_dw2Dp():
    plt.scatter( list_y1 , list_y4 , c=list_x , cmap='plasma' )
    plt.xlabel('Component 1')
    plt.ylabel('Component 4')
    plt.title('Weights of the documents for the 1st and 4th components')
    plt.savefig(SVD_TFIDF_path+'1st and 4th components.png')
    plt.colorbar()
    plt.show()
    
    plt.scatter( list_y2 , list_y4 , c=list_x , cmap='plasma' )
    plt.xlabel('Component 2')
    plt.ylabel('Component 4')
    plt.title('Weights of the documents for the 2nd and 4th components')
    plt.savefig(SVD_TFIDF_path+'2nd and 4th components.png')
    plt.colorbar()
    plt.show()
    
    plt.scatter( list_y3 , list_y4 , c=list_x , cmap='plasma' )
    plt.xlabel('Component 3')
    plt.ylabel('Component 4')
    plt.title('Weights of the documents for the 3rd and 4th components')
    plt.savefig(SVD_TFIDF_path+'3rd and 4th components.png')
    plt.colorbar()
    plt.show()

# This is used to plot the GO z-score of the top five significant words, positive and negative, of
# the four main axes of variation. The year is indicated by the x-axis.
def plot_ww(limit) :
    plt.rcParams['figure.max_open_warning'] = 10000
    for i in range(4):
        plt.figure(figsize=(10,5))
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_pos[i][4][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_pos[i][4][0]] , color='lightsalmon', marker='+' , linewidth=0)
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_neg[i][4][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_neg[i][4][0]] , color='lightskyblue', marker='+' , linewidth=0)
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_pos[i][3][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_pos[i][3][0]] , color='salmon', marker='+' , linewidth=0)
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_neg[i][3][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_neg[i][3][0]] , color='deepskyblue', marker='+' , linewidth=0)
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_pos[i][2][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_pos[i][2][0]] , color='tomato', marker='+' , linewidth=0)
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_neg[i][2][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_neg[i][2][0]] , color='dodgerblue', marker='+' , linewidth=0)
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_pos[i][1][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_pos[i][1][0]] , color='red', marker='+' , linewidth=0)
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_neg[i][1][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_neg[i][1][0]] , color='blue', marker='+' , linewidth=0)
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_pos[i][0][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_pos[i][0][0]] , color='darkred', marker='+' , linewidth=0)
       
        list_x = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
        list_xbis , list_y = remove_zeros(list_x , list(matrix_doc[:,sig_wrds_neg[i][0][0]]) , limit )
        plt.plot(list_xbis, list_y , label=dico[sig_wrds_neg[i][0][0]] , color='darkblue', marker='+' , linewidth=0)
       
        plt.legend()
        plt.title("Ten most significative words of component "+str(i+1))
        plt.xlabel("Year")
        plt.ylabel("Time Frequencies - Inversed Document Frequencies")
        plt.savefig(SVD_TFIDF_path+'Ten most significatives words of component '+str(i+1)+'.png')
        plt.show()

# This is used to plot the absolute positions of the documents along the four main axes of 
# variation. The length of each text is indicated by the x-axis.
def plot_lengths() :
    new_y1 = [ abs(val) for val in list_y1 ]
    new_y2 = [ abs(val) for val in list_y2 ]
    new_y3 = [ abs(val) for val in list_y3 ]
    new_y4 = [ abs(val) for val in list_y4 ]
    plt.plot( len_selected , new_y1 , label='Comp 1' , color='blue' , marker='.' , linewidth=0 )
    plt.title('Absolute values of the documents for component 1')
    plt.xlabel('Length of the document')
    plt.ylabel('Aboslute value on the component')
    plt.savefig(SVD_TFIDF_path+'Abs values, component 1.png')
    plt.show()
    plt.plot( len_selected , new_y2 , label='Comp 2' , color='orange' , marker='.' , linewidth=0 )
    plt.title('Absolute values of the documents for component 2')
    plt.xlabel('Length of the document')
    plt.ylabel('Aboslute value on the component')
    plt.savefig(SVD_TFIDF_path+'Abs values, component 2.png')
    plt.show()
    plt.plot( len_selected , new_y3 , label='Comp 3' , color='green' , marker='.' , linewidth=0 )
    plt.title('Absolute values of the documents for component 3')
    plt.xlabel('Length of the document')
    plt.ylabel('Aboslute value on the component')
    plt.savefig(SVD_TFIDF_path+'Abs values, component 3.png')
    plt.show()
    plt.plot( len_selected , new_y4 , label='Comp 4' , color='red' , marker='.' , linewidth=0 )
    plt.title('Absolute values of the documents for component 4')
    plt.xlabel('Length of the document')
    plt.ylabel('Aboslute value on the component')
    plt.savefig(SVD_TFIDF_path+'Abs values, component 4.png')
    plt.show()

# This is used to plot and save all of the graphs
if plot :
    plot_all(limit1,limit2)