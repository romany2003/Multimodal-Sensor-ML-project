import dash
from dash.dependencies import Output, Input
from dash import dcc, html, dcc
from datetime import datetime
import json
import plotly.graph_objs as go
from collections import deque
from flask import Flask, request
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.cluster import KMeans
from tqdm import tqdm 
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from sklearn.svm import OneClassSVM

data = pd.read_csv("out.csv")
data2 = pd.read_csv("out2.csv")


def findpca(data):
   #covarience
    data1 = np.array(list(data.values))
    cov_matrix = np.cov(data1)
    

    print(f"the shape of this matrix is: {cov_matrix.shape}\n")
    print(f"the covarnce matrix is: {cov_matrix}")
    
    #PCA
    scaled_data = preprocessing.scale(data1)
    pca = PCA(n_components=6)
    data_pca = pca.fit_transform(scaled_data)
    PC_values =  np.arange(pca.n_components) + 1
    kmeans = KMeans(n_clusters=2)
    labels = kmeans.fit_predict(data_pca)

    plt.scatter(data_pca[:,0],data_pca[:,1], c = labels, s = 1)
    plt.title('PCA PLOT')
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA Plot")
    plt.show()
  
    
findpca(data)


data1_dtw = pd.read_csv("out.csv")
data2_dtw = pd.read_csv("out2.csv")

#Dynamic Time warping(DTW)
def DTW(data1_dtw, data2_dtw):   
    data1 = pd.DataFrame(np.array(data1_dtw))
    data2 = pd.DataFrame(np.array(data2_dtw))
    distance, path = fastdtw(data1,data2, dist=euclidean )
    wraped_signal = np.empty_like(data1)
    print(F"The shape of the sample 1: {data1.shape}")
    print(F"The shape of the sample 2: {data2.shape}")

    print(f"The Distance is: {distance}")
    print('------------------------------------------------------------------')
    print(f"The Paths are: {path}")
    print('------------------------------------------------------------------')


    
   
DTW(data1_dtw, data2_dtw)

    
def aonomly(data,data2):
   #baseline data
    base_data = np.array(list(data.values))
    scaled_data = preprocessing.scale(base_data)
    pca_base = PCA(n_components=6)
    data_pca_base = pca_base.fit_transform(scaled_data)
    
    #anomoly data
    anom_data = np.array(list(data2.values))
    scaled_data = preprocessing.scale(anom_data)
    pca_anom = PCA(n_components=6)
    data_pca_anom = pca_anom.fit_transform(scaled_data)
    
    
    #train
    svm = OneClassSVM(nu=0.1, kernel="rbf")  # Adjust 'nu' based on your dataset
    svm.fit(data_pca_base)
   

    # predict anomalies
    pred = svm.predict(data_pca_anom)
    print(f"This is the prediction: {pred}")
    print('------------------------------------------------------------------')

    for i in range(len(pred)):
        
        if(pred[i] == -1):
            print("THERE HAS BEEN AN ANOMOLY DETECTED, RUNNNN!")
            break
        elif(pred[i] == 1) :
            print('NO Anomoly found in new data set')
    
   
aonomly(data,data2)