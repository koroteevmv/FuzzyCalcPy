from FuzzyCalc_Common import *
from FuzzyDomain import *
from math import *

class Subset:
    '''
    Реализует функциональность нечеткого подмножества общего вида.
    Имеет атрибуты, указывающие начало и конец интервала
    определения подмножества (для подмножеств, определенных на R).

    >>> A=Subset(0.0, 1.0)
    >>> A.begin
    0.0
    >>> A.end
    1.0
    '''

    begin=0.0
    end=1.0
    Values={}
    Points={}
    Domain=RationalRange()
    tnorm=min_max()
    def __init__(self, begin=0.0, end=1.0, domain=RationalRange(), tnorm=min_max):
        self.begin=begin
        self.end=end
        self.Domain=domain
        self.Values={}
        self.Values[self.begin]=0.0
        self.Values[self.end]=0.0
        self.Points[self.begin]=0.0
        self.Points[self.end]=0.0
        self.tnorm=tnorm()
        pass
    def value(self, x):
        '''
        Возвращает уровень принадлежности точки нечеткому подмножеству.
        Данный метод непосредственно и является программной имплементацией функции принадлежности.
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
            return self.Values[x]
        except KeyError:
            sort=sorted(self.Values.keys())
            sort1=sorted(self.Values.keys())
            sort1.pop(0)
            for i, j in zip(sort, sort1):
                if i<x<j:
                    x1=i
                    x2=j
                    y1=self.value(i)
                    y2=self.value(j)
                    y=(x-x1)*(y2-y1)/(x2-x1)+y1
                    #~ return y
                    return round((y1+y2)/2, 4)
            else:
                return 0.0
    def cut(self):
        delta=(self.end-self.begin)/ACCURACY
        for i in self.Domain:
            if self.value(i)<PRECISION:
                self.begin+=delta
            else:
                break
            i=i+delta
        i=self.end
        while i>=self.begin:
            if self.value(i)<PRECISION:
                self.end-=delta
            else:
                break
            i=i-delta
        self.begin-=2*delta
        self.end+=2*delta
        self.Values[self.begin]=0.0
        self.Values[self.begin+delta]=0.0
        self.Values[self.end]=0.0
        self.Values[self.end-delta]=0.0
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
        for x in self.Domain:
            print x, self.value(x)
    def _char(self):    # TODO привести к общему формату или удалить
        print
        for i in sorted(self.Values.keys()):
            print i, self.Values[i]
        print
        
        for x in self.Domain:
            print x, ":"
            try:
                print self.Values[x]
            except KeyError:
                sort=sorted(self.Values.keys())
                sort1=sorted(self.Values.keys())
                sort1.pop(0)
                for i, j in zip(sort, sort1):
                    if i<x<j:
                        x1=i
                        x2=j
                        y1=self.value(i)
                        y2=self.value(j)
                        y=((x1-x2)/(y1-x2))*(x-x1)+y1
                        print x1, x2
                        print y1, y, y2
                        print (y1+y2)/2
            print

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
        sup=self.sup()
        if sup==0.0: return self
        res=Subset(self.begin, self.end)
        for i in self.Domain:
            res.set(i, self.value(i)/sup)
        return res
    def sup(self):
        sup=0.0
        for i in self.Domain:
            v=self.value(i)
            if v>sup:
                sup=v
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
        x=[]
        y=[]
        for i in self.Domain:
            v=self.value(i)
            x.append(i)
            y.append(v)
        p.plot(x, y)
        if isinstance(self.Domain, IntegerRange):
        # TODO построение графиков НПМ на целочисленных интервалах.
            pass
        ##p.plot(self.begin, 1.2)
        ##p.plot(self.end+(self.end-self.begin)/3, -0.1)
        if verbose:
           ##p.text(self.begin, 0.0, str(self.begin))
           ##p.text(self.end, 0.0, str(self.end))
##           p.text(self.mode(), 1.0, str(self.mode()))
##           p.text(self.centr(), 0.5, str(self.centr()))
           for i in self.Points.iterkeys():
               p.text(i, self.Points[i], str(i))
    def level(self, a):     # TODO привести к общему формату или удалить
        x1=self.begin
        x2=self.end
        for i in self.Domain:
            if (self.value(i)>=float(a)):
                x1=i
                break
        for i in self.Domain:
            if (self.value(i)<=a) and (i>x1):
                x2=i
                break
        res=Interval(x1, x2)
        return res
    def set(self, a, mu):
        self.Values[a]=mu
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
        summ=0.0
        j=0.0
        for i in self.Domain:
            summ+= self.value(i)*i
            j+=self.value(i)
        try:
            return summ/j
        except ZeroDivisionError:
            return None
    def card(self):
        # FIXME bиспрвить и отладить инвариантность при разных значениях точности
        '''
        Возвращает мощность нечеткого подмножества
        Синтаксис:
            >>> T=Triangle(-1.4, 0.0, 2.6)
            >>> print round(T.card(), 2) # doctest: +SKIP
            4.0
        '''
        summ=0.0
        j=0
        for i in self.Domain:
            summ+=self.value(i)
            j+=1
        return summ*(self.end-self.begin) / self.Domain.acc
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
        res=self.begin
        for i in self.Domain:
            if self.value(i)>self.value(res): res=i
        return res
    def Euclid_distance(self, other): # XXX расстояние Евклида
        begin=min(self.begin, other.begin)
        end=max(self.end, other.end)
        i=begin
        k=0.0
        delta=(end-begin)/ACCURACY
        summ=0.0
        while i<=end:
            summ+=(self.value(i)-other.value(i))**2
            i+=delta
            k+=1.0
            pass
        return math.sqrt(summ/k)
        pass
    def Hamming_distance(self, other): # XXX расстояние Хэмминга
        begin=min(self.begin, other.begin)
        end=max(self.end, other.end)
        i=begin
        k=0.0
        delta=(end-begin)/ACCURACY
        summ=0.0
        while i<=end:
            summ+=abs(self.value(i)-other.value(i))
            i+=delta
            k+=1.0
            pass
        return summ/k
        pass
    def con(self):
        '''
        Возвращает НПМ, подвергнутое операции концентрации - возведения в
        квадрат.
        Синтаксис:
            >>> T=Triangle(-1.4, 0.0, 2.6)
            >>> B=T.con()
            >>> print round(T.value(-1.0), 2)
            0.29
            >>> print round(B.value(-1.0), 2)
            0.08
            >>> print round(T.centr(), 2)
            0.4
            >>> print round(B.centr(), 2)
            0.42

        '''
        return self**2
    def dil(self):
        '''
        Возвращает НПМ, подвергнутое операции размытия - извлечение квадратного
        корня (возведение в степень 0,5)
        Синтаксис:
            >>> T=Triangle(-1.4, 0.0, 2.6)
            >>> B=T.dil()
            >>> print round(T.centr(), 2)
            0.4
            >>> print round(B.centr(), 2)
            0.48
            >>> print round(T.mode(), 2)
            0.0
            >>> print round(B.mode(), 2)
            0.0
        '''
        return self**0.5
    def __add__(self, other):
        if isinstance(self, Point) or isinstance(other, Point):
            raise NotImplemented
        if isinstance(other, float) or isinstance(other  , int):
            raise NotImplemented
        begin=min(self.begin, other.begin)
        end=max(self.end, other.end)
        res=Subset(domain=RationalRange(begin, end))
        for i in res.Domain:
            ii=self.value(i)
            jj=other.value(i)
            res.set(i, min(ii+jj, 1))       # TODO: вставить t-нормы
        return res
    def __sub__(self, other):
        if isinstance(self, Point) or isinstance(other, Point):
            raise NotImplemented
        if isinstance(other, float) or isinstance(other  , int):
            raise NotImplemented
        begin=min(self.begin, other.begin)
        end=max(self.end, other.end)
        res=Subset(domain=RationalRange(begin, end))
        for i in res.Domain:
            ii=self.value(i)
            jj=other.value(i)
            res.set(i, max(ii-jj, 0))
        return res
    def __mul__(self, other):
        if isinstance(self, Point) or isinstance(other, Point):
            raise NotImplemented
        if isinstance(other, float) or isinstance(other, int):
            begin=self.begin
            end=self.end
            res=Subset(domain=RationalRange(begin, end))
            for i in res.Domain:
                ii=self.value(i)
                res.set(i, min(ii*other, 1))
            return res
        begin=min(self.begin, other.begin)
        end=max(self.end, other.end)
        res=Subset(domain=RationalRange(begin, end))
        for i in res.Domain:
            ii=self.value(i)
            jj=other.value(i)
            res.set(i, ii*jj)
        return res
    def __pow__(self, other):
        if not(isinstance(other, float) or isinstance(other, int)):
            raise NotImplemented
        begin=self.begin
        end=self.end
        res=Subset(domain=RationalRange(begin, end))
        for i in res.Domain:
            ii=self.value(i)
            res.set(i, min(ii**other, 1))
        return res
    def __invert__():
        return self.__neg__()
    def __not__():
        return self.__neg__()
    def __neg__(self):
        res=Subset(self.begin, self.end)
        i=res.begin
        while i<=res.end:
            i=i+(res.end-res.begin)/ACCURACY
            res.set(i, 1 - self.value(i))
    def __and__(a, b):
        begin=min(a.begin, b.begin)
        end=max(a.end, b.end)
        res=Subset(begin, end)
        i=res.begin
        while i<=res.end:
            i=i+(res.end-res.begin)/ACCURACY
            res.set(i, min(a.value(i), b.value(i)))
        return res
    def __or__(a, b):
        begin=min(a.begin, b.begin)
        end=max(a.end, b.end)
        res=Subset(begin, end)
        i=res.begin
        while i<=res.end:
            i=i+(res.end-res.begin)/ACCURACY
            res.set(i, max(a.value(i), b.value(i)))
        return res
    def __abs__(self):
        return self.card()
    def __str__(self):
##        self.plot()
        return str(self.centr())
    def t_norm(a, b):
        '''
        Описание
        Синтаксис:
        Параметры:
            Параметр
                описание
        '''
        # TODO задокументировать эти две функции. Отметить возможность изменения t-норм на лету
        begin=min(a.begin, b.begin)
        end=max(a.end, b.end)
        res=Subset(begin, end)
        i=res.begin
        while i<=res.end:
            i=i+(res.end-res.begin)/ACCURACY
            res.set(i, a.tnorm.t_norm(a.value(i), b.value(i)))
        return res
    def t_conorm(a, b):
        begin=min(a.begin, b.begin)
        end=max(a.end, b.end)
        res=Subset(begin, end)
        i=res.begin
        while i<=res.end:
            i=i+(res.end-res.begin)/ACCURACY
            res.set(i, a.tnorm.t_conorm(a.value(i), b.value(i)))
        return res
    def __cmp__(self, other):
        '''
        Описание
        Синтаксис:
        Параметры:
            Параметр
                описание
        '''
        return self>other
    def __gt__(self, other):
        '''
        Описание
        Синтаксис:
        Параметры:
            Параметр
                описание
        '''
        if self==other: return 0.0
        summ=0.0
        sum1=0.0
        sum2=0.0
        card=(self.card()*other.card())
        for npv in self.Domain:
            for g in other.Domain:
                chances=self.value(npv)*other.value(g)/card
                summ+=chances
                if npv>=g:
                    sum1+=chances
                else:
                    sum2+=chances
        ch=sum1/summ
        risk=sum2/summ
        return max(-risk*2+1, 0.0)
    def __eq__(self, other):
        begin=min(self.begin, other.begin)
        end=max(self.end, other.end)
        i=begin
        delta=(end-begin)/ACCURACY
        flag=True
        while i<=end:
            if self.value(i)!=other.value(i):
                flag=False
            i+=delta
        return float(flag)
    def __ne__(self, other):
        return not self==other
    def ___le__(self, other):
        if self==other:
            return 0.0
        else:
            return (self<other)
        pass
    def ___ge__(self, other):
        if self==other:
            return 0.0
        else:
            return (self>other)
    def ___lt__(other, self):
        '''
        Описание
        Синтаксис:
        Параметры:
            Параметр
                описание
        '''
        if self==other: return 0.0
        summ=0.0
        sum1=0.0
        sum2=0.0
        card=(self.card()*other.card())
        for npv in self.Domain:
            for g in other.Domain:
                chances=self.value(npv)*other.value(g)/card
                summ+=chances
                if npv>=g:
                    sum1+=chances
                else:
                    sum2+=chances
        ch=sum1/summ
        risk=sum2/summ
        return max(-risk*2+1, 0.0)


class Trapezoidal (Subset):
    '''
    Нечеткое множество с трапециевидной функцией принадлежности.
    Синтаксис:
        >>> A=Trapezoidal(begin=0.0, begin_tol=1.5, end_tol=2.8, end=6.6, domain=RationalRange(begin=0, end=10))

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
    '''
    begin=0.0
    begin_tol=0.0
    end_tol=0.0
    end=0.0
    def __init__(self, begin, begin_tol, end_tol, end, domain=None):
        self.begin=float(begin)
        self.begin_tol=float(begin_tol)
        self.end_tol=float(end_tol)
        self.end=float(end)
        self.Points[begin]=0.0
        self.Points[begin_tol]=1.0
        self.Points[end_tol]=1.0
        self.Points[end]=0.0
        if not domain:
            self.Domain=RationalRange(begin, end)
        else:
            self.Domain=domain
    def value(self, x):
        if x<=self.begin: return 0.0
        elif self.begin<x<self.begin_tol: return (x-self.begin)/(self.begin_tol-self.begin)
        elif self.begin_tol<=x<=self.end_tol: return 1.0
        elif self.end_tol<x<=self.end: return (x-self.end)/(self.end_tol-self.end)
        elif self.end<x: return 0.0
        else: return -1
    def card(self):
        a=(self.begin_tol-self.begin)/2
        b=self.end_tol-self.begin_tol
        c=(self.end-self.end_tol)/2
        return a+b+c
    def mom(self):
        return (self.end_tol+self.begin_tol)/2
    def mode(self):
        return self.begin_tol
##    def centr(self):
##        return
    def median(self):
        return (self.begin+self.begin_tol+self.end+self.end_tol)/4
    def __eq__(self, other):
        if isinstance(other, Trapezoidal):
            if self.begin==other.begin and self.begin_tol==other.begin_tol and self.end_tol==other.end_tol and self.end==other.end:
                return True
            else: return False
        else:
            return Subset.__eq__(self, other)



class Piecewise (Subset):
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
    def __init__(self, points={}, begin=0.0, end=1.0):
        self.Points=points
        self.begin=begin
        self.end=end
        self.Domain=RationalRange(begin=begin, end=end)
        if not self.begin in self.Points:
            self.Points[self.begin]=0.0
        if not self.end in self.Points:
            self.Points[self.end]=0.0
    def value(self, x):
        p_=sorted(self.Points.keys())
        p_i=p_[0]
        if x<=self.begin: return 0.0
        elif x>self.end: return 0.0
        for i in sorted(p_):
            v=self.Points[i]
            p_v=self.Points[p_i]
            if p_i<x<=i:
                return p_v + (x-p_i)*(v-p_v)/(i-p_i)
            p_i=i

class Triangle (Trapezoidal):
    '''
    Нечеткое множество с функцией принадлежности в виде треугольника. Фактически,
    представляет собой частный случай трапециевидного нечеткого множества
    с вырожденным в точку интервалом толерантности. Этот класс создан для
    быстрого создания нечетких множеств наиболее распространенной (треугольной)
    формы.
    Синтаксис:
        >>> A=Triangle(1.0, 2.3, 5.6)

    Параметры:
        Принимает три параметра, по порядку: нижняя раница ската, точка моды,
        верхняя граница ската. Числа должны быть упорядочены по возрастанию.
    '''
    a=0.0
    b=0.0
    c=0.0
    def __init__(self, a, b, c, domain=None):
        self.a=float(a)
        self.b=float(b)
        self.c=float(c)
        self.begin=self.a
        self.end=self.c
        self.begin_tol=self.b
        self.end_tol=self.b
        self.Points[self.begin_tol]=1.0
        if not domain:
            self.Domain=RationalRange(begin=a, end=c)
        else:
            self.Domain=domain
    def value(self, x):
        if x<=self.a: return 0.0
        elif self.a<x<=self.b: return (x - self.a) / (self.b - self.a)
        elif self.b<x<=self.c: return (x - self.c) / (self.b - self.c)
        elif self.c<x: return 0.0
        else: return -1
    def mode(self):
        return self.b
    def card(self):
        return (self.end-self.begin)/2

class Interval (Subset):
    '''
    Определяет четкий интервал как частный вид нечеткого множества. Конструктор
    принимает два параметра - границы интервала.
    Синтаксис:
        >>> A=Interval(0.5, 6.4)

    '''
    a=0.0
    b=0.0
    tnorm=min_max()
    def __init__(self, a, b, tnorm=min_max):
        self.a=float(a)
        self.b=float(b)
        self.Domain=RationalRange(begin=a, end=b)
        self.begin=a-2*(b-a)
        self.end=b+2*(b-a)
        self.tnorm=tnorm
    def value(self, x):
        if x<self.a: return 0.0
        elif self.a<=x<=self.b: return 1.0
        elif self.b<x: return 0.0
        else: return -1
    def card(self):
        return self.end-self.begin


class Point (Subset):
    '''
    Реализует нечеткое множество состоящее из одной точки.
    Синтаксис:
        >>> A=Point(2.0)

    '''
    a=0.0
    def __init__(self, a):
        self.a=float(a)
        self.begin=a
        self.end=a
    def value(self, x):
        if x<>self.a: return 0.0
        elif self.a==x: return 1.0
        else: return -1
    def traversal(self):
        i=1
        while i<=ACCURACY:
            yield self.a
            i=i+1
    def plot(self):
        p.scatter([self.a], [1.0], 20)
        p.plot(self.a, 1.0)
    def card(self):
        return 0.0


class Gaussian (Subset):
    '''
    Определяет нечеткое множество с функцией принадлежности в виде гауссианы.
    Синтаксис:
        >>> A=Gaussian(0.0, 1.0)    # Стандартное распределение

    Первый параметр - мода гауссианы, второй - стандартное отклонение (омега)
    '''
    mu=0.0
    omega=0.0
    def __init__(self, mu, omega):
        self.mu=float(mu)
        self.omega=float(omega)
        self.begin=mu-5*omega
        self.end=mu+5*omega
        self.Domain=RationalRange(self.begin, self.end)
    def value(self, x):
        return round(math.exp(-((x-self.mu)**2)/(2*self.omega**2)), 5)
    ##def plot(self):
        ##x=[]
        ##y=[]
        ##for i in self.traversal():
            ##v=self.value(i)
            ##x.append(i)
            ##y.append(v)
        ##p.plot(x, y)
        ##p.plot(self.end+(self.end-self.begin)/3, -0.1)
        ##p.text(self.mu, 1.00, str(self.mu))
    def centr(self):
        return self.mu
    def mode(self):
        return self.mu
    def card(self):
        return round(math.sqrt(2*math.pi)*self.omega, 5)

if __name__ == "__main__":
    import doctest
    #~ doctest.testmod(verbose=False)
    doctest.testmod(verbose=True)
