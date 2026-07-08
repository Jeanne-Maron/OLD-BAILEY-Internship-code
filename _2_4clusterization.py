#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 12:38:14 2026

@author: jeann2e
"""

# This part is too choose all of the parameters that will be applied to do the clusterization.
# The method has to be chosen, and then, the number of components taken into acount for
# the clusterization. It is also possible to choose the seed for the k-means. Addiotionally,
# the maximal number of clusters has to be chosen (the clusetrization will be done for 2 to
# n_clus clusters). Finally, the matrix on which the clusterization will be done is chosen.

# Methods available : 'Ward', 'Ward UMAP', 'k-means', 'Spectral', 'HDBscan'
# The spectral clustering uses UMAP to function, and only works for the Getis Ord matrix

method = 'Ward'
n_comp = 3
k_means_seed = 0        # only useful for k-means
n_clus = 8              # not useful forHDBscan
# 1 for TF-IDF , 2 for GO z-score
which_one = 1

## These are the UMAP parameters. Thanks to the file _2_3umap.py, a lot of sets were tested 
# and then the best was used here.
if which_one == 1 :
    n_neighbours , multiplicator = 150 , 5
if which_one == 2 :
    n_neighbours , multiplicator = 25 , 3



# Importing the libraries
from _2_1extractingsample import matrix_go, matrix_doc, infos_doc, doc_selected, sample_path
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans, HDBSCAN, SpectralClustering
from scipy.cluster import hierarchy
import matplotlib as mpl
import umap

# Doing the SVD
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

# Creating the folders and sub-folders corresponding to the right clusterization method
path_here = sample_path+"Clusterization"
if not os.path.exists(path_here):
    os.makedirs(path_here)
path_here = path_here+'/'
if which_one == 1 :    
    path_here = path_here+'TFIDF '+method
if which_one == 2 :
    path_here = path_here+'GO '+method
if not os.path.exists(path_here):
    os.makedirs(path_here)
path_here = path_here+'/'
path_here = path_here+'n = '+str(n_comp)
if not os.path.exists(path_here):
    os.makedirs(path_here)
path_here = path_here+'/'

### Initial distance matrix for the silhouette score

init_vectors = [ Us[i][:n_comp] for i in range(len(Us)) ]

def euclidian_distance(x1 , x2):
    return np.sqrt( sum( (np.subtract(x1,x2))**2 ) )

init_dist = np.array([ [ euclidian_distance(x, init_vectors[i]) for x in init_vectors ] for i in tqdm(range(len(init_vectors))) ], dtype=float)

def minimum(dist_matrix):
    res = dist_matrix[0,1]
    for line in dist_matrix :
        for val in line :
            if (val>0.0) and (val<res) :
                res = val
    return res

### Clustering the data: all of the different methods

c_prog = [ ]

if method == 'k-means' :
    method = method+' (seed='+str(k_means_seed)+')'
    doc_list = [ Us[i][:n_comp] for i in range(len(Us)) ]
    list_n = [ n for n in range(1,n_clus+1) ]
    for n in list_n :
        kmeans = KMeans(n_clusters=n, random_state=k_means_seed, n_init="auto").fit(np.array(doc_list, dtype=float))
        clus_list = kmeans.labels_
        clusters = [ [] for i in range(n) ]
        for i in range(len(clus_list)) :
            clusters[clus_list[i]].append(i)
        c_prog.append(clusters)

if method == 'Spectral' :
    doc_list = Us[:,:n_comp]
    list_n = [ n for n in range(1,n_clus+1) ]
    min_dist = minimum(init_dist)*multiplicator
    umap_trans = umap.UMAP(n_neighbors=n_neighbours, min_dist=min_dist, n_components=2, metric='euclidean')
    u = umap_trans.fit_transform(doc_list)
    plt.figure(figsize=(10,6))
    list_code = list(infos_doc[:,0])
    list_col = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
    plt.scatter(u[:,0], u[:,1], c=list_col, cmap='rainbow')
    plt.colorbar()
    if which_one == 1 :
        title = '2D rep of the docs with UMAP for TF-IDF (n_neigh='+str(n_neighbours)+', m='+str(multiplicator)+')'
    if which_one == 2 :
        title = '2D rep of the docs with UMAP for Getis-Ord (n_neigh='+str(n_neighbours)+', m='+str(multiplicator)+')'
    plt.title(title)
    if which_one == 1 :
        plt.savefig(path_here+'umap_tfidf for the Spectral clusterisation.png')
    if which_one == 2 :
        plt.savefig(path_here+'umap_go for the Spectral clusterisation.png')
    plt.show()
    for n in list_n :
        spectral = SpectralClustering(n_clusters=n, n_components=2).fit(np.array(u, dtype=float))
        clus_list = spectral.labels_
        clusters = [ [] for i in range(n) ]
        for i in range(len(clus_list)) :
            clusters[clus_list[i]].append(i)
        c_prog.append(clusters)

if method == 'HDBscan' :
    doc_list = Us[:,:n_comp]
    list_n = [ n for n in range(1,n_clus+1) ]
    min_dist = minimum(init_dist)*multiplicator
    umap_trans = umap.UMAP(n_neighbors=n_neighbours, min_dist=min_dist, n_components=2, metric='euclidean')
    u = umap_trans.fit_transform(doc_list)
    plt.figure(figsize=(10,6))
    list_code = list(infos_doc[:,0])
    list_col = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
    plt.scatter(u[:,0], u[:,1], c=list_col, cmap='rainbow')
    plt.colorbar()
    if which_one == 1 :
        title = '2D rep of the docs with UMAP for TF-IDF (n_neigh='+str(n_neighbours)+', m='+str(multiplicator)+')'
    if which_one == 2 :
        title = '2D rep of the docs with UMAP for Getis-Ord (n_neigh='+str(n_neighbours)+', m='+str(multiplicator)+')'
    plt.title(title)
    if which_one == 1 :
        plt.savefig(path_here+'umap_tfidf for the Spectral clusterisation.png')
    if which_one == 2 :
        plt.savefig(path_here+'umap_go for the Spectral clusterisation.png')
    plt.show()
    hdbscan = HDBSCAN().fit(np.array(u, dtype=float))
    clus_list = hdbscan.labels_
    n = max(clus_list)+1
    clusters = [ [] for i in range(n) ]
    noises = []
    for i in range(len(clus_list)) :
        if i == -1 :
            noises.append(i)
        else :
            clusters[clus_list[i]].append(i)

if method == 'Ward' :  
    doc_list = Us[:,:n_comp]
    ward = hierarchy.linkage(doc_list, 'ward')
    for n in range(1,n_clus+1) :
        clus_list = hierarchy.fcluster(ward,n,'maxclust')
        clusters = [ [] for i in range(n) ]
        for i in range(len(clus_list)) :
            clusters[clus_list[i]-1].append(i)
        c_prog.append(clusters)
    labels = [ len(cluster) for cluster in c_prog[7] ]
    fig = plt.figure()
    cmap = ['mediumorchid','cornflowerblue','springgreen']
    hierarchy.set_link_color_palette([mpl.colors.rgb2hex(rgb[:]) for rgb in cmap])
    dn = hierarchy.dendrogram( ward, p=8, truncate_mode='lastp', above_threshold_color='firebrick', no_labels=True, orientation='left')
    ax = plt.gca()
    ax.spines['top'].set_color('none') , ax.spines['left'].set_color('none') , ax.spines['right'].set_color('none')
    plt.xlabel('Euclidian distance')
    plt.title('Dendogram of the clusters (Ward, for n = '+str(n_comp)+')')
    plt.savefig(path_here+'dendogram.png')
    plt.show()
    
if method == 'Ward UMAP' :
    doc_list = Us[:,:n_comp]
    list_n = [ n for n in range(1,n_clus+1) ]
    min_dist = minimum(init_dist)*multiplicator
    umap_trans = umap.UMAP(n_neighbors=n_neighbours, min_dist=min_dist, n_components=2, metric='euclidean')
    u = umap_trans.fit_transform(doc_list)
    plt.figure(figsize=(10,6))
    list_code = list(infos_doc[:,0])
    list_col = [ int(infos_doc[list_code.index(code),3]) for code in doc_selected ]
    plt.scatter(u[:,0], u[:,1], c=list_col, cmap='rainbow')
    plt.colorbar()
    if which_one == 1 :
        title = '2D rep of the docs with UMAP for TF-IDF (n_neigh='+str(n_neighbours)+', m='+str(multiplicator)+')'
    if which_one == 2 :
        title = '2D rep of the docs with UMAP for Getis-Ord (n_neigh='+str(n_neighbours)+', m='+str(multiplicator)+')'
    plt.title(title)
    if which_one == 1 :
        plt.savefig(path_here+'umap_tfidf for the Spectral clusterisation.png')
    if which_one == 2 :
        plt.savefig(path_here+'umap_go for the Spectral clusterisation.png')
    plt.show()
    ward = hierarchy.linkage(u, 'ward')
    for n in range(1,n_clus+1) :
        clus_list = hierarchy.fcluster(ward,n,'maxclust')
        clusters = [ [] for i in range(n) ]
        for i in range(len(clus_list)) :
            clusters[clus_list[i]-1].append(i)
        c_prog.append(clusters)
    labels = [ len(cluster) for cluster in c_prog[7] ]
    fig = plt.figure()
    cmap = ['mediumorchid','cornflowerblue','springgreen']
    hierarchy.set_link_color_palette([mpl.colors.rgb2hex(rgb[:]) for rgb in cmap])
    dn = hierarchy.dendrogram( ward, p=8, truncate_mode='lastp', above_threshold_color='firebrick', no_labels=True, orientation='left')
    ax = plt.gca()
    ax.spines['top'].set_color('none') , ax.spines['left'].set_color('none') , ax.spines['right'].set_color('none')
    plt.xlabel('Euclidian distance')
    plt.title('Dendogram of the clusters (Ward, for n = '+str(n_comp)+')')
    plt.savefig(path_here+'dendogram.png')
    plt.show()

# Printing the parameters used
print('\nParameters used :\n\t - Method : '+method+'\n\t - Number of components : '+str(n_comp))


### Plotting the results

list_code = list(infos_doc[:,0])
colors = ['red','mediumblue','gold','green','orange','cornflowerblue','deeppink','darkorchid','limegreen']

if method != 'HDBscan' :
    for n in range(2,n_clus+1) :
        for i in range(n) :
            list_x = [ int(infos_doc[list_code.index(doc_selected[code]),3]) for code in c_prog[n-1][i] ]
            list_y = [ Us[j,0] for j in c_prog[n-1][i] ]
            plt.plot( list_x, list_y, color=colors[i], linewidth=0, marker='.')
        plt.xlabel('Date')
        if which_one == 1 :
            plt.ylabel('Weight on the 1st TFIDF comp')
            plt.title(method+' with n='+str(n_comp)+' for the TFIDF ('+str(n)+' clusters)')
            plt.savefig(path_here+'tfidf_'+method+'_n='+str(n_comp)+'_'+str(n)+' clusters.png')
        if which_one == 2 :
            plt.ylabel('Weight on the 1st GO comp')
            plt.title(method+' with n='+str(n_comp)+' for the GO ('+str(n)+' clusters)')
            plt.savefig(path_here+'go_'+method+'_n='+str(n_comp)+'_'+str(n)+' clusters.png')
        plt.show()
else :
    n_clusters = max(clus_list) + 1
    for i in range(n_clusters) :
        list_x = [ int(infos_doc[list_code.index(doc_selected[code]),3]) for code in clusters[i] ]
        list_y = [ Us[j,0] for j in clusters[i] ]
        plt.plot( list_x, list_y, color=colors[i], linewidth=0, marker='.')
    plt.xlabel('Date')
    if which_one == 1 :
        plt.ylabel('Weight on the 1st TFIDF comp')
        plt.title(method+' with n='+str(n_comp)+' for the TFIDF ('+str(n_clusters)+' clusters)')
        plt.savefig(path_here+'tfidf_'+method+'_n='+str(n_comp)+'_'+str(n_clusters)+' clusters.png')
    if which_one == 2 :
        plt.ylabel('Weight on the 1st GO comp')
        plt.title(method+' with n='+str(n_comp)+' for the GO ('+str(n_clusters)+' clusters)')
        plt.savefig(path_here+'go_'+method+'_n='+str(n_comp)+'_'+str(n_clusters)+' clusters.png')
    plt.show()

        
### Silhouette
# Now we calculate the silhouette score for every clusterization computed before. This is to
# see which clusterization finds the best clusters.

# Here are defined all of the useful functions to calculate the silhouettes
def a_sil(i , clusters):
    res = 0
    for clus in clusters:
        if i in clus :
            for neighbour in clus :
                res += init_dist[i,neighbour]
            if len(clus) == 1 :
                return 0.0
            return res / (len(clus)-1)

def d_sil(i , C , clusters):
    res = 0
    for not_neigh in clusters[C] :
        res += init_dist[i,not_neigh]
    return res / len(clusters[C])

def b_sil(i , clusters):
    res , neighbour = init_dist[i,0] * (10**6) , 0
    for C in range(len(clusters)) :
        if i not in clusters[C] :
            if res > d_sil(i,C,clusters) :
                res , neighbour = d_sil(i,C , clusters) , C
    return res , neighbour

def s_sil(i , clusters):
    a , b = a_sil(i , clusters) , b_sil(i , clusters)[0]
    if max(a,b) == 0.0 :
        return 0.0
    return (b-a) / max(a,b)

def avg_sil(clusters) :
    res , n_obj = 0 , 0
    for cluster in clusters :
        for i in cluster :
            res , n_obj = res + s_sil(i , clusters) , n_obj + 1
    return res / n_obj

# Now the silhouettes are plotted depending on the number of clusters. HDBscan is not 
# included because with this method not everything is included in a cluster at the end. Some
# are simply considered as noise.
if method != 'HDBscan' :    
    list_x = [ n for n in range(2,n_clus+1) ]
    list_y = [ avg_sil(c_prog[n-1]) for n in range(2,n_clus+1) ]
    plt.plot(list_x,list_y,color='purple',linestyle='--',marker='o')
    plt.xlabel('Number of clusters')
    plt.grid()
    plt.ylabel('Overall average silhouette width')
    if which_one == 1 :
        plt.title('Silhouette scores TFIDF ('+method+', n='+str(n_comp)+')')
        plt.savefig(path_here+'silhouette_tfidf_'+method+'_n='+str(n_comp)+'.png')
    if which_one == 2 :
        plt.title('Silhouette scores GO ('+method+', n='+str(n_comp)+')')
        plt.savefig(path_here+'silhouette_go_'+method+'_n='+str(n_comp)+'.png')
    plt.show()





