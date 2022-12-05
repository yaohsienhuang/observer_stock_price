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
                print(f'[價格提醒] {name} 在條件單中')
                
                alert=False
                for action,detail in self.obser_dict[name].items():
                    prices,positions=[a['price'] for a in detail],[a['position'] for a in detail]
                    if now_price in prices:
                        position=positions[prices.index(now_price)]
                        print(f'[價格提醒] {name} 觸發條件({action}:{now_price}元,{position}張) 建議 {action} {position} 張')
                        alert=True
                        
                if alert==False:
                    print('[價格提醒] 未觸發任何條件，不做任何動作') 
            else:
                print(f'[價格提醒] {name} 不在條件單中')

class profitObser(Observer):
    def __init__(self,obser_dict):
        self.obser_dict=obser_dict
        self.avg_dict=self.avg_price()
        
    def update(self, stockPrice):
        for name,now_price in stockPrice.price.items():
            if name in self.obser_dict.keys():
                price,position=self.avg_dict[name]['price'],self.avg_dict[name]['position']
                profit=(now_price-price)*position*1000
                profit_ratio=round((now_price-price)/price,1)
                print(f'[部位提醒] {name} 持有 {position} 張部位，平均價格 {price}，平均獲利 {profit_ratio} %，共獲利 {profit} 元。')
            else:
                print(f'[部位提醒] {name} 未持有部位')
                    
        
    def avg_price(self):
        avg_dict=dict()
        for name,detail in self.obser_dict.items():
            sum_product=sum([a['price']*a['position'] for a in detail])
            sum_position=sum([a['position'] for a in detail])
            avg_price=round(sum_product/sum_position,1)
            avg_dict[name]={'price':avg_price,'position':sum_position}
        return avg_dict
            
        

if __name__=='__main__':
    # 實體化 stockPrice 命名為 notifier
    notifier = stockPrice()
    
    # 實體化 監聽者:priceObser(監聽條件)
    conditional_dict={
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
    conditional_obser = priceObser(conditional_dict)
    
    # 實體化 監聽者:profitObser(監聽條件)
    poistion_dict={
        'TSMC':[
            {'price':245,'position':1},
            {'price':276,'position':2},
            {'price':324,'position':1}
        ]
    }
    profit_obser = profitObser(poistion_dict)
    
    # 將 監聽者 加入 notifier
    notifier.addObserver(profit_obser)
    notifier.addObserver(conditional_obser)
    

    # 將當前價格 帶入 price.setter -> priceObser會針對當前價格做出反應動作
    notifier.price={'TSMC':495}



