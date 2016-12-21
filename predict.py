# predict the sales on the next 2 weeks
# date: 2016/05/09
# author: workingloong

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle 
import math
from scipy import  stats
import statsmodels.api as sm
from sklearn import linear_model

def QtyDataPlot(QtyData):
    xTicks = np.linspace(0,450,10)
    xTicks[9] = 443
    xlabels = []
    for i in range(len(xTicks)):
        xlabels.append(dateCodeDict[int(xTicks[i])])
    xlabels = tuple(xlabels)
    plt.figure()
    x = dateCodeDict.values()
    plt.plot(QtyData, label = "Qty")
    plt.legend(loc = 'upper right')
    plt.show()
    
f= open('dateCodeDict.pkl','rb')
dateCodeDict = pickle.load(f)
f.close()
f= open('itemCostDict.pkl','rb')
itemCostDict = pickle.load(f)
f.close()
f= open('QtyStoredateSortedData.pkl','rb')
QtyStoreDataDict = pickle.load(f)
f.close()
f= open('QtyNationdateSortedData.pkl','rb')
QtyNationDataDict = pickle.load(f)
f.close()
f= open('CartStoredateSortedData.pkl','rb')
CartStoreDataDict = pickle.load(f)
f.close()
f= open('CartNationdateSortedData.pkl','rb')
CartNationDataDict = pickle.load(f)
f.close()

def OLSpredict(temp):
    x= []
    for i in range(1,len(temp)+1):
        x.append([i])
    clf = linear_model.LinearRegression()
    clf.fit(x,temp)
    Xnew = []
    for i in range(len(temp)+1,len(temp)+15):
        Xnew.append([i])
    clfPre = clf.predict(Xnew)
    return sum( clfPre)

def SlopeCal(temp):
    x= []
    for i in range(1,len(temp)+1):
        x.append([i])
    clf = linear_model.LinearRegression()
    clf.fit(x,temp)
    return clf.coef_
    
def QtyStorePredict(QtyData,CartData,itemCost):
    temp = np.array(QtyData)
    sortedTemp = sorted(temp,reverse = True)
    for i in range(6):
        temp[temp == sortedTemp[i]] = sortedTemp[40]
    #QtyPre = OLSpredict(temp[-14:])
    QtyPre = temp[-14:].mean()*14
    if itemCost[0]>itemCost[1]:
            QtyPre = QtyPre*1.3
    else:
            QtyPre = QtyPre*0.9
    return QtyPre
    
def QtyNationPredict(QtyData,CartData,itemCost):
    temp = np.array(QtyData)
    sortedTemp = sorted(temp,reverse = True)
    k = SlopeCal(CartData[-4:])
    for i in range(6):
        temp[temp == sortedTemp[i]] = sortedTemp[40]
        QtyPre = temp[-14:].mean()*14
        #QtyPre = OLSpredict(temp[-14:])
    if itemCost[0]>itemCost[1]:
        if k>-1:
            QtyPre = QtyPre*1.3
        else:
            QtyPre = QtyPre*0.9
    else:
        if k>-1:
            QtyPre = QtyPre*1.3
        else:
            QtyPre = QtyPre*0.9
    return QtyPre

def NationQtyToFile(item_id,store_id,preQty):
    if store_id == 0:
        store_id = 'all'
    #preResultFile = open("lastTwoWeekPred01.csv","a")
    preResultFile = open("SubmissionResult0515.csv","a")
    resultLine = [str(item_id),str(store_id),str(preQty)]
    printline = ",".join(resultLine)
    preResultFile.writelines(printline)
    preResultFile.write('\n')
    preResultFile.close()

#f = open("lastTwoWeekPred01.csv","wb")
f = open("SubmissionResult0515.csv","wb")
f.close()
itemList = np.array(QtyStoreDataDict.keys())
LessItemList = []
MoreItemList = []
for i in range(len(itemList)):
    item_id = itemList[i]
    for store_id in QtyStoreDataDict[item_id].keys():
        itemCost = itemCostDict[str(item_id)][str(store_id)]
        QtyData = np.array(QtyStoreDataDict[item_id][store_id])[0:]
        CartData = np.array(CartStoreDataDict[item_id][store_id])[0:]
        QtyPrediction = QtyStorePredict(QtyData,CartData,itemCost)
        NationQtyToFile(item_id,store_id,QtyPrediction )
for i in range(len(itemList)):
    item_id = itemList[i]
    QtyData = np.array(QtyNationDataDict[item_id])[0:]
    CartData = np.array(CartNationDataDict[item_id])[0:]
    itemCost = itemCostDict[str(item_id)]['all']
    QtyPrediction = QtyNationPredict(QtyData,CartData,itemCost)
    NationQtyToFile(item_id,0,QtyPrediction )
