
# -*- coding: UTF-8 -*- 

class Chart():
    values=[]
    labels=[]
    def __init__(self, values, labels):
       self.values=values
       self.labels=labels

def cart_20131221(domain_eCommerce, text_at, text_shipping):
    result=None
    if domain_eCommerce==1:
        result=1
    elif domain_eCommerce==0:
        if text_at==1:
            result=0
        elif text_at==0:
            if text_shipping==1:
                result=1
            else:
                result=0
    return result

