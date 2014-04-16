# -*- coding: UTF-8 -*-
''' Модуль для работы с нечеткими числами

Модуль реализует функциональность аппарата нечеткой логики в части работы с
нечеткими числами. Он включает:
    - описание
'''

from .subset import Subset
from .domain import RationalRange
from math import tanh, log, pi, cos, exp, cosh

LINE = lambda c: lambda a, b: lambda x: abs((x-b)/(a-b))**c
LINES = lambda c: lambda a, b: lambda x: abs((x-b)/(a-b)) ** \
                        log(0.5, ((c-b)/(a-b)))
QUAD = lambda c: lambda a, b: lambda x: abs(1-((x-a)/abs(b-a))**2)**c
QUADS = lambda c: lambda a, b: lambda x: abs(1-((x-a)/abs(b-a))**2) ** \
                        log(0.5, (1-((c-a)/abs(b-a))**2))
LAPL = lambda c: lambda a, b: lambda x: exp(-abs(x-a)*c/abs(b-a))
LAPLS = lambda c: lambda a, b: lambda x: exp(abs(x-a)*log(0.5)/abs(c-a))
TANG = lambda c: lambda a, b: lambda x: (1+tanh(-((x-a)/(abs(b-a)/c))**2))
GAUS = lambda c: lambda a, b: lambda x: (exp(-((x-a)**2)/c**2))
CAUC = lambda c: lambda a, b: lambda x: (1/(1+((x-a)*c/abs(b-a))**2))
LOGI = lambda c: lambda a, b: lambda x: (2/(1+exp(((x-a)*c/abs(b-a))**2)))
SECG = lambda c: lambda a, b: lambda x: (1/cosh((x-a)/(b-a)))
TANGS = lambda c: lambda a, b: lambda x: (1+tanh(-((x-a)/abs(b-a))**2)) ** \
                        log(0.5, (1+tanh(-((c-a)/abs(b-a))**2)))
GAUSS = lambda c: lambda a, b: lambda x: exp(((x-a)**2)*log(0.5) / ((c-a)**2))
CAUCS = lambda c: lambda a, b: lambda x: (1/ (1+ ((x-a) / (c-a))**2))
LOGIS = lambda c: lambda a, b: lambda x: (2/(1+exp(((x-a)/abs(b-a))**2))) ** \
                        log(0.5, ((2/(1+exp(((c-a)/abs(b-a))**2)))))
SECGS = lambda c: lambda a, b: lambda x: (1/cosh((x-a)/abs(b-a))) ** \
                        log(0.5, (1/cosh((c-a)/abs(b-a))))
COSS = lambda c: lambda a, b: lambda x: ((1+cos(pi*(x-a)/abs(b-a)))/2) ** \
                        log(0.5, ((1+cos(pi*(c-a)/abs(b-a)))/2))
POINT = lambda a, b: lambda x: 1

class TrapExt(Subset):
    '''
    Нечеткие числа в обобщенно-трапециевидной форме.
    Синтаксис:
        >>> A = TrapExt(begin = 1.0,
                         end = 4.0,
                         begin_tol = 2.0,
                         end_tol = 3.0,
                         left = LINE(3.0),
                         right = LINE(1.0))

    Первые 4 параметра аналогичны параметрам конструктора трапециевидных
    нечетких чисел (см. Trapezoidal). Два последних определяют форму функций
    скатов - левого и правого. Для этого используется ряд лямбда-выражений,
    включенных в настоящую библиотеку. При их использовании следует
    указать параметр функции - число, характеризующее степень плавности ската.
    Функцию каждого ската выбирает пользователь из следующих альтернатив:
        LINE
            линейный (степенной) скат
        quad
            квадратический (параболический, полукруговой) скат
        lapl
            скат в виде лаплассианы
        tang
            тангенсоида
        gaus
            гауссиана
        cauc
            скат в виде распределения Коши
        logi
            логистическая кривая
        secg
            скат в виде гиперболического секанса
    '''

    def __init__(self, begin=0.0,
                       begin_tol=0.0,
                       end_tol=0.0,
                       end=0.0,
                       left=LINE(1),
                       right=LINE(1)):

        self.begin = float(begin)
        self.begin_tol = float(begin_tol)
        self.end_tol = float(end_tol)
        self.end = float(end)
        self.points = {}
        self.points[begin] = 0.0
        self.points[begin_tol] = 1.0
        self.points[end_tol] = 1.0
        self.points[end] = 0.0
        self.left = left
        self.right = right
        self.l_skat = left(self.begin_tol, self.begin)
        self.r_skat = right(self.end_tol, self.end)
        self.domain = RationalRange(begin, end)

        if begin == begin_tol:
            self.left = POINT
            self.l_skat = POINT(self.begin_tol, self.begin)
        if end == end_tol:
            self.right = POINT
            self.r_skat = POINT(self.end_tol, self.end)

    def value(self, key):
        '''
        см. fuzzycalc.subset.Subset.value()
        '''
        if key <= self.begin:
            return 0.0
        elif self.begin < key < self.begin_tol:
            return self.l_skat(key)
        elif self.begin_tol <= key <= self.end_tol:
            return 1.0
        elif self.end_tol < key <= self.end:
            return self.r_skat(key)
        elif self.end < key:
            return 0.0
        else:
            return -1

    def fuzziness(self):
        tol = self.end_tol - self.begin_tol
        supp = self.end - self.begin
        lvl = Subset.level(self, 0.5)
##        lvl = self.level(0.5)
        mid = lvl.b - lvl.a
        return tol*(1-abs(2.0*mid-supp-tol)/(0-tol))

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            other = TrapExt(begin=other,
                             end=other,
                             begin_tol=other,
                             end_tol=other)

        res_begin = min(self.begin + other.begin,
                        self.begin + other.end,
                        self.end + other.begin,
                        self.end + other.end)
        res_begin_tol = min(self.begin_tol + other.begin_tol,
                            self.begin_tol + other.end_tol,
                            self.end_tol + other.begin_tol,
                            self.end_tol + other.end_tol)
        res_end_tol = max(self.begin_tol+other.begin_tol,
                            self.begin_tol+other.end_tol,
                            self.end_tol+other.begin_tol,
                            self.end_tol+other.end_tol)
        res_end = max(self.begin+other.begin,
                        self.begin+other.end,
                        self.end+other.begin,
                        self.end+other.end)

        res_left = lambda x, y: lambda z: \
                        self.left(self.begin_tol, self.begin)\
                        (self.begin+(self.begin_tol-self.begin)*\
                        (z-res_begin)/(res_begin_tol-res_begin)) * \
                        other.left(other.begin_tol, other.begin)\
                        (other.begin+(other.begin_tol-other.begin)*\
                        (z-res_begin)/(res_begin_tol-res_begin))
        res_right = lambda x, y: lambda z: \
                        self.right(self.end_tol, self.end)\
                        (self.end_tol+(self.end-self.end_tol)*\
                        (z-res.end_tol)/(res_end-res_end_tol)) * \
                        other.right(other.end_tol, other.end)\
                        (other.end_tol+(other.end-other.end_tol)*\
                        (z-res_end_tol)/(res_end-res_end_tol))

        res = TrapExt(begin=res_begin, begin_tol=res_begin_tol,
                        end_tol=res_end_tol, end=res_end,
                        left=res_left, right=res_right)
        return res

    def __sub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            other = TrapExt(begin=other, end=other,
                                begin_tol=other, end_tol=other)

        res_begin = min(self.begin-other.begin,
                        self.begin-other.end,
                        self.end-other.begin,
                        self.end-other.end)
        res_begin_tol = min(self.begin_tol-other.begin_tol,
                            self.begin_tol-other.end_tol,
                            self.end_tol-other.begin_tol,
                            self.end_tol-other.end_tol)
        res_end_tol = max(self.begin_tol-other.begin_tol,
                            self.begin_tol-other.end_tol,
                            self.end_tol-other.begin_tol,
                            self.end_tol-other.end_tol)
        res_end = max(self.begin-other.begin,
                        self.begin-other.end,
                        self.end-other.begin,
                        self.end-other.end)

        res_left = lambda x, y: lambda z: self.left(self.begin_tol, self.begin)\
                                    (self.begin+(self.begin_tol-self.begin)*\
                                    (z-res_begin)/(res_begin_tol-res_begin)) * \
                                    other.left(other.begin_tol, other.begin)\
                                    (other.begin+(other.begin_tol-other.begin)*\
                                    (z-res_begin)/(res_begin_tol-res_begin))
        res_right = lambda x, y: lambda z: self.right(self.end_tol, self.end)\
                                    (self.end_tol+(self.end-self.end_tol)*\
                                    (z-res_end_tol)/(res_end-res_end_tol)) * \
                                    other.right(other.end_tol, other.end)\
                                    (other.end_tol+(other.end-other.end_tol)*\
                                    (z-res_end_tol)/(res_end-res_end_tol))

        res = TrapExt(begin=res_begin, begin_tol=res_begin_tol,
                        end_tol=res_end_tol, end=res_end,
                        left=res_left, right=res_right)
        return res

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            other = TrapExt(begin=other, end=other,
                                begin_tol=other, end_tol=other)

        res_begin = min(self.begin*other.begin,
                        self.begin*other.end,
                        self.end*other.begin,
                        self.end*other.end)
        res_begin_tol = min(self.begin_tol*other.begin_tol,
                            self.begin_tol*other.end_tol,
                            self.end_tol*other.begin_tol,
                            self.end_tol*other.end_tol)
        res_end_tol = max(self.begin_tol*other.begin_tol,
                            self.begin_tol*other.end_tol,
                            self.end_tol*other.begin_tol,
                            self.end_tol*other.end_tol)
        res_end = max(self.begin*other.begin,
                        self.begin*other.end,
                        self.end*other.begin,
                        self.end*other.end)

        res_left = lambda x, y: lambda z: \
                        self.left(x, y)(z)*other.left(x, y)(z)
        res_right = lambda x, y: lambda z: \
                        self.right(x, y)(z)*other.right(x, y)(z)

        res = TrapExt(begin=res_begin, begin_tol=res_begin_tol,
                        end_tol=res_end_tol, end=res_end,
                        left=res_left, right=res_right)
        return res

    def __div__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            other = TrapExt(begin=other, end=other,
                                begin_tol=other, end_tol=other)

        res_begin = min(self.begin/other.begin,
                        self.begin/other.end,
                        self.end/other.begin,
                        self.end/other.end)
        res_begin_tol = min(self.begin_tol/other.begin_tol,
                            self.begin_tol/other.end_tol,
                            self.end_tol/other.begin_tol,
                            self.end_tol/other.end_tol)
        res_end_tol = max(self.begin_tol/other.begin_tol,
                            self.begin_tol/other.end_tol,
                            self.end_tol/other.begin_tol,
                            self.end_tol/other.end_tol)
        res_end = max(self.begin/other.begin,
                        self.begin/other.end,
                        self.end/other.begin,
                        self.end/other.end)

        res_left = lambda x, y: lambda z: \
                        self.left(x, y)(z)*other.left(x, y)(z)
        res_right = lambda x, y: lambda z: \
                        self.right(x, y)(z)*other.right(x, y)(z)

        res = TrapExt(begin=res_begin, begin_tol=res_begin_tol,
                        end_tol=res_end_tol, end=res_end,
                        left=res_left, right=res_right)
        return res

    def __radd__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            other = TrapExt(begin=other, end=other,
                                begin_tol=other, end_tol=other)

        res_begin = min(self.begin+other.begin,
                        self.begin+other.end,
                        self.end+other.begin,
                        self.end+other.end)
        res_begin_tol = min(self.begin_tol+other.begin_tol,
                            self.begin_tol+other.end_tol,
                            self.end_tol+other.begin_tol,
                            self.end_tol+other.end_tol)
        res_end_tol = max(self.begin_tol+other.begin_tol,
                            self.begin_tol+other.end_tol,
                            self.end_tol+other.begin_tol,
                            self.end_tol+other.end_tol)
        res_end = max(self.begin+other.begin,
                        self.begin+other.end,
                        self.end+other.begin,
                        self.end+other.end)

        res_left = lambda x, y: lambda z: self.left(self.begin_tol, self.begin)\
                                    (self.begin+(self.begin_tol-self.begin)*\
                                    (z-res_begin)/(res_begin_tol-res_begin)) * \
                                    other.left(other.begin_tol, other.begin)\
                                    (other.begin+(other.begin_tol-other.begin)*\
                                    (z-res_begin)/(res_begin_tol-res_begin))
        res_right = lambda x, y: lambda z: self.right(self.end_tol, self.end)\
                                    (self.end_tol+(self.end-self.end_tol)*\
                                    (z-res_end_tol)/(res_end-res_end_tol)) * \
                                    other.right(other.end_tol, other.end)\
                                    (other.end_tol+(other.end-other.end_tol)*\
                                    (z-res_end_tol)/(res_end-res_end_tol))

        res = TrapExt(begin=res_begin, begin_tol=res_begin_tol,
                        end_tol=res_end_tol, end=res_end,
                        left=res_left, right=res_right)
        return res

    def __rsub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            other = TrapExt(begin=other, end=other,
                                begin_tol=other, end_tol=other)

        res_begin = min(self.begin-other.begin,
                        self.begin-other.end,
                        self.end-other.begin,
                        self.end-other.end)
        res_begin_tol = min(self.begin_tol-other.begin_tol,
                            self.begin_tol-other.end_tol,
                            self.end_tol-other.begin_tol,
                            self.end_tol-other.end_tol)
        res_end_tol = max(self.begin_tol-other.begin_tol,
                            self.begin_tol-other.end_tol,
                            self.end_tol-other.begin_tol,
                            self.end_tol-other.end_tol)
        res_end = max(self.begin-other.begin,
                        self.begin-other.end,
                        self.end-other.begin,
                        self.end-other.end)

        res_left = lambda x, y: lambda z: self.left(self.begin_tol, self.begin)\
                                    (self.begin+(self.begin_tol-self.begin)*\
                                    (z-res_begin)/(res_begin_tol-res_begin)) * \
                                    other.left(other.begin_tol, other.begin)\
                                    (other.begin+(other.begin_tol-other.begin)*\
                                    (z-res_begin)/(res_begin_tol-res_begin))
        res_right = lambda x, y: lambda z: self.right(self.end_tol, self.end)\
                                    (self.end_tol+(self.end-self.end_tol)*\
                                    (z-res_end_tol)/(res_end-res_end_tol)) * \
                                    other.right(other.end_tol, other.end)\
                                    (other.end_tol+(other.end-other.end_tol)*\
                                    (z-res_end_tol)/(res_end-res_end_tol))

        res = TrapExt(begin=res_begin, begin_tol=res_begin_tol,
                        end_tol=res_end_tol, end=res_end,
                        left=res_left, right=res_right)
        return res

    def __rmul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            other = TrapExt(begin=other, end=other,
                                begin_tol=other, end_tol=other)

        res_begin = min(self.begin*other.begin,
                        self.begin*other.end,
                        self.end*other.begin,
                        self.end*other.end)
        res_begin_tol = min(self.begin_tol*other.begin_tol,
                            self.begin_tol*other.end_tol,
                            self.end_tol*other.begin_tol,
                            self.end_tol*other.end_tol)
        res_end_tol = max(self.begin_tol*other.begin_tol,
                            self.begin_tol*other.end_tol,
                            self.end_tol*other.begin_tol,
                            self.end_tol*other.end_tol)
        res_end = max(self.begin*other.begin,
                        self.begin*other.end,
                        self.end*other.begin,
                        self.end*other.end)

        res_left = lambda x, y: lambda z: \
                        self.left(x, y)(z)*other.left(x, y)(z)
        res_right = lambda x, y: lambda z: \
                        self.right(x, y)(z)*other.right(x, y)(z)

        res = TrapExt(begin=res_begin, begin_tol=res_begin_tol,
                        end_tol=res_end_tol, end=res_end,
                        left=res_left, right=res_right)
        return res

    def __rdiv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            other = TrapExt(begin=other, end=other,
                                begin_tol=other, end_tol=other)

        res_begin = min(self.begin/other.begin,
                        self.begin/other.end,
                        self.end/other.begin,
                        self.end/other.end)
        res_begin_tol = min(self.begin_tol/other.begin_tol,
                            self.begin_tol/other.end_tol,
                            self.end_tol/other.begin_tol,
                            self.end_tol/other.end_tol)
        res_end_tol = max(self.begin_tol/other.begin_tol,
                            self.begin_tol/other.end_tol,
                            self.end_tol/other.begin_tol,
                            self.end_tol/other.end_tol)
        res_end = max(self.begin/other.begin,
                        self.begin/other.end,
                        self.end/other.begin,
                        self.end/other.end)

        res_left = lambda x, y: lambda z: \
                        self.left(x, y)(z)*other.left(x, y)(z)
        res_right = lambda x, y: lambda z: \
                        self.right(x, y)(z)*other.right(x, y)(z)

        res = TrapExt(begin=res_begin, begin_tol=res_begin_tol,
                        end_tol=res_end_tol, end=res_end,
                        left=res_left, right=res_right)
        return res

class TrFN(TrapExt):
    '''
    Трапециевидное нечеткое число
    '''

    def __init__(self, a, b, c, d):
        TrapExt.__init__(self, a, b, c, d, LINE(1), LINE(1))
##        super(TrFN, self).__init__(a, b, c, d, LINE(1), LINE(1))

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    #~ doctest.testmod(verbose=True)
