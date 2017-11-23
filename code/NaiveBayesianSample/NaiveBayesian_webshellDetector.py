# _*_coding:utf-8_*_
#使用朴素贝叶斯检测webshell

import os
from sklearn.feature_extraction.text import CountVectorizer
import sys
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB


def load_file(file_path):
    try:
        t=""
        #用utf-8的编码方式打开
        with open(file_path,'r', encoding='UTF-8') as f:
            for line in f:
                line=line.strip('\n')
                t+=line
    #可能碰到gbk编码的无法解码，跳过
    except UnicodeDecodeError:
       pass
    
    return t


def load_files(path):
    files_list=[]
    for r, d, files in os.walk(path):
        for file in files:
            if file.endswith('.php'):
                file_path=path+file
                print("Load %s" % file_path)
                t=load_file(file_path)
                files_list.append(t)
    return  files_list



if __name__ == '__main__':

    #bigram_vectorizer = CountVectorizer(ngram_range=(2, 2),token_pattern = r'\b\w+\b', min_df = 1)
    webshell_bigram_vectorizer = CountVectorizer(ngram_range=(2, 2), decode_error="ignore",
                                        token_pattern = r'\b\w+\b',min_df=1)
    webshell_files_list=load_files("../../data/PHP-WEBSHELL/xiaoma/")
    x1=webshell_bigram_vectorizer.fit_transform(webshell_files_list).toarray()
    y1=[1]*len(x1)
    vocabulary=webshell_bigram_vectorizer.vocabulary_

    wp_bigram_vectorizer = CountVectorizer(ngram_range=(2, 2), decode_error="ignore",
                                        token_pattern = r'\b\w+\b',min_df=1,vocabulary=vocabulary)
    wp_files_list=load_files("../../data/wordpress/")
    x2=wp_bigram_vectorizer.fit_transform(wp_files_list).toarray()
    y2=[0]*len(x2)

    x=np.concatenate((x1,x2))
    y=np.concatenate((y1,y2))

    #print(x)
    #print(y)

    clf = GaussianNB()

    score = cross_val_score(clf, x, y, n_jobs=-1,cv=3)
    print(score)
    print(np.mean(score))



