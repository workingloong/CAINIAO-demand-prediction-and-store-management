# extract the all date
# date: 2016/05/06
# author: workingloong
itemList = itemQtyDataDict.keys()
nationTrainData ={}
nationTestData ={}
for item_id in itemList:
    nationTrainData.setdefault(item_id,[])
    HistoryTimeQty = sum(itemQtyDataDict[item_id][65:79])
    monthAvgQty = 7 * np.mean(itemQtyDataDict[item_id][402:430])
    PreTwoWeekQty = sum(itemQtyDataDict[item_id][416:430])
    CartNum = sum(itemCartDataDict[item_id][424:430])
    CartQty = CartNum - sum(itemQtyDataDict[item_id][424:430])
    PreTwoWeekFlow = sum(itemFlowDataDict[item_id][416:430])
    PreTwoWeekClick = sum(itemClickDataDict[item_id][416:430])
    CartAdd = sum(itemCartDataDict[item_id][429:430]) >sum(itemCartDataDict[item_id][428:429])
    Qty =  sum(itemQtyDataDict[item_id][430:])
    nationTrainData[item_id]=[HistoryTimeQty, monthAvgQty,
		PreTwoWeekQty,CartNum,CartQty,PreTwoWeekFlow,PreTwoWeekClick,CartAdd,Qty]
    
    nationTestData.setdefault(item_id,[])
    HistoryTimeQty = sum(itemQtyDataDict[item_id][79:93])
    monthAvgQty = 7 * np.mean(itemQtyDataDict[item_id][430:444])
    PreTwoWeekQty = sum(itemQtyDataDict[item_id][430:444])
    CartNum = sum(itemCartDataDict[item_id][434:444])
    CartQty = CartNum - sum(itemQtyDataDict[item_id][434:444])
    PreTwoWeekFlow = sum(itemFlowDataDict[item_id][430:444])
    PreTwoWeekClick = sum(itemClickDataDict[item_id][430:444])
    CartAdd = sum(itemCartDataDict[item_id][443:444]) >sum(itemCartDataDict[item_id][442:443])
    nationTestData[item_id]=[ HistoryTimeQty,monthAvgQty,
		PreTwoWeekQty,CartNum,CartQty,PreTwoWeekFlow,PreTwoWeekClick,CartAdd]
f = open('HnationTrainDataDict.pkl','wb')
pickle.dump(nationTrainData,f)
f.close()
f = open('HnationTestDataDict.pkl','wb')
pickle.dump(nationTestData,f)
f.close()
