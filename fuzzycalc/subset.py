# -*- coding: UTF-8 -*-

'''
Модуль реализует набор базовых типов, представляющих разные виды нечетких
подмножеств.
'''

from .common import ACCURACY
from .domain import RationalRange, IntegerRange

import pylab as p
import math


class Subset(object):
    '''
    Реализует функциональность нечеткого подмножества общего вида.
    Имеет атрибуты, указывающие начало и конец интервала
    определения подмножества (для подмножеств, определенных на R).

    >>> A=Subset(0.0, 1.0)
    >>> A.begin
    0.0
    >>> A.end
    1.0

    Attributes:
        values
        points
        domain

    '''

    def __init__(self, begin=0.0,
                        end=1.0,
                        domain=None):

        if not domain:
            domain = RationalRange(begin, end)

        self.domain = domain
        self.values = {}
        self.points = {}

        self.values[self.domain.begin] = 0.0
        self.values[self.domain.end] = 0.0
        self.points[self.domain.begin] = 0.0
        self.points[self.domain.end] = 0.0

    def value(self, key):
        '''
        Возвращает уровень принадлежности точки нечеткому подмножеству.
        Данный метод непосредственно и является программной имплементацией
        функции принадлежности.
        >>> A=Gaussian(1.0, 1.0)
        >>> A.value(0.5)
        0.8825
        >>> A.value(1.5)
        0.8825
        >>> A.value(1.0)
        1.0
        >>> A.value(0.0)
        0.60653
        '''
        try:
            return self.values[key]
        except KeyError:
            sort = sorted(self.values.keys())
            sort1 = sorted(self.values.keys())
            sort1.pop(0)
            for i, j in zip(sort, sort1):
                if i < key < j:
                    return round((self.value(i) + self.value(j))/2, 4)
                else:
                    return 0.0

    def char(self):
        '''
        Выводит на экран список элементов носителя и соответствующих им значений
        нечеткого множества. Шаг перебора непрерывного носителя совпадает с
        частотой дискретизации при численных вычислениях
        Синтаксис:
            >>> A=Triangle(1.0, 2.0, 4.0)
            >>> A.Domain.acc=5
            >>> A.char()
            1.0 0.0
            1.6 0.6
            2.2 0.9
            2.8 0.6
            3.4 0.3
            4.0 -0.0

        '''
        for i in self.domain:
            print i, self.value(i)

    def normalize(self):
        '''
        Возвращает нормированное по высоте нечеткое множество.
        Синтаксис:
            >>> A=Triangle(1.0, 2.0, 4.0)
            >>> A.Domain.acc=5
            >>> B=A*0.5
            >>> print B.card()  #doctest: +SKIP
            1.49985
            >>> print A.card()  #doctest: +SKIP
            29.997
            >>> C=B.normalize()
            >>> print C.card()  #doctest: +SKIP
            2.97
            >>> print round(B.value(B.mode()), 2)
            0.5
            >>> print round(C.value(C.mode()), 2)
            1.0

        '''
        sup = self.sup()
        if sup == 0.0:
            return self
        res = Subset(self.domain.begin, self.domain.end)
        for i in self.domain:
            res[i] = self.value(i)/sup
        return res

    def sup(self):
        sup = 0.0
        for i in self.domain:
            if self.value(i) > sup:
                sup = self.value(i)
        return sup
    def plot(self, verbose=True):
        '''
        Отображает нечеткое множество графически. Только для нечетких множеств,
        определенных на носителе типа RationalRange. Параметр verbose
        определяет отображение на графике дополнительной информации.
        Синтаксис:
            >>> A=Triangle(2.5, 3.8, 10.2)
            >>> A.plot()
            >>> A.plot(verbose=True)
            >>> A.plot(verbose=False)

        '''
        x = []
        y = []
        for i in self.domain:
            x.append(i)
            y.append(self.value(i))
        p.plot(x, y)
        if isinstance(self.domain, IntegerRange):
        # TODO построение графиков НПМ на целочисленных интервалах.
            pass
        p.plot(self.domain.begin, 1.2)
        p.plot(self.domain.end+(self.domain.end-self.domain.begin)/3, -0.1)
        if verbose:
            p.text(self.domain.begin, 0.0, str(self.domain.begin))
            p.text(self.domain.end, 0.0, str(self.domain.end))
            for i in self.points.iterkeys():
                p.text(i, self.points[i], str(i))

    def level(self, lvl):     # TODO привести к общему формату или удалить
        begin = self.domain.begin
        end = self.domain.end
        for i in self.domain:
            if self.value(i) >= float(lvl):
                begin = i
                break
        for i in self.domain:
            if (self.value(i) <= lvl) and (i > begin):
                end = i
                break
        res = Interval(begin, end)
        return res

    def __getitem__(self, key):
        if not key in self.domain:
            raise KeyError
        return self.value(key)
    def __setitem__(self, key, value):
        if not key in self.domain:
            raise KeyError
        self.values[key] = value

    def centr(self):
        '''
        Вычисляет центроид (центр масс) нечеткого подмножества.
        Зависит от конфигурации ФП. Работает как на непрерывных
        ФП заданного вида, так и на ФП произвольного вида.
        >>> A=Triangle(0.2, 0.3, 0.4)
        >>> print round(A.centr(), 3)
        0.3
        >>> A=Trapezoidal(begin=1.0, begin_tol=2.0, end_tol=5.0, end=6.0)
        >>> print round(A.centr(), 3)
        3.5
        '''
        sum_ = 0.0
        j = 0.0
        for i in self.domain:
            sum_ += self.value(i)*i
            j += self.value(i)
        try:
            return sum_/j
        except ZeroDivisionError:
            return None

    def card(self):
        # TODO отладить инвариантность при разных значениях точности
        '''
        Возвращает мощность нечеткого подмножества
        Синтаксис:
            >>> T=Triangle(-1.4, 0.0, 2.6)
            >>> print round(T.card(), 2) # doctest: +SKIP
            4.0
        '''
        sum_ = 0.0
        for i in self.domain:
            sum_ += self.value(i)
        return sum_*(self.domain.end-self.domain.begin) / self.domain.acc

    def mode(self):
        '''
        Возвращает моду (точку максимума) нечеткого подмножества.
        Синтаксис:
        >>> A=Triangle(10, 20, 40)
        >>> A.mode()
        20.0
        >>> B=Triangle(20, 40, 50)
        >>> B.mode()
        40.0
        >>> C=A+B
        >>> print round(C.mode(), 2)
        20.0
        '''
        res = self.domain.begin
        for i in self.domain():
            if self.value(i) > self.value(res):
                res = i
        return res

    def euclid_distance(self, other): # XXX расстояние Евклида
        begin = min(self.domain.begin, other.begin)
        end = max(self.domain.end, other.end)
        i = begin
        k = 0.0
        delta = (end-begin)/ACCURACY
        summ = 0.0
        while i <= end:
            summ += (self.value(i)-other.value(i))**2
            i += delta
            k += 1.0
        return math.sqrt(summ/k)

    def hamming_distance(self, other): # XXX расстояние Хэмминга
        begin = min(self.domain.begin, other.begin)
        end = max(self.domain.end, other.end)
        i = begin
        k = 0.0
        delta = (end-begin)/ACCURACY
        summ = 0.0
        while i <= end:
            summ += abs(self.value(i)-other.value(i))
            i += delta
            k += 1.0
        return summ/k

##    def con(self):
##        '''
##        Возвращает НПМ, подвергнутое операции концентрации - возведения в
##        квадрат.
##        Синтаксис:
##            >>> T=Triangle(-1.4, 0.0, 2.6)
##            >>> B=T.con()
##            >>> print round(T.value(-1.0), 2)
##            0.29
##            >>> print round(B.value(-1.0), 2)
##            0.08
##            >>> print round(T.centr(), 2)
##            0.4
##            >>> print round(B.centr(), 2)
##            0.42
##
##        '''
##        return self**2
##
##    def dil(self):
##        '''
##        Возвращает НПМ, подвергнутое операции размытия -
##        извлечение квадратного
##        корня (возведение в степень 0,5)
##        Синтаксис:
##            >>> T=Triangle(-1.4, 0.0, 2.6)
##            >>> B=T.dil()
##            >>> print round(T.centr(), 2)
##            0.4
##            >>> print round(B.centr(), 2)
##            0.48
##            >>> print round(T.mode(), 2)
##            0.0
##            >>> print round(B.mode(), 2)
##            0.0
##        '''
##        return self**0.5

    def __add__(self, other):
        if isinstance(self, Point) or isinstance(other, Point):
            raise NotImplementedError
        if isinstance(other, float) or isinstance(other, int):
            raise NotImplementedError
        begin = min(self.domain.begin, other.begin)
        end = max(self.domain.end, other.end)
        res = Subset(begin, end)
        for i in res.domain:
            res[i] = min(self.value(i)+other.value(i), 1)
        return res

    def __sub__(self, other):
        if isinstance(self, Point) or isinstance(other, Point):
            raise NotImplementedError
        if isinstance(other, float) or isinstance(other, int):
            raise NotImplementedError
        begin = min(self.domain.begin, other.begin)
        end = max(self.domain.end, other.end)
        res = Subset(begin, end)
        for i in res.domain:
            res[i] = max(self.value(i)-other.value(i), 0)
        return res

    def __mul__(self, other):
        if isinstance(self, Point) or isinstance(other, Point):
            raise NotImplementedError
        if isinstance(other, float) or isinstance(other, int):
            begin = self.domain.begin
            end = self.domain.end
            res = Subset(begin, end)
            for i in res.domain:
                res[i] = min(self.value(i)*other, 1)
            return res
        begin = min(self.domain.begin, other.begin)
        end = max(self.domain.end, other.end)
        res = Subset(begin, end)
        for i in res.domain:
            res[i] = self.value(i)*other.value(i)
        return res

    def __pow__(self, other):
        if not(isinstance(other, float) or isinstance(other, int)):
            raise NotImplementedError
        begin = self.domain.begin
        end = self.domain.end
        res = Subset(begin, end)
        for i in res.domain:
            res[i] = min(self.value(i)**other, 1)
        return res

    def __invert__(self):
        return self.__neg__()

    def __not__(self):
        return self.__neg__()

    def __neg__(self):
        res = Subset(self.domain.begin, self.domain.end)
        i = res.domain.begin
        while i <= res.domain.end:
            i = i+(res.domain.end-res.domain.begin)/ACCURACY
            res[i] = 1 - self.value(i)

    def __and__(self, other):
        begin = min(self.domain.begin, other.domain.begin)
        end = max(self.domain.end, other.domain.end)
        res = Subset(begin, end)
        i = res.domain.begin
        while i <= res.domain.end:
            i = i+(res.domain.end-res.domain.begin)/ACCURACY
            res[i] = min(self.value(i), other.value(i))
        return res

    def __or__(self, other):
        begin = min(self.domain.begin, other.domain.begin)
        end = max(self.domain.end, other.domain.end)
        res = Subset(begin, end)
        i = res.domain.begin
        while i <= res.domain.end:
            i = i+(res.domain.end-res.domain.begin)/ACCURACY
            res[i] = max(self.value(i), other.value(i))
        return res

    def __abs__(self):
        return self.card()

    def __str__(self):
        return str(self.centr())

    # TODO протестировать следующие три функции
    def __cmp__(self, other):
        '''
        Описание
        Синтаксис:
        Параметры:
            Параметр
                описание
        '''
##        if self == other:
##            return 0.0
        sum_ = 0.0
        sum2 = 0.0
        card = (self.card()*other.card())
        for i in self.domain:
            for j in other.domain:
                chances = self.value(i)*other.value(j)/card
                sum_ += chances
                if i < j:
                    sum2 += chances
        risk = sum2/sum_
        return max(-risk*2+1, 0.0)

    def __eq__(self, other):
        begin = min(self.domain.begin, other.domain.begin)
        end = max(self.domain.end, other.domain.end)
        i = begin
        delta = (end-begin)/ACCURACY
        res = True
        while i <= end:
            if self.value(i) != other.value(i):
                res = False
            i += delta
        return res

    def __ne__(self, other):
        return not self == other


class Trapezoidal(Subset):
    '''
    Нечеткое множество с трапециевидной функцией принадлежности.
    Синтаксис:
        >>> A=Trapezoidal(begin=0.0, begin_tol=1.5,
                            end_tol=2.8, end=6.6,
                            domain=RationalRange(begin=0, end=10))

    Параметры:
        begin
            задает нижнюю границу левого ската трапеции. Значение
            принадлежности в этой точке равно 0.
        begin_tol
            задает нижнюю границу интервала толернтности. Значение
            принадлежности равно 1.
        end_tol
            верхняя граница интервала толерантности. Значение - 1.
        end
            верхняя граница правого ската трапеции. Значение - 0.
        domain
            Этим параметром можно задать границы области определения нечеткого
            множества. Подробнее см. RationalRange и IntegerRange.

        Attributes:
            begin
            begin_tol
            end_tol
            end
    '''

    def __init__(self, begin, begin_tol, end_tol, end, domain=None):
        self.domain.begin = float(begin)
        self.begin_tol = float(begin_tol)
        self.end_tol = float(end_tol)
        self.domain.end = float(end)

        self.points[begin] = 0.0
        self.points[begin_tol] = 1.0
        self.points[end_tol] = 1.0
        self.points[end] = 0.0
        if not domain:
            self.domain = RationalRange(begin, end)
        else:
            self.domain = domain

    def value(self, x):
        if x <= self.domain.begin:
            return 0.0
        elif self.domain.begin < x < self.begin_tol:
            return (x-self.domain.begin)/(self.begin_tol-self.domain.begin)
        elif self.begin_tol <= x <= self.end_tol:
            return 1.0
        elif self.end_tol < x <= self.domain.end:
            return (x-self.domain.end)/(self.end_tol-self.domain.end)
        elif self.domain.end < x:
            return 0.0
        else: return -1

    def card(self):
        return (self.begin_tol-self.domain.begin)/2 + \
                self.end_tol-self.begin_tol + \
                (self.domain.end-self.end_tol)/2

    def mom(self):
        return (self.end_tol+self.begin_tol)/2

    def mode(self):
        return self.begin_tol

    def median(self):
        return (self.domain.begin+self.begin_tol+self.domain.end+self.end_tol)/4

    def __eq__(self, other):
        if isinstance(other, Trapezoidal):
            if self.domain.begin == other.begin and \
                self.begin_tol == other.begin_tol and \
                self.end_tol == other.end_tol and \
                self.domain.end == other.end:
                return True
            else:
                return False
        else:
            return Subset.__eq__(self, other)


class Piecewise(Subset):
    '''
    Класс реализует нечеткое подмножество с функцией принадлежности в виде
    кусочно-линейной функции, задаваемой ассоциативным массивом.

    Синтаксис:
    >>> p={0.2:1.0, 0.5:0.5}
    >>> A=Piecewise(points=p, begin=0.0, end=1.0)
    >>> A.begin
    0.0
    >>> A.end
    1.0
    >>> A.Points[A.begin]
    0.0
    >>> A.value(0.1)
    0.5

    Параметры конструктора (см. Subset):

    points
          Ассоциативный массив, ключами которого являются элементы области
          определения нечеткого множества, а значениями - соответствующие
          значения уровня принадлежности.
          Данная таблица значений задает узловые точки кусочно-линейной
          функции.
          В таблицу автоматически заносятся точки начала и конца
          интервала определения со значениями принадлежности 0.0, так что
          следите за тем, чтобы таблица значений не выходила за пределы
          области определения
    '''
    def __init__(self, points=None, begin=0.0, end=1.0):
        if not points:
            points = {}
        self.points = points
        self.domain.begin = begin
        self.domain.end = end
        self.domain = RationalRange(begin=begin, end=end)
        if not self.domain.begin in self.points:
            self.points[self.domain.begin] = 0.0
        if not self.domain.end in self.points:
            self.points[self.domain.end] = 0.0

    def value(self, x):
        p_ = sorted(self.points.keys())
        p_i = p_[0]
        if x <= self.domain.begin:
            return 0.0
        elif x > self.domain.end:
            return 0.0
        for i in sorted(p_):
            v = self.points[i]
            p_v = self.points[p_i]
            if p_i < x <= i:
                return p_v + (x-p_i)*(v-p_v)/(i-p_i)
            p_i = i

class Triangle(Trapezoidal):
    '''
    Нечеткое множество с функцией принадлежности в виде треугольника.
    Фактически, представляет собой частный случай трапециевидного нечеткого
    множества с вырожденным в точку интервалом толерантности. Этот класс
    создан для быстрого создания нечетких множеств наиболее распространенной
    (треугольной) формы.
    Синтаксис:
        >>> A=Triangle(1.0, 2.3, 5.6)

    Параметры:
        Принимает три параметра, по порядку: нижняя раница ската, точка моды,
        верхняя граница ската. Числа должны быть упорядочены по возрастанию.

    Attributes:
        a
        b
        c

    '''

    def __init__(self, a, b, c, domain=None):
        self.domain.begin = a
        self.domain.end = c
        self.begin_tol = b
        self.end_tol = b
        self.points[self.begin_tol] = 1.0
        if not domain:
            self.domain = RationalRange(begin=a, end=c)
        else:
            self.domain = domain

    def value(self, value):
        if value <= self.domain.begin:
            return 0.0
        elif self.domain.begin < value <= self.begin_tol:
            return (value - self.domain.begin) / \
                    (self.begin_tol - self.domain.begin)
        elif self.begin_tol < value <= self.domain.end:
            return (value - self.domain.end) / \
                    (self.begin_tol - self.domain.end)
        elif self.domain.end < value:
            return 0.0
        else: return -1

    def mode(self):
        return self.begin_tol

    def card(self):
        return (self.domain.end-self.domain.begin)/2

class Interval(Trapezoidal):
    '''
    Определяет четкий интервал как частный вид нечеткого множества. Конструктор
    принимает два параметра - границы интервала.
    Синтаксис:
        >>> A=Interval(0.5, 6.4)

    '''

    def __init__(self, a, b):
        self.domain = RationalRange(begin=a, end=b)
        self.domain.begin = a-2*(b-a)
        self.domain.end = b+2*(b-a)
        self.begin_tol = a
        self.end_tol = b

    def value(self, value):
        if value < self.begin_tol:
            return 0.0
        elif self.begin_tol <= value <= self.end_tol:
            return 1.0
        elif self.end_tol < value:
            return 0.0
        else:
            return -1

    def card(self):
        return self.domain.end-self.begin_tol


class Point(Subset):
    '''
    Реализует нечеткое множество состоящее из одной точки.
    Синтаксис:
        >>> A=Point(2.0)

    '''

    def __init__(self, a):
        self.domain.begin = a
        self.domain.end = a

    def value(self, x):
        if x != self.domain.begin:
            return 0.0
        elif self.domain.begin == x:
            return 1.0
        else:
            return -1

    def traversal(self):
        i = 1
        while i <= ACCURACY:
            yield self.domain.begin
            i = i+1

    def plot(self):
        p.scatter([self.domain.begin], [1.0], 20)
        p.plot(self.domain.begin, 1.0)

    def card(self):
        return 0.0


class Gaussian(Subset):
    '''
    Определяет нечеткое множество с функцией принадлежности в виде гауссианы.
    Синтаксис:
        >>> A=Gaussian(0.0, 1.0)    # Стандартное распределение

    Первый параметр - мода гауссианы, второй - стандартное отклонение (омега)
    Attributes:
        mu
        omega
    '''

    def __init__(self, mu, omega):
        self.mu = float(mu)
        self.omega = float(omega)

        self.domain.begin = mu-5*omega
        self.domain.end = mu+5*omega

    def value(self, x):
        return round(math.exp(-((x-self.mu)**2)/(2*self.omega**2)), 5)

    def plot(self):
        x = []
        y = []
        for i in self.domain:
            x.append(i)
            y.append(self.value(i))
        p.plot(x, y)
        p.plot(self.domain.end+(self.domain.end-self.domain.begin)/3, -0.1)
        p.text(self.mu, 1.00, str(self.mu))

    def centr(self):
        return self.mu

    def mode(self):
        return self.mu

    def card(self):
        return round(math.sqrt(2*math.pi)*self.omega, 5)

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    #~ doctest.testmod(verbose=True)
