import torch
from transformers import AutoModel, AutoTokenizer
import regex as re
import underthesea
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score 
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Hàm load model BERT
def load_bert():
    v_phobert = AutoModel.from_pretrained("vinai/phobert-base")
    v_tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)
    return v_phobert, v_tokenizer 

# Hàm chuẩn hoá câu
def standardize_data(row):
    row = row.replace(",", " ").replace(".", " ") \
        .replace("`", " ").replace("~", " ") \
        .replace("!", " ").replace("@", " ") \
        .replace('#', " ").replace("$", " ") \
        .replace("%", " ").replace("^", " ") \
        .replace("&", " ").replace("*", " ") \
        .replace("(", " ").replace(")", " ") \
        .replace("-", " ").replace("_", " ") \
        .replace("+", " ").replace("=", " ") \
        .replace("{", " ").replace("[", " ") \
        .replace("}", " ").replace("]", " ") \
        .replace("|", " ").replace("\\", " ") \
        .replace("}", " ").replace("]", " ") \
        .replace(":", " ").replace(";", " ") \
        .replace("\"", " ").replace("'", " ") \
        .replace("<", " ").replace(",", " ") \
        .replace(">", " ").replace(".", " ") \
        .replace("?", " ").replace("/", " ")\
        .replace("\t", " ")
    row = row.strip().lower()
    return row

def pre_process(line):
    line = standardize_data(line)
    line = underthesea.word_tokenize(line, format="text")
    return line

# data = pd.read_csv('nhung.csv',  sep=';', encoding="utf-8")
# labels = np.array(data['rating1'].apply((lambda x: int((x)))))

# for index in range(len(data['rating1'])):
#     try:
#         data['rating1'][index] = int(data['rating1'][index]) 
#     except:
#         print(data['comment'][index])
# labels = np.array(data['rating1'])

# data0 = data[data['rating1'] == 0]['comment']
# data1 = data[data['rating1'] == 1]['comment']
# data2 = data[data['rating1'] == 2]['comment']
# data3 = data[data['rating1'] == 3]['comment']
# data4 = data[data['rating1'] == 4]['comment']
# data5 = data[data['rating1'] == 5]['comment']
# print(len(data0))
# print(len(data1))
# print(len(data2))
# print(len(data3))
# print(len(data4))
# print(len(data5))


# for i in range(len(data['comment'])):
#     data.iloc[i,0] = pre_process(data.iloc[i,0])
    
# print(data.head())



def embedding(e_X_train, e_X_test, fulldata):
    global  emb
    emb = TfidfVectorizer(min_df=10, max_df=0.7,max_features=3000,sublinear_tf=True, ngram_range=(1, 1))
    emb.fit(fulldata)
    out_X_train =  emb.transform(e_X_train)
    out_X_test = emb.transform(e_X_test)
    print(emb.get_feature_names())
    print(out_X_train.shape)
    print(emb.idf_)
    # Save pkl file
    joblib.dump(emb, 'tfidf.pkl')
    return out_X_train, out_X_test


def phoBertExact():
    phobert, tokenizer = load_bert()
    tokenized = data['comment'].apply(lambda x: tokenizer.encode(x, add_special_tokens = True))
    # print('encode',tokenized[1])
    # print('decode',tokenizer.decode(tokenized[1]))

    max_len = 0

    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)      
    print('max len:', max_len)

    padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])
    #print('padded:', padded[1])
    # print('len padded:', padded.shape)

    attention_mask = np.where(padded ==0, 0,1)
    padded = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)


    with torch.no_grad():
        last_hidden_states = phobert(padded, attention_mask = attention_mask)
    # print('last hidden states:', last_hidden_states)

    features = last_hidden_states[0][:,0,:].numpy()
    # print('features:', features)
    print(features.shape)
    return features

def trainSVM(t_X_train, t_X_test, t_y_train, t_y_test, filemodel):
    param_grid = {'C': [0.1, 1, 10, 100, 1000], 
               'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel':['rbf']} 
  
    grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 3)
    grid.fit(t_X_train, t_y_train)
    # print best parameter after tuning
    print(grid.best_params_) 
    print(grid.best_estimator_)
    grid_predictions = grid.predict(t_X_test)
    # print(grid_predictions)
    print(classification_report(t_y_test, grid_predictions))
    sc = grid.score(t_X_test, t_y_test)
    print('Kết quả train model, độ chính xác SVM + GridSearch = ', sc*100, '%')
    joblib.dump(grid, filemodel)

def embeddingDataTraining():
    X_train, X_test, y_train, y_test = train_test_split(data['comment'], labels, test_size=0.2, random_state=5)
    X_train, X_test = embedding(X_train, X_test,data['comment'])
    trainSVM(X_train,X_test, y_train, y_test, "emb_model01.pkl")

def phoBertDataTraining():
    features = phoBertExact()
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.25, random_state=5)
    trainSVM(X_train,X_test, y_train, y_test,"phobert_model01.pkl")

# embeddingDataTraining()
# phoBertDataTraining()