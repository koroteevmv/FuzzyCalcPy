# -*- coding: UTF-8 -*-

import pylab as p
import math


ACCURACY=1500
PRECISION=0.00000001


def Nedosekin(NPV, G):
    '''
    Описание
    Синтаксис:
        >>>
    Параметры:
        Параметр
            описание
    '''
    summ=0.0
    sum1=0.0
    sum2=0.0
    card=(NPV.card()*G.card())
    for npv in NPV.traversal():
        for g in G.traversal():
            chances=NPV.value(npv)*G.value(g)/card
            summ+=chances
            if npv>=g:
                sum1+=chances
            else:
                sum2+=chances
    ch=sum1/summ
    risk=sum2/summ
    return risk
