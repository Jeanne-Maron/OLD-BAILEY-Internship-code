# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 10:17:59 2026

@author: jeann
"""

# This file is to apply the UMAP to a sample. It does the SVD of the matrix chosen and then
# applies the SVD for every set of parameters given.

# First the matrix used has to be chosen
# 1 for TFIDF, 2 for GO
which_one = 2

# Then we chose the different sets of parameters. The first set of parameters corresponds to 
# the first values of each list, and so on. The first list is for how many components of the
# SVD will be taken into account for the UMAP. The second and third lists are parameters for
# the UMAP algorithm. They have to be adjusted so that the results are the best possible.
if which_one == 1 :
    list_ncomp = [3 for i in range(5)]
    list_neighbours = [150 for i in range(5)]
    list_multiplicator = [1,1.5,2,3,5]
if which_one == 2 :
    list_ncomp = [3 for i in range(10)]
    list_neighbours = [5,10,15,20,25,50,75,100,150,200]
    list_multiplicator = [3 for i in range(10)]

# Number of sets of parameters
length = len(list_ncomp)

# Importing the libraries
import numpy as np
import umap
import matplotlib.pyplot as plt
from _2_1extractingsample import matrix_doc, matrix_go, infos_doc, doc_selected, sample_path
from tqdm import tqdm
import os

# Creating the folder
UMAP_path = sample_path+"UMAP"
if not os.path.exists(UMAP_path):
    os.makedirs(UMAP_path)
UMAP_path = UMAP_path+'\\'

# Doing the SVD and gathering the data
if which_one == 1 :
    matrix = matrix_doc
if which_one == 2 :
    matrix = matrix_go
d , w = len(matrix) , len(matrix[0])
U , s , Vh = np.linalg.svd( matrix , full_matrices=True )
ns = np.zeros((d,w))
for i in range(d):
    for j in range(w):
        if i == j :
            ns[i,j] = s[i]
Us = np.dot(U,ns)
print('\nSVD done.')

list_code = list(infos_doc[:,0])
list_col = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]

# Defining the euclidian distance
def euclidian_distance(x1 , x2):
    return np.sqrt( sum( (np.subtract(x1,x2))**2 ) )


# Defining useful functions for the UMAP

# This is used to find the minimum distance for the UMAP algorithm
def minimum(dist_matrix):
    res = dist_matrix[0,1]
    for line in dist_matrix :
        for val in line :
            if (val>0.0) and (val<res) :
                res = val
    return res

# This is to create, draw and save every UMAP for every set of parameters
def draw_umap(n_neighbours=15, min_dist=0.1, number=0, metric='euclidean'):
    fit = umap.UMAP(
        n_neighbors=n_neighbours,
        min_dist=min_dist,
        n_components=2,
        metric=metric)
    u = fit.fit_transform(data);
    list1 , list2 = u[:,0] , u[:,1]
    if np.max(u[:,0])-np.min(u[:,0]) > np.max(u[:,1])-np.min(u[:,1]) :
        list1 , list2 = u[:,1] , u[:,0]
    plt.figure(figsize=(10,6))
    plt.scatter(list1, list2, c=list_col, cmap='rainbow')
    plt.colorbar()
    if which_one == 1 :
        title = '2D rep of the docs with UMAP for TF-IDF (n_neigh='+str(n_neighbours)+', m='+str(list_multiplicator[i])+')'
    if which_one == 2 :
        title = '2D rep of the docs with UMAP for Getis-Ord (n_neigh='+str(n_neighbours)+', m='+str(list_multiplicator[i])+')'
    plt.title(title)
    if which_one == 1 :
        plt.savefig(UMAP_path+'umap_tfidf (neigh='+str(n_neighbours)+', multi='+str(list_multiplicator[i])+').png')
    if which_one == 2 :
        plt.savefig(UMAP_path+'umap_go (neigh='+str(n_neighbours)+', multi='+str(list_multiplicator[i])+').png')
    plt.show()

# Using the functions
for i in range(length) :
    init_vectors = [ Us[i][:3] for i in range(len(Us)) ]
    init_dist = np.array([ [ euclidian_distance(x, init_vectors[i]) for x in init_vectors ] for i in tqdm(range(len(init_vectors))) ], dtype=float)

    data = Us[:,:list_ncomp[i]]
    draw_umap(n_neighbours=list_neighbours[i], min_dist=minimum(init_dist)*list_multiplicator[i], number=i)











