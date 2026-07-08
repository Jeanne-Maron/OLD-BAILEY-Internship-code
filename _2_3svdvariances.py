# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:37:18 2026

@author: jeann2e
"""

# To do the analysis for the variances of the right sample, the file '_2_1extractingsample.py' 
# has to be modified accordingly.
# You can choose to analyze the variances of the TF-IDF matrix or the GO matrix.
# 1 for TF-IDF, 2 for GO z-score
which_one = 1

# This file is used to analyze the components of the matrix obtained by the SVD. Calculating
# the variances of each component is useful because it allows to see which components of the
# SVD are useful and which one reflect only the noise in the data. A broken-stick model is
# also present to select only the most interesting components.

# Here the right matrix and folder is selected
if which_one == 1 :
    from _2_2svd_tfidf import U , V , s , matrix_doc , SVD_TFIDF_path
    matrix = matrix_doc
    path = SVD_TFIDF_path
if which_one == 2 :
    from _2_2svd_go import U , V , s , matrix_go , SVD_GO_path
    matrix = matrix_go
    path = SVD_GO_path
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Here is defined the Frobenius Norm, the norm used for the variances of the matrix and the 
# individual components
def frobenius_norm(M):
    norm = 0
    for ligne in M :
        for mij in ligne :
            norm += mij*mij
    return np.sqrt(norm)

# This is the global norm of the original matrix data
norm_m = frobenius_norm(matrix)

# These are the sizes of the matrices
m , n = len(matrix) , len(matrix[0])
r = len(s)

# The lists of the measures that will be calculated are created. The measures are: the 
# variance of each individual component of the SVD of the data matrix, the variance of the 
# SVD matrix as each individual component is added, normalized with the norm of the original 
# matrix data, and the variances of each individual component of the SVD of a random matrix 
# (for the broken-stick model).
list_x = [ k for k in range(r) ]
list_compmk = [ 0 for i in range(r) ]
list_cumulmk = [ 0 for i in range(r) ]
list_comprm = [ 0 for i in range(r) ]

# We create and do the SVD of the random matrix
rand_matrix = np.random.uniform(-1,1, size=(m,n))
norm_r = frobenius_norm(rand_matrix)
Ur , sr , Vhr = np.linalg.svd( rand_matrix , full_matrices=True )
Vr = np.transpose( Vhr )
print('\nSVD random matrix done.')

# Now all of the lists described above are completed
mk = np.zeros((m,n))
print('\nVariances calculation :')
for k in tqdm(range(r)):
    ui , vit = np.transpose([U[:,k]]) , np.array([V[:,k]])
    it = s[k]* np.dot( ui , vit )
    uir , vitr = np.transpose([Ur[:,k]]) , np.array([Vr[:,k]])
    itr = sr[k]* np.dot( uir , vitr )
    mk = np.add( mk , it )
    norm_k = frobenius_norm(mk)
    norm_component = frobenius_norm(it)
    norm_cprd = frobenius_norm(itr)
    list_cumulmk[k] = norm_k / norm_m
    list_compmk[k] = norm_component / norm_m
    list_comprm[k] = norm_cprd / norm_r


# Now we apply the broken-stick rule, by looking at where the individual component of the 
# random matrix becomes greater than the individul component of the data matrix. 
for i in range(len(list_x)) :
    if list_comprm[i] > list_compmk[i] :
        print('Maximum component to analyze the PCA :',i)
        limit = i
        break

### Plotting the graphs

# This is to include the zero
list_x1 = []
list_x2 , list_y2 = [0] , [0]
for i in range(len(list_x)):
    list_x1.append(list_x[i]+1)
    list_x2.append(list_x[i]+1)
    list_y2.append(list_cumulmk[i])

# First graph: component and cumulative variance

fig, ax1 = plt.subplots()
# Plot the component variance
ax1.semilogy(list_x1, list_compmk, color='limegreen', label='By component')
ax1.set_xlabel('Number of components')
ax1.set_ylabel('Variance by component', color='black')
ax1.tick_params(axis='y', labelcolor='limegreen')
if which_one == 1 :
    ax1.set_ylim(2.5*10**(-2),0.5)
if which_one == 2 :
    ax1.set_ylim(3*10**(-2),0.5)
# Create a second axis
ax2 = ax1.twinx()
# Plot the cumulative variance
ax2.plot(list_x2, list_y2, color='lightseagreen', label='Cumulative ')
ax2.set_ylabel('Cumulative variance', color='black')
ax2.tick_params(axis='y', labelcolor='lightseagreen')
ax2.set_xlim(-5,200)
ax2.set_ylim(0,1)
fig.suptitle('Variance by component for the SVD')
# The labels are added
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.grid()
plt.savefig(path+'Variances by component 1.png')
plt.show()

# Second graph: component and cumulative variance (zoomed)

fig, ax1 = plt.subplots()
# Plot the component variance
ax1.semilogy(list_x1, list_compmk, color='limegreen', label='By component')
ax1.set_xlabel('Number of components')
ax1.set_ylabel('Variance by component', color='black')
ax1.tick_params(axis='y', labelcolor='limegreen')
if which_one == 1 :
    ax1.set_ylim(7*10**(-2),0.4)
if which_one == 2 :
    ax1.set_ylim(6*10**(-2),0.5)
# Create a second axis
ax2 = ax1.twinx()
# Plot the cumulative variance
ax2.plot(list_x2, list_y2, color='lightseagreen', label='Cumulative ', marker='.')
ax2.set_ylabel('Cumulative variance', color='black')
ax2.tick_params(axis='y', labelcolor='lightseagreen')
ax2.set_xlim(-0.5,20.5)
ax2.set_ylim(0,1)
fig.suptitle('Variance by component for the SVD')
# The labels are added
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.grid()
plt.savefig(path+'Variances by component 2.png')
plt.show()

# Third graph: with the broken-stick model

fig, ax1 = plt.subplots()
# Plot the data
ax1.semilogy(list_x, list_compmk, color='limegreen', label='Data matrix')
ax1.semilogy(list_x, list_comprm, color='mediumvioletred', label='Random matrix')
ax1.set_xlabel('Number of components')
ax1.set_ylabel('Variance by component', color='black')
ax1.tick_params(axis='y')
if which_one == 1 :
    ax1.set_ylim(2.5*10**(-2),0.4)
    t = plt.text(170,0.21,'Max comp : '+str(limit))
    t.set_bbox(dict(facecolor='red', alpha=0.25))
if which_one == 2 :
    ax1.set_ylim(0.03,0.5)
    t = plt.text(170,0.13,'Max comp : '+str(limit))
    t.set_bbox(dict(facecolor='red', alpha=0.25))
fig.suptitle('Broken-stick model for the SVD')
ax1.set_xlim(-10,250)
ax1.legend(loc='upper right')
plt.grid()
plt.savefig(path+'Broken-stick model.png')
plt.show()