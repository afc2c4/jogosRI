# -*- coding: utf-8 -*-
import glob
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import codecs

def removeHtmlTags(path):
    page = BeautifulSoup(open(path), "html.parser")
    [s.extract() for s in page("script")]
    [s.extract() for s in page("style")]

    page_content = page.get_text().encode("utf-8")
    return page_content

def takeAllFiles(file_type):
    files = glob.glob("sites/*/*/*." + file_type)

    return files

def removeSpecialCharacters(html_content):
    html_content = re.sub("\n+|\t+", " ", html_content)
    html_content = re.sub("[!\d+,.;@#?!&$--)(:/}{|=]+|•|©|﻿|™|®|×| x "," ",  html_content)
    return html_content

def putContentInFile(in_type, out_type):
    files = takeAllFiles(in_type)
    for i in range(len(files)):
        path_output = re.sub('.' + in_type, '.' + out_type, files[i])
        html_content = removeHtmlTags(files[i])
        html_content = removeSpecialCharacters(html_content)
        file = open(path_output, "w")
        file.write(html_content)
        file.close()

def stemming(vec_doc):
    stemmer = PorterStemmer()
    analyzer = CountVectorizer().build_analyzer()

    return (stemmer.stem(w) for w in analyzer(vec_doc))

def stop_words():
    stopWords = set(stopwords.words('english'))

    return stopWords

def MakeVecDoc():
    files = takeAllFiles("txt")

    vec_doc = [codecs.open(files[i], "r", encoding='utf-8').read() for i in range(len(files))]

    vec_class = [re.search("\w+/\w+/(\w+)/\w+", files[i]).group(1) == "positivePages" and 1 or 0
                for i in range(len(files))]

    return vec_doc, vec_class

def put_in_csv(dataName, doctermMatrix, vec_class):
    dataFrame = pd.DataFrame(doctermMatrix)
    dataFrame["class"] = vec_class
    dataFrame.to_csv("data/" + dataName + ".csv", index = False)

def tokenizeFiles(useStemming, useStopWords, dataName):
    vec_doc, vec_class = MakeVecDoc()
    vectorizer = None
    vectorizerTfidf = None
    if(useStemming == False and useStopWords == False):
        vectorizer = CountVectorizer(encoding='utf-8')
        vectorizerTfidf = TfidfVectorizer(encoding='utf-8')

    elif(useStemming == True and useStopWords == False):
        vectorizer = CountVectorizer(encoding='utf-8', analyzer=stemming)
        vectorizerTfidf = TfidfVectorizer(encoding='utf-8', analyzer=stemming)

    elif(useStemming == False and useStopWords == True):
        vectorizer = CountVectorizer(encoding='utf-8', stop_words=stop_words())
        vectorizerTfidf = TfidfVectorizer(encoding='utf-8', stop_words=stop_words())
    else:
        vectorizer = CountVectorizer(encoding='utf-8', stop_words=stop_words(), analyzer=stemming)
        vectorizerTfidf = TfidfVectorizer(encoding='utf-8', stop_words=stop_words(), analyzer=stemming)


    vectorizer.fit(vec_doc)
    vectorizerTfidf.fit(vec_doc)

    #put_in_csv(dataName, doctermMatrix.todense(), vec_class)
    #put_in_csv(dataName + "Tfidf", doctermMatrixTfidf.todense(), vec_class)

    return [vectorizer, vectorizerTfidf]

def main():
    vectorizer = tokenizeFiles(False, False, "token")
    #print(vectorizer[0].vocabulary_)

    #dataFrame = pd.DataFrame(vectorizer[0].vocabulary_)
    #dataFrame.to_csv("data/vocabulary.csv")
    info_gain = pd.read_csv("data/info_gain.csv")
    info_gain.drop("class", axis = 1, inplace = True)

    best_tokens = []
    info_gain_tokens = []
    for col in info_gain.columns:
        for i in vectorizer[0].vocabulary_:
            #print(int(col), i)
            if(int(col) == vectorizer[0].vocabulary_[i]):
                best_tokens.append(col)
                info_gain_tokens.append(i)
                break
    dataFrame = pd.DataFrame(zip(best_tokens, info_gain_tokens), columns = ["Name", "information_gain"])
    #print(dataFrame)
    dataFrame.to_csv("data/info_gain_tokens.csv", index = False, encoding='utf-8')

main()
