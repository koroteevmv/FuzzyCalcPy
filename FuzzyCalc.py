#coding: UTF-8
#-------------------------------------------------------------------------------
# Name:        FuzzyCalc.py
# Purpose:
#
# Author:      sejros
# Version:     0.2.3
# Created:     08.10.2010
# Modified:    15.08.2011
# Copyright:   (c) sejros 2010 - 2011
# Licence:     GNU GPL v3
#-------------------------------------------------------------------------------
#!/usr/bin/env python
'''Библиотека работы с аппаратом нечеткой логики

Данная библиотека содержит ряд модулей, призванных обеспечить использование
нечеткой логики в экономико-математическом моделировании. Она включает
следующие разделы:
    - различные носители нечетких подмножеств: от действительного интервала до
    иерархических структур
    - нечеткие подмножества: арифметические, логические операции
    - нечеткие числа, нечеткая арифметика
    - нечеткие множества, классификаторы
    - нечеткий логический вывод, нечеткие контроллеры
    - метод анализа иерархий
'''
from FuzzyCalc_Common import *
from FuzzySubset import *
from FuzzySet import *
from FuzzyDomain import *
from FuzzyNumbers import *
from FuzzyRule import *
from FuzzyController import *

##if __name__ == "__main__":
##    import doctest
####    doctest.testmod(verbose=False)
##    doctest.testmod(verbose=True)