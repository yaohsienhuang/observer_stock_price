from abc import ABCMeta, abstractmethod

class stockPrice:
    def __init__(self):
        self._prices = None
        self._observers = []
    
    @property
    def price(self):
        return self._prices

    @price.setter
    def price(self, prices):
        self._prices = prices
        for name,price in self._prices.items():
            print(f"{name} 當前價格是：{str(price)}")
        self.notifies()
    
    @price.deleter
    def price(self):
        del self._prices
        print('delete complite')
    
    def addObserver(self, observer):
        self._observers.append(observer)
        
    def notifies(self):
        for obser in self._observers:
            obser.update(self)

class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, stockPrice):
        pass

class priceObser(Observer):
    def __init__(self,obser_dict):
        self.obser_dict=obser_dict
        
    def update(self, stockPrice):
        for name,now_price in stockPrice.price.items():
            if name in self.obser_dict.keys():
                print(f'{name} 在觀察清單中')
                
                alert=False
                for action,detail in self.obser_dict[name].items():
                    prices,positions=[a['price'] for a in detail],[a['position'] for a in detail]
                    if now_price in prices:
                        position=positions[prices.index(now_price)]
                        print(f'[{action}] {name} {action} {position} 張')
                        alert=True
                        
                if alert==False:
                    print('未觸發任何條件，不做任何動作') 
            else:
                print(f'{name} 不在觀察清單中')

if __name__=='__main__':
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
    
    # 將 監聽者 加入 notifier
    notifier.addObserver(price_obser)

    # 將當前價格 帶入 price.setter -> priceObser會針對當前價格做出反應動作
    notifier.price={'TSMC':600}



