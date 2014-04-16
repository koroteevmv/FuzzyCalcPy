# -*- coding: UTF-8 -*-
'''
Модуль, описывающий различные типы носителей нечетких множеств, а также
реализующий функциональность нечетких правил логического вывода.
'''

from .common import ACCURACY

class Domain(object):
    '''
        Абстрактный класс, реализующий интерфейс носителя
        нечеткого множества. Смысловую нагрузку несут подклассы этого класса,
        представляющие различные виды носителей. Преимуществом такого подхода
        является его универсальность: в качестве носителя при определении
        нечеткого множества можно задавать действительный интервал,
        целочисленный интервал, в принципе, любую итерируемую структуру.
    '''
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def char(self):
        '''
        Синтаксис:
        '''
        for i in self:
            print i

class RationalRange(Domain):
    '''
    Данный класс реализует носитель нечеткого подмножества в виде
    отрезка действительной оси. В качестве параметров конструктор класса
    принимает значения начала и конца интервала, а также параметр "точность" -
    целое число, определяющее количество проходов при расчете нечетких
    функционалов численным методом. Это число является компромиссом между
    точностью и скоростью подсчета, поэтому там, где это возможно,
    численный расчет нечетких функционалов заменен аналитическими выражениями.

        Синтаксис:

            >>> B=RationalRange(begin=0.0, end=3.0, acc=3)
            >>> for i in B: print i
            0.0
            1.0
            2.0
            3.0

            >>> B=RationalRange(begin=0.0, end=3.0, acc=8)
            >>> for i in B: print i
            0.0
            0.375
            0.75
            1.125
            1.5
            1.875
            2.25
            2.625
            3.0
            >>> A=Triangle(1.0, 1.5, 2.5, domain=B)
            >>> print A
            1.65441176471
            >>> A.char()
            0.0 0.0
            0.375 0.0
            0.75 0.0
            1.125 0.25
            1.5 1.0
            1.875 0.625
            2.25 0.25
            2.625 0.0
            3.0 0.0
    '''
    begin = 0.0
    end = 1.0
    delta = 0.01
    acc = ACCURACY
    def __init__(self, begin=0.0, end=1.0, acc=ACCURACY):
        self.begin = float(begin)
        self.end = float(end)
        self.acc = acc
    def __iter__(self):
        if self.begin == self.end:
            for i in range(self.acc):
                yield self.begin
        else:
            self.delta = (self.end-self.begin)/(self.acc)
            i = self.begin
            while i < self.end+self.delta:
                yield i
                i += self.delta

class IntegerRange(Domain):
    '''
    Класс, моделирующий носитель нечеткого множества в виде целочисленного
    интервала. По сути, является частным случаем предыдущего класса
    (см. RationalRange), когда точность равна разнице границ интервала.

       Синтаксис:

            >>> B=IntegerRange(begin=0.0, end=3.0)
            >>> for i in B: print i
            0.0
            1.0
            2.0
            3.0

            >>> A=Trapezoidal(begin=0.0, begin_tol=2.0,
                                end_tol=2.0, end=3.0, domain=B)
            >>> print A
            1.66666666667
            >>> A.char()
            0.0 0.0
            1.0 0.5
            2.0 1.0
            3.0 -0.0

    '''
    begin = 0
    end = 100
    def __init__(self, begin=0.0, end=1.0):
        self.begin = begin
        self.end = end
    def __iter__(self):
        i = self.begin
        while i < self.end+1:
            yield i
            i += 1


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    #~ doctest.testmod(verbose=True)
