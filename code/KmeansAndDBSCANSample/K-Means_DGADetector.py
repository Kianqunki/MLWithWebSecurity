# -*- coding:utf-8 -*-

import sys
import re
import numpy as np
from sklearn.externals import joblib
import csv
import matplotlib.pyplot as plt
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
import os
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE


#处理域名的最小长度
MIN_LEN=10

#随机程度
random_state = 170


def load_alexa(filename):
    domain_list=[]
    csv_reader = csv.reader(open(filename))
    for row in csv_reader:
        domain=row[1]
        if len(domain) >= MIN_LEN:
            domain_list.append(domain)
    return domain_list

def domain2ver(domain):
    ver=[]
    for i in range(0,len(domain)):
        ver.append([ord(domain[i])])
    return ver


def load_dga(filename):
    domain_list=[]
    #xsxqeadsbgvpdke.co.uk,Domain used by Cryptolocker - Flashback DGA for 13 Apr 2017,2017-04-13,
    # http://osint.bambenekconsulting.com/manual/cl.txt
    with open(filename) as f:
        for line in f:
            domain=line.split(",")[0]
            if len(domain) >= MIN_LEN:
                domain_list.append(domain)
    return  domain_list


def kmeans_dga():
    x1_domain_list = load_alexa("../../data/DGA_data/top-1000.csv")
    x2_domain_list = load_dga("../../data/DGA_data/dga-cryptolocke-1000.txt")
    x3_domain_list = load_dga("../../data/DGA_data/dga-post-tovar-goz-1000.txt")

    x_domain_list=np.concatenate((x1_domain_list, x2_domain_list,x3_domain_list))
    #x_domain_list = np.concatenate((x1_domain_list, x2_domain_list))

    y1=[0]*len(x1_domain_list)
    y2=[1]*len(x2_domain_list)
    y3=[1]*len(x3_domain_list)

    y=np.concatenate((y1, y2,y3))
    #y = np.concatenate((y1, y2))

    #print x_domain_list

    cv = CountVectorizer(ngram_range=(2, 2), decode_error="ignore",
                                          token_pattern=r"\w", min_df=1)
    x= cv.fit_transform(x_domain_list).toarray()
    model=KMeans(n_clusters=2, random_state=random_state)
    y_pred = model.fit_predict(x)
    #print  y_pred

    tsne = TSNE(learning_rate=100)
    x=tsne.fit_transform(x)
    print(x)
    print(x_domain_list)

    for i,label in enumerate(x):
        #print label
        x1,x2=x[i]
        if y_pred[i] == 1:
            plt.scatter(x1,x2,marker='o')
        else:
            plt.scatter(x1, x2,marker='x')
        #plt.annotate(label,xy=(x1,x2),xytext=(x1,x2))

    plt.show()

if __name__ == '__main__':
    kmeans_dga()


