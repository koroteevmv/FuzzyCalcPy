# -*- coding: UTF-8 -*-
'''
Общие ресурсы библиотеки fuzzycalc
'''

ACCURACY = 1500
PRECISION = 0.00000001

def nedosekin(subset1, subset2):
    '''
    Описание
    Синтаксис:
        >>>
    Параметры:
        Параметр
            описание
    '''
    sum_ = 0.0
    sum2 = 0.0
    card = (subset1.card()*subset2.card())
    for i in subset1.traversal():
        for j in subset2.traversal():
            chances = subset1.value(i)*subset2.value(j)/card
            sum_ += chances
            if i < j:
                sum2 += chances
    risk = sum2/sum_
    return risk
