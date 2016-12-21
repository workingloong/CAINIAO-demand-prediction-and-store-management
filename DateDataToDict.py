#sort the qty_alipay by date of each item
# date: 2016/05/06
# author: workingloong

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import copy
DataDF = pd.read_csv('CartStoreData.csv')
items_list = list(set(DataDF.item_id))
date_list = list(set(DataDF.date))
print len(date_list)
# tranfer store data of csv to dict
itemDataDict = {}
items_num = 0
store_list = [1,2,3,4,5]
for item in items_list:
    items_num +=1
    if items_num %100 ==0:
        print '*****************************'
    store_dict = itemDataDict.setdefault(item,{})
    itemDataDF = DataDF[DataDF.item_id == item]
    for store_id in store_list:
        init_store_array = np.zeros(444)
        itemStoreDataDF = itemDataDF[itemDataDF.store_id == store_id]
        #itemStoreDataSortedDF = itemStoreDataDF.sort(columns = 'date') 
        #dateQtyDF = itemStoreDataDF.loc[:,['date','qty_alipay']]
        dateQtyDF = itemStoreDataDF.loc[:,['date','cart_uv']]
        
        for i in range(dateQtyDF.shape[0]):
            init_store_array[dateQtyDF.iloc[i,0]] = dateQtyDF.iloc[i,1]
            #store_dict[store_code] = list(itemStoreDataSortedDF['qty_alipay'])
            store_dict[store_id] = list(init_store_array)
output = open('CartStoredateSortedData.pkl','wb')
pickle.dump(itemDataDict,output)
output.close()

# extract the national cart records for each good
items_list = list(set(DataDF.item_id))
itemDataDict = {}
items_num = 0
for item in items_list:
    items_num +=1
    if items_num %100 ==0:
        print '*****************************'
    store_list = itemDataDict.setdefault(item,[])
    itemDataDF = DataDF[DataDF.item_id == item]
    init_store_array = np.zeros(444)
    dateDF = itemDataDF.loc[:,['date','cart_uv']]
    for i in range(itemDataDF.shape[0]):
        init_store_array[dateDF.iloc[i,0]] = dateDF.iloc[i,1]
    itemDataDict[item] = list(init_store_array)
output = open('CartNationdateSortedData.pkl','wb')
pickle.dump(itemDataDict,output)
output.close()
