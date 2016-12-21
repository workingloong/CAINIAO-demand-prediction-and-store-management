# cross validation for tuning parameter
# the evaluation criterion is the cost provided on TianChi
# date: 2016/05/07
# author: workingloong
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
def NationQtyToFile(item_id,store_id,preQty):
    if store_id == 0:
        store_id = 'all'
    preResultFile = open("lastTwoWeekQty.csv","a")
    resultLine = [str(item_id),str(store_id),str(preQty)]
    printline = ",".join(resultLine)
    preResultFile.writelines(printline)
    preResultFile.write('\n')
    preResultFile.close()
def loadCostQtyDict():
    f = open('itemCostDict.pkl','rb')
    itemCostDict = pickle.load(f)
    f.close()
    f = open('lastTwoWeekQty.pkl','rb')
    lastTwoWeekQtyDict = pickle.load(f)
    f.close()
    return itemCostDict,lastTwoWeekQtyDict
def DictToCsv(lastTwoWeekQtyDict):
    totalCost = 0
    for item_id in lastTwoWeekQtyDict.keys():
        for store_id in lastTwoWeekQtyDict[item_id].keys():
            preQty = lastTwoWeekQtyDict[item_id][store_id]
            NationQtyToFile(item_id,store_id,preQty)


def costCal(lastTwoWeekQtyDict,resultDict,itemCostDict):
    totalCost = 0
    print resultDict[resultDict.keys()[0]]["all"]
    for item_id in lastTwoWeekQtyDict.keys():
        for store_id in lastTwoWeekQtyDict[item_id].keys():
            error = resultDict[item_id][store_id] - lastTwoWeekQtyDict[item_id][store_id]
            if  error >0:
                totalCost += float(itemCostDict[item_id][store_id][1] )* float(error)
            else:
                totalCost +=float(itemCostDict[item_id][store_id][0]) *float( ((-1)*error) )
    return totalCost

def errorCal(lastTwoWeekQtyDict,resultDict,itemCostDict):
    totalCost = 0
    for item_id in resultDict.keys():
        for store_id in resultDict[item_id].keys():
            error = resultDict[item_id][store_id] - lastTwoWeekQtyDict[item_id][store_id]
            totalCost +=  abs(float(error))
    return totalCost
            
def QtycsvToDict(csvFileName):
    #
    #filename is the name of csv file
    print csvFileName
    f = open(csvFileName,'rb')
    record = []
    for line in f.readlines():
        curline = line.strip().split(',')
        record.append(curline)
    f.close()
    Dict = {}
    for i in range(len(record)):
        item_id = record[i][0]
        Dict.setdefault(item_id,{})
        Dict[item_id][record[i][1]]=float(record[i][2])
    return Dict
#fname = "lastTwoWeekQty.csv"
#TwoWeekDict = csvToDict(fname)
def CostCsvtoDict():
    costFile = open('config1.csv','rb')
    itemCostDict = {}
    record = []
    for line in costFile.readlines():
        curline = line.strip().split(',')
        record.append(curline)
    for i in range(len(record)):
        item_id = record[i][0]
        itemCostDict.setdefault(item_id,{})
        itemCostDict[item_id][record[i][1]]=[float(record[i][2]),float(record[i][3])]
    f = open('itemCostDict.pkl','wb')
    pickle.dump(itemCostDict,f)
    f.close()

resultFile = "SubmissionResult0513_1.csv"
resultDict = QtycsvToDict(resultFile)
TwoWeekFile = 'SubmissionResult0512.csv'
TwoWeekDict = QtycsvToDict(TwoWeekFile)
#itemCostDict,lastTwoWeekQtyDict = loadCostQtyDict()
f = open('itemCostDict.pkl','rb')
itemCostDict = pickle.load(f)
f.close()
totalCost = costCal(TwoWeekDict,resultDict,itemCostDict)
totalError = errorCal(TwoWeekDict,resultDict,itemCostDict)
print totalCost
print totalError
