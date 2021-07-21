# fmz@df1f20b5eb4d80ad7c9b8fef4e9340ac

import time
import numpy as np
import functools

#K线均价
class KLineInfo:
    index = "0-4" #当前取值范围
    avgPrice = 0 #范围内的均价
 
#根据均价存储KLineInfo; 例: 5: KLineInfo; 10: KLineInfo
AvgPriceData = {}
#macd参数
MacdData = {}
#定义时间单位
dataUnitMap = {
     0 : 60           #min
    ,1 : 60 * 60      #hour
    ,2 : 60 * 60 * 24 #day
}
#从下拉框获取对应的k线周期
unit = dataUnitMap[dataUnit]
orginKLineData = exchange.GetRecords(unit * avgPriceSkip)
#获取K线数据并反转
#KLineData = list(reversed(orginKLineData))
KLineData = orginKLineData

def main():
    getMacdParams()
    getAvgPriceByParams(avgPriceDays)
    for j in range(len(KLineData)):
        currClose = KLineData[j]['Close']#获取当前收盘价
        #分别获取各均价数据
        fiveAvgPrice = AvgPriceData["5"][j].avgPrice
        tenAvgPrice = AvgPriceData["10"][j].avgPrice
        twenAvgPrice = AvgPriceData["20"][j].avgPrice
        avgPriceArr = [fiveAvgPrice, tenAvgPrice, twenAvgPrice]
        # 检测 开多(平空)    
        if currClose > tenAvgPrice and tenAvgPrice > twenAvgPrice : #1:市价>MA10>MA20
            #获取前一周期的高点数据
            if j > 0 :
                lastHighPrice = KLineData[j - 1]['High']
                lastLowPrice = KLineData[j - 1]['Low']
                maxAvgPrice = max(avgPriceArr)
                minAvgPrice = min(avgPriceArr)
                if lastHighPrice >= maxAvgPrice and lastLowPrice <= minAvgPrice: #2:前一周期K线高点大于≥三根均线最大值，最低点≤三根均线最小值；
                    if MacdData['DIF'][j] > MacdData["DEA"][j]: #3:MACD指标的DIF>DEA；
                        #满足买入条件
                        Log("发现满足'开多'条件,当前时间点:", timestamp_to_str(KLineData[j].Time/1000) , ";收盘价:" , currClose)
                        #id = exchange.Buy(currClose, amount)
        #检测 平多(开空)
        if currClose < fiveAvgPrice and fiveAvgPrice < twenAvgPrice : #1:市价<MA5<MA20；
            if j > 0 :
                lastHighPrice = KLineData[j - 1]['High']
                lastLowPrice = KLineData[j - 1]['Low']
                maxAvgPrice = max(avgPriceArr)
                minAvgPrice = min(avgPriceArr)
                if lastHighPrice >= maxAvgPrice and lastLowPrice <= minAvgPrice: #2:前一周期K线高点大于≥三根均线最大值，最低点≤三根均线最小值；
                    if MacdData['DIF'][j] < MacdData["DEA"][j]: #3:MACD指标的DIF<DEA；
                        Log("发现满足'开空'条件,当前时间点:", timestamp_to_str(KLineData[j].Time/1000) , ";收盘价:" , currClose)

#获取均价集合中的价格（最高价求平均值）
def getAvgPriceByParams(avgPriceDays):
    for i in avgPriceDays.split(','):
        #构造数据
        list = []
        AvgPriceData[i] = list
        for j in range(len(KLineData)):
            indexEnd = int(i) - 1 + j
            targetList = KLineData[j : indexEnd] #取出范围内的数据，例：5日均线 取出0-4范围的数据
            targetRange = j , '-' , indexEnd #范围区间，例：0-4
            avgTargetPrice = functools.reduce(lambda x,y:x+y, [z['Close']for z in targetList]) / int(i) #取出每个均价下的平均值,例：5日均线 取出0-4范围内的最高价求平均值
            #构造数据
            kLineInfo = KLineInfo()
            kLineInfo.index = targetRange
            kLineInfo.avgPrice = avgTargetPrice
            list.append(kLineInfo)
        #Log(avgPriceData.unit, avgPriceData.kLineInfos)

#获取MACD参数
def getMacdParams():
    params = macdParam.split(',')
    macd = TA.MACD(orginKLineData, int(params[0]), int(params[1]), int(params[2]))
    MacdData['DIF'] = macd[0]
    MacdData['DEA'] = macd[1]
    MacdData['MACD'] = macd[2]
        
# 时间戳格式化
def timestamp_to_str(timestamp=None, format='%Y-%m-%d %H:%M:%S'):
    if timestamp:
        time_tuple = time.localtime(timestamp)  
        result = time.strftime(format, time_tuple) 
        return result
    else:
        return time.strptime(format)