# coding:utf8

class medal:

    def __init__(self,name='',gold=0,silver=0,copper=0):
        self.name = name
        self.gold = gold
        self.silver = silver
        self.copper = copper

    # 获得名次# 获得名次
    def get_place(self,rank):
        if rank == 1:
            self.gold += 1
        if rank == 2:
            self.silver += 1
        if rank == 3:
            self.copper += 1

    # 总奖牌数
    # count 是计算奖牌总数的方法。实例代码中，通过一个装饰器 @property，将这个类方法转成只读的属性，称为属性函数。在调用时像属性一样，无需再加括号。
    @property
    def count(self):
        return self.gold+self.silver+self.copper

    # 对象的字符串表示，被print时显示
    def __str__(self):
        return '%s :gold %d,silver %d,copper %d,total %d' %(self.name,self.gold,self.silver,self.copper,self.count)

if __name__ == '__main__':
    china = medal("中国", 26, 18, 26)
    us = medal("美国", 46, 37, 38)
    uk = medal("英国", 27, 23, 17)
    print(china)
    print(us)
    print(uk)
    print("中国获得一个冠军：")
    china.get_place(1)
    print(china)
    medal_list = [us, uk, china]
    print("按金牌数排序：")
    # sorted 函数通过指定不同的属性（gold、count）作为排序依据，可实现按照不同方式的排序
    order_by_count = sorted(medal_list, key=lambda x:x.gold, reverse=True)
    for o in order_by_count:
        print(o)
    print("按奖牌数排序：")
    order_by_count = sorted(medal_list, key=lambda x:x.count, reverse=True)
    for o in order_by_count:
        print(o)