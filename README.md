# OLD-BAILEY-Internship-code
In this repository is stored the code used during the internship done in the first year of my Masters in Physics. This code is used to analyze the lexical variations of the Old Bailey corpus.

# Explanations for the OLD-BAILEY code

The code contains two main steps. The first one creates the lexicons and the matrices Mt and Mg. The second contains several programs that can be used to analyze the matrices obtained.

To create both matrixes, two files have to be opened. First, the file _1_2settingparameters.py has to be opened to modify all the parameters wanted to create the sample. The file can then be saved and closed. After, the file _1_3getisordmatrix.py has to be opened and ran. On my laptop, both matrices were computed in 3 hours and 30 minutes.

After the matrices are created, you have to go to the file _2_1extractingsample.py to write the name of the sample that you want to analyze. Then, any file like _2*.py can be ran to analyze the sample.


## Details: Part 1

### _1_2settingparameters.py
The file needs to be open when creating a sample. It allows the user to set all of the parameters that will be applied when creating the sample. You have to set:
       - the name
       - the maximal percentage of documents (for the dictionary)
       - the minimum number of documents (for the dictionary)
       - the neighbourhood parameter for the Getis Ord matrix
The program then creates a folder for the sample, and with the documents tokenized, selects only the documents fitting the criteria given above. It also creates and saves the files doc_selected.txt, len_selected.txt, and the repartition of years, lengths and tokens of the documents.

### _1_3getisordmatrix.py
This is the file the user needs to execute to create the full sample, as it will run all of the files from part 1 (except the _1_1processingtxt.py one), creating and saving all the needed files and informations of the sample. 
This program in particular creates the Getis Ord's z-score matrix.

### _1tokenization.py
The program retreives all of the processed documents from 'corpus1' and tokenizes them. It also retreives the infos_doc.txt file.

### _1dictionary.py
The program creates and then filters the dictionary. It also saves the words that were filtered in different files:
       - maxi_wordsn.txt
       - mini_words.txt
       - proper_names.txt
The dictionary is saved in dico_filtered.txt.

### _1tfidfmatrix.py
The program creates and saves the TF-IDF matrix.


## Details: Part 2

### _2_1extractingsample.py
The user needs to enter the name of the sample that will be analyzed.
It also prints all of the parameters of the sample.

### _2_2svd_tfidf.py
The SVD is done for the TF-IDF matrix. It creates a folder where everything will be saved. It saves the n most significant words of the first 4 components. It also plots differents types of graphs:
       - one dimension weights for the 1st 4 components (Year/doc Weight)
       - two dimension weights for the 1st 4 components (doc Weight/doc Weight, and color-coded years)
       - one dimension weights for significant words of components (Year/word Weight)
       - one dimension weights for lengths (Length/doc Weight)

### _2_2svd_go.py
The SVD is done for the Getis Ord's z-score matrix. After that, it does the same thing as the SVD TF-IDF program (same plots, etc).

### _2_3svdvariances.py
The variances (Frobenius norm) are computed and saved in two graphs (one zoomed, one less zoomed). The variances calculated are the individual component variance for each component, as well as the normalized cumulative variance as components are added, are plotted. A broken-stick model or broken-stick rule is also implemented to show which are the most useful components. The graphs of the broken-stick model may have to be adjusted in the way they are plotted.

### _2_3umap.py
This file is to apply the UMAP to a sample. It does the SVD of the matrix chosen and then applies the SVD for every set of parameters given. This is useful to see which set of parameters gives a good UMAP of the data. This type of information can be used for the clusterization methods that use UMAP.

### _2_4clusterization
This is used to calculate, plot and save different clusterizations. A lot of parameters can be modified: the clusterization method used, the number of components taken into account, the k-means seed (if k-means is chosen), the maximum number of clusters wanted (the clusters will be calculated for 2 to n_clus clusters).
The file does a few things. First, if the clusterization method uses UMAP, it plots and saves the UMAP used. Then, if the Ward method was chosen, the dendrogram is plotted. Then, it plots every clusterization realized for 2 to n_clus. Finally (except for HDBscan), the silhouette score for each number of cluster is calculated, plotted and saved.

### _2_4compcomparison.py
This file compares the lists of significant words for one given axis of the TFIDF matrix and one given axis of the Getis-Ord matrix. It compares the similarity of the lists, thanks to the Jaccard Index and a new index, depending on the lengths of the lists taken. This allows us to see if axes that seem similar from one matrix to another are really caused by similar reasons or not.

### _3_zipfslaw.py
This is used to see if Zipf's law is verified for a given sample. It also does a linear regress to check it.

### _3_heapslaw.py
This is used to see if Heap's law is verified for a given sample. It also does a linear regress to check it.
