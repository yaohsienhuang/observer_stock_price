# observer_stock_price
* 使用python常用裝飾器 ＠property 搭配setter與deleter實作
* 使用design pattern中的 observer pattern(監聽模式)
* priceObser設定策略後，stockPrice中的price.setter帶入當前價格，priceObser會提供當前價格的對應操作

## 使用方式：
```python=
# 實體化 stockPrice 命名為 notifier
notifier = stockPrice()
obser_dict={
    'TSMC':{
        'buy':[
            {'price':362,'position':1},
            {'price':320,'position':2},
            {'price':290,'position':3}
        ],
        'sell':[
            {'price':500,'position':1},
            {'price':550,'position':1},
            {'price':600,'position':2}
        ],
    }
}
# 實體化 監聽者:priceObser(監聽條件)
price_obser = priceObser(obser_dict)

# 將 監聽者 加入 notifier -> 此處可建立並加入更多的 監聽者 
notifier.addObserver(price_obser)

# 將當前價格 帶入 price.setter -> priceObser會針對當前價格做出反應動作
notifier.price={'TSMC':600}
```
## Outputs:
```
TSMC 當前價格是：600
TSMC 在觀察清單中
[sell] TSMC sell 2 張
```
