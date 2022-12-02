# -*- coding: utf-8 -*-
"""IIP_review 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pBaOPpD6ryOJYE67_yFGbfoc_pfC1e22
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing

data=pd.read_csv("chronic_kidney_disease_full.csv")

#Checking for null values
data.isnull().values.sum()

data.head()

data

"""Cleaning the data set"""

data=data.dropna()

data.shape

data= data.rename(columns={"'age'":'age',"'bp'":'bp',"'sg'":'sg',"'al'":'al',"'su'":'su',"'rbc'": 'rbc',"'pc'":'pc',"'pcc'":'pcc',"'ba'":'ba',"'bgr'":'bgr',"'bu'":'bu',"'sc'":'sc',"'sod'":'sod',"'pot'":'pot',"'hemo'":'hemo',"'pcv'":'pcv',"'wbcc'":'wbcc',"'rbcc'":'rbcc',"'htn'":'htn',"'dm'":'dm',"'cad'":'cad',"'appet'":'appet',"'pe'":'pe',"'ane'":'ane',"'class'":'clas'})
data.head()

#USING LABLE ENCODER
matrix = [] 
col=399
lis=['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane','clas']
for k in range(len(lis)):
    le=preprocessing.LabelEncoder()
    data[lis[k]]=le.fit_transform(data[lis[k]])

data.head()

ls2=data.columns.tolist() #entire list
print(ls2)
m=[]
for i in ls2:
   for j in lis: #list for which lable encoder was used
       if(i==j):
           p=ls2.index(i)
           if p not in m:
               m.append(p)
print(m)

#replacing '?' with null values
cnt=0
for i in ls2:
    for j in data[i]:
        try:
            if(j == '?'):
                   data[i] = data[i].replace(j,np.nan)
                   cnt+=1
        except:
            pass

print(cnt)

data.head()

data.isnull().values.sum()

data.shape

#there are 9975 values in total, out of which 775 are null values. Drop null values
data=data.dropna()

data.shape

for i in ls2:
    print(data[i].dtype)

#converting to datatype float
for i in ls2:
    data[i]=data[i].astype('float64')

data.head()

X=data.drop(['clas'],axis=1)
y=data['clas']

X.head()

y.head()

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

models=[
        ('rf',RandomForestClassifier()),
        ('nb',GaussianNB())
]

from sklearn.model_selection import train_test_split
X_train, X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
#train 80% data and test 20% data
for i,j in models:
    clf=j
    clf.fit(X_train,y_train)
    acc=clf.score(X_test,y_test)
    print(i,acc)

#printing accuracy of naive base and random forest

inp=[62,80,1.01,2,3,'normal','normal','notpresent','notpresent',423,53,1.8,111,2.5,9.6,31,7500,3.5,'no','yes','no','poor','no','yes']

for i in range(len(inp)):
    if(inp[i]=='normal'):
        inp[i]=2
    if(inp[i]=='abnormal'):
        inp[i]=1
    if(inp[i]=='present'):
        inp[i]=2
    if(inp[i]=='notpresent'):
        inp[i]=1
    if(inp[i]=='yes'):
        inp[i]=2
    if(inp[i]=='no'):
        inp[i]=1
    if(inp[i]=='good'):
        inp[i]=1
    if(inp[i]=='poor'):
        inp[i]=2


inp=[62,80,1.01,2,3,'normal','normal','notpresent','notpresent',423,53,1.8,111,2.5,9.6,31,7500,3.5,'no','yes','no','poor','no','yes']        

f_list = [] #converting to float
for item in inp:
    f_list.append(float(item))

print(f_list)

   
inp1=[f_list]

clf.predict(inp1)
lst_1=clf.predict(inp1).tolist()
print(lst_1)

if(lst_1[0])==0.0:
    print("Chronic kidney disease")

# Commented out IPython magic to ensure Python compatibility.
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report,accuracy_score
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')
# %matplotlib inline

def auc_scorer(clf, X, y, model): # Helper function to plot the ROC curve
    if model=='RF':
        fpr, tpr, _ = roc_curve(y, clf.predict_proba(X)[:,1])
    elif model=='SVM':
        fpr, tpr, _ = roc_curve(y, clf.decision_function(X))
    roc_auc = auc(fpr, tpr)

    plt.figure()    # Plot the ROC curve
    plt.plot(fpr, tpr, label='ROC curve from '+model+' model (area = %0.3f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.show()

    return fpr,tpr,roc_auc

corr_df = data.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr_df, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr_df, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.title('Correlations between different predictors')
plt.show()