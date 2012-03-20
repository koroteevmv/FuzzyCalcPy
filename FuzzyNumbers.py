''' Модуль для работы с нечеткими числами

Модуль реализует функциональность аппарата нечеткой логики в части работы с
нечеткими числами. Он включает:
    - описание
'''

# -*- coding: UTF-8 -*-

from FuzzyCalc_Common import *
from FuzzySubset import *
from math import *

line=lambda c: lambda a, b: lambda x: abs((x-b)/(a-b))**c
lines=lambda c: lambda a, b: lambda x: abs((x-b)/(a-b))**log(0.5, ((c-b)/(a-b)))
quad=lambda c: lambda a, b: lambda x: abs(1-((x-a)/abs(b-a))**2)**c
quads=lambda c: lambda a, b: lambda x: abs(1-((x-a)/abs(b-a))**2)**log(0.5, (1-((c-a)/abs(b-a))**2))
lapl=lambda c: lambda a, b: lambda x: exp(-abs(x-a)*c/abs(b-a))
lapls=lambda c: lambda a, b: lambda x: exp(abs(x-a)*log(0.5)/abs(c-a))
tang=lambda c: lambda a, b: lambda x: (1+tanh(-((x-a)/(abs(b-a)/c))**2))
gaus=lambda c: lambda a, b: lambda x: (exp(-((x-a)**2)/c**2))
cauc=lambda c: lambda a, b: lambda x: (1/(1+((x-a)*c/abs(b-a))**2))
logi=lambda c: lambda a, b: lambda x: (2/(1+exp(((x-a)*c/abs(b-a))**2)))
secg=lambda c: lambda a, b: lambda x: (1/cosh((x-a)/(b-a)))
tangs=lambda c: lambda a, b: lambda x: (1+tanh(-((x-a)/abs(b-a))**2))**log(0.5, (1+tanh(-((c-a)/abs(b-a))**2)))
gauss=lambda c: lambda a, b: lambda x: exp( ((x-a)**2)*log(0.5) / ((c-a)**2) )
caucs=lambda c: lambda a, b: lambda x: (1/ (1+ ((x-a) / (c-a))**2))
logis=lambda c: lambda a, b: lambda x: (2/(1+exp(((x-a)/abs(b-a))**2)))**log(0.5, ((2/(1+exp(((c-a)/abs(b-a))**2)))))
secgs=lambda c: lambda a, b: lambda x: (1/cosh((x-a)/abs(b-a)))**log(0.5, (1/cosh((c-a)/abs(b-a))))
coss=lambda c: lambda a, b: lambda x: ((1+cos(pi*(x-a)/abs(b-a)))/2)**log(0.5, ((1+cos(pi*(c-a)/abs(b-a)))/2))
point=lambda a, b: lambda x: 1

class Trap_ext(Subset):
    '''
    Нечеткие числа в обобщенно-трапециевидной форме.
    Синтаксис:
        >>> A=Trap_ext(begin=1.0, end=4.0, begin_tol=2.0, end_tol=3.0, left=line(3.0), right=line(1.0))
    Первые 4 параметра аналогичны параметрам конструктора трапециевидных
    нечетких чисел (см. Trapezoidal). Два последних определяют форму функций
    скатов - левого и правого. Для этого используется ряд лямбда-выражений,
    включенных в настоящую библиотеку. При их использовании следует
    указать параметр функции - число, характеризующее степень плавности ската.
    Функцию каждого ската выбирает пользователь из следующих альтернатив:
        line
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
    begin=0.0
    begin_tol=0.0
    end_tol=0.0
    end=0.0
    l_skat=line(1.0)
    r_skat=line(1.0)
    left=None
    right=None
    def __init__(self, begin=0.0, begin_tol=0.0, end_tol=0.0, end=0.0, domain=None, left=line(1), right=line(1)):
        self.begin=float(begin)
        self.begin_tol=float(begin_tol)
        self.end_tol=float(end_tol)
        self.end=float(end)
        self.Points[begin]=0.0
        self.Points[begin_tol]=1.0
        self.Points[end_tol]=1.0
        self.Points[end]=0.0
        self.left=left
        self.right=right
        self.l_skat=left(self.begin_tol, self.begin)
        self.r_skat=right(self.end_tol, self.end)
        if begin==begin_tol:
            self.left=point
            self.l_skat=point(self.begin_tol, self.begin)
        if end==end_tol:
            self.right=point
            self.r_skat=point(self.end_tol, self.end)
        if not domain:
            self.Domain=RationalRange(begin, end)
        else:
            self.Domain=domain
    def value(self, x):
        if x<=self.begin: return 0.0
        elif self.begin<x<self.begin_tol: return self.l_skat(x)
        elif self.begin_tol<=x<=self.end_tol: return 1.0
        elif self.end_tol<x<=self.end: return self.r_skat(x)
        elif self.end<x: return 0.0
        else: return -1
    def disp(self):
        for i in self.Domain:
            pass
    def fuzziness(self):
        t=self.end_tol - self.begin_tol
        o=self.end - self.begin
        l=self.level(0.5)
        u=l.b - l.a
        return t*( 1-abs( 2.0*u-o-t )/(0-t) )
        pass

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other  , int):
            other=Trap_ext(begin=other, end=other, begin_tol=other, end_tol=other)
        x1=self.begin
        x2=self.begin_tol
        x3=self.end_tol
        x4=self.end
        xl=self.left
        xr=self.right
        y1=other.begin
        y2=other.begin_tol
        y3=other.end_tol
        y4=other.end
        yl=other.left
        yr=other.right
        z1=min(x1+y1, x1+y4, x4+y1, x4+y4)
        z2=min(x2+y2, x2+y3, x3+y2, x3+y3)
        z3=max(x2+y2, x2+y3, x3+y2, x3+y3)
        z4=max(x1+y1, x1+y4, x4+y1, x4+y4)

        zl=lambda x, y: lambda z: xl(x2, x1)(x1+(x2-x1)*(z-z1)/(z2-z1))*yl(y2, y1)(y1+(y2-y1)*(z-z1)/(z2-z1))
        zr=lambda x, y: lambda z: xr(x3, x4)(x3+(x4-x3)*(z-z3)/(z4-z3))*yr(y3, y4)(y3+(y4-y3)*(z-z3)/(z4-z3))

        res=Trap_ext(begin=z1, begin_tol=z2, end_tol=z3, end=z4, left=zl, right=zr)
        return res

    def __sub__(self, other):
        if isinstance(other, float) or isinstance(other  , int):
            other=Trap_ext(begin=other, end=other, begin_tol=other, end_tol=other)
        x1=self.begin
        x2=self.begin_tol
        x3=self.end_tol
        x4=self.end
        xl=self.left
        xr=self.right

        y1=other.begin
        y2=other.begin_tol
        y3=other.end_tol
        y4=other.end
        yl=other.left
        yr=other.right

        z1=min(x1-y1, x1-y4, x4-y1, x4-y4)
        z2=min(x2-y2, x2-y3, x3-y2, x3-y3)
        z3=max(x2-y2, x2-y3, x3-y2, x3-y3)
        z4=max(x1-y1, x1-y4, x4-y1, x4-y4)

        zl=lambda x, y: lambda z: xl(x2, x1)(x1+(x2-x1)*(z-z1)/(z2-z1))*yl(y2, y1)(y1+(y2-y1)*(z-z1)/(z2-z1))
        zr=lambda x, y: lambda z: xr(x3, x4)(x3+(x4-x3)*(z-z3)/(z4-z3))*yr(y3, y4)(y3+(y4-y3)*(z-z3)/(z4-z3))

        res=Trap_ext(begin=z1, begin_tol=z2, end_tol=z3, end=z4, left=zl, right=zr)
        return res

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other  , int):
            other=Trap_ext(begin=other, end=other, begin_tol=other, end_tol=other)
        x1=self.begin
        x2=self.begin_tol
        x3=self.end_tol
        x4=self.end
        xl=self.left
        xr=self.right
        y1=other.begin
        y2=other.begin_tol
        y3=other.end_tol
        y4=other.end
        yl=other.left
        yr=other.right

        z1=min(x1*y1, x1*y4, x4*y1, x4*y4)
        z2=min(x2*y2, x2*y3, x3*y2, x3*y3)
        z3=max(x2*y2, x2*y3, x3*y2, x3*y3)
        z4=max(x1*y1, x1*y4, x4*y1, x4*y4)

        zl=lambda x, y: lambda z: xl(x, y)(z)*yl(x, y)(z)
        zr=lambda x, y: lambda z: xr(x, y)(z)*yr(x, y)(z)

        res=Trap_ext(begin=z1, begin_tol=z2, end_tol=z3, end=z4, left=zl, right=zr)
        return res

    def __div__(self, other):
        if isinstance(other, float) or isinstance(other  , int):
            other=Trap_ext(begin=other, end=other, begin_tol=other, end_tol=other)
        x1=self.begin
        x2=self.begin_tol
        x3=self.end_tol
        x4=self.end
        xl=self.left
        xr=self.right
        y1=other.begin
        y2=other.begin_tol
        y3=other.end_tol
        y4=other.end
        yl=other.left
        yr=other.right

        z1=min(x1/y1, x1/y4, x4/y1, x4/y4)
        z2=min(x2/y2, x2/y3, x3/y2, x3/y3)
        z3=max(x2/y2, x2/y3, x3/y2, x3/y3)
        z4=max(x1/y1, x1/y4, x4/y1, x4/y4)

        zl=lambda x, y: lambda z: xl(x, y)(z)*yl(x, y)(z)
        zr=lambda x, y: lambda z: xr(x, y)(z)*yr(x, y)(z)

        res=Trap_ext(begin=z1, begin_tol=z2, end_tol=z3, end=z4, left=zl, right=zr)
        return res

    def __radd__(self, other):
        if isinstance(other, float) or isinstance(other  , int):
            other=Trap_ext(begin=other, end=other, begin_tol=other, end_tol=other)
        x1=self.begin
        x2=self.begin_tol
        x3=self.end_tol
        x4=self.end
        xl=self.left
        xr=self.right
        y1=other.begin
        y2=other.begin_tol
        y3=other.end_tol
        y4=other.end
        yl=other.left
        yr=other.right
        z1=min(x1+y1, x1+y4, x4+y1, x4+y4)
        z2=min(x2+y2, x2+y3, x3+y2, x3+y3)
        z3=max(x2+y2, x2+y3, x3+y2, x3+y3)
        z4=max(x1+y1, x1+y4, x4+y1, x4+y4)

##        print z1, z2, z3, z4

        zl=lambda x, y: lambda z: xl(x2, x1)(x1+(x2-x1)*(z-z1)/(z2-z1))*yl(y2, y1)(y1+(y2-y1)*(z-z1)/(z2-z1))
        zr=lambda x, y: lambda z: xr(x3, x4)(x3+(x4-x3)*(z-z3)/(z4-z3))*yr(y3, y4)(y3+(y4-y3)*(z-z3)/(z4-z3))

        res=Trap_ext(begin=z1, begin_tol=z2, end_tol=z3, end=z4, left=zl, right=zr)
        return res

    def __rsub__(self, other):
        if isinstance(other, float) or isinstance(other  , int):
            other=Trap_ext(begin=other, end=other, begin_tol=other, end_tol=other)
        x1=self.begin
        x2=self.begin_tol
        x3=self.end_tol
        x4=self.end
        xl=self.left
        xr=self.right

        y1=other.begin
        y2=other.begin_tol
        y3=other.end_tol
        y4=other.end
        yl=other.left
        yr=other.right

        z1=min(x1-y1, x1-y4, x4-y1, x4-y4)
        z2=min(x2-y2, x2-y3, x3-y2, x3-y3)
        z3=max(x2-y2, x2-y3, x3-y2, x3-y3)
        z4=max(x1-y1, x1-y4, x4-y1, x4-y4)

        zl=lambda x, y: lambda z: xl(x2, x1)(x1+(x2-x1)*(z-z1)/(z2-z1))*yl(y2, y1)(y1+(y2-y1)*(z-z1)/(z2-z1))
        zr=lambda x, y: lambda z: xr(x3, x4)(x3+(x4-x3)*(z-z3)/(z4-z3))*yr(y3, y4)(y3+(y4-y3)*(z-z3)/(z4-z3))

        res=Trap_ext(begin=z1, begin_tol=z2, end_tol=z3, end=z4, left=zl, right=zr)
        return res

    def __rmul__(self, other):
        if isinstance(other, float) or isinstance(other  , int):
            other=Trap_ext(begin=other, end=other, begin_tol=other, end_tol=other)
        x1=self.begin
        x2=self.begin_tol
        x3=self.end_tol
        x4=self.end
        xl=self.left
        xr=self.right
        y1=other.begin
        y2=other.begin_tol
        y3=other.end_tol
        y4=other.end
        yl=other.left
        yr=other.right

        z1=min(x1*y1, x1*y4, x4*y1, x4*y4)
        z2=min(x2*y2, x2*y3, x3*y2, x3*y3)
        z3=max(x2*y2, x2*y3, x3*y2, x3*y3)
        z4=max(x1*y1, x1*y4, x4*y1, x4*y4)

        zl=lambda x, y: lambda z: xl(x, y)(z)*yl(x, y)(z)
        zr=lambda x, y: lambda z: xr(x, y)(z)*yr(x, y)(z)

        res=Trap_ext(begin=z1, begin_tol=z2, end_tol=z3, end=z4, left=zl, right=zr)
        return res

    def __rdiv__(self, other):
        if isinstance(other, float) or isinstance(other  , int):
            other=Trap_ext(begin=other, end=other, begin_tol=other, end_tol=other)
        x1=self.begin
        x2=self.begin_tol
        x3=self.end_tol
        x4=self.end
        xl=self.left
        xr=self.right
        y1=other.begin
        y2=other.begin_tol
        y3=other.end_tol
        y4=other.end
        yl=other.left
        yr=other.right

        z1=min(x1/y1, x1/y4, x4/y1, x4/y4)
        z2=min(x2/y2, x2/y3, x3/y2, x3/y3)
        z3=max(x2/y2, x2/y3, x3/y2, x3/y3)
        z4=max(x1/y1, x1/y4, x4/y1, x4/y4)

        zl=lambda x, y: lambda z: xl(x, y)(z)*yl(x, y)(z)
        zr=lambda x, y: lambda z: xr(x, y)(z)*yr(x, y)(z)

        res=Trap_ext(begin=z1, begin_tol=z2, end_tol=z3, end=z4, left=zl, right=zr)
        return res


def g(k, f, s):
    skat_=f(k)
    skat=skat_(mode, edge)
    x=[i+edge for i in range(int(1.5*abs(mode-edge)))]
    y=[skat(i) for i in x]
    for i in range(len(y)):
        if y[i]>1: y[i]=1.0
        elif y[i]<0: y[i]=0.0
    p.plot(x, y)
    legend.append(' '+s)

class TrFN(Trap_ext):
    def __init__(self, a, b, c, d):
        self.begin=float(a)
        self.begin_tol=float(b)
        self.end_tol=float(c)
        self.end=float(d)
        self.Points[a]=0.0
        self.Points[b]=1.0
        self.Points[c]=1.0
        self.Points[d]=0.0
        self.left=line(1.0)
        self.right=line(1.0)
        self.l_skat=line(1.0)(self.begin_tol, self.begin)
        self.r_skat=line(1.0)(self.end_tol, self.end)
        if a==b:
            self.left=point
            self.l_skat=point(self.begin_tol, self.begin)
        if c==d:
            self.right=point
            self.r_skat=point(self.end_tol, self.end)
        self.Domain=RationalRange(a, d)