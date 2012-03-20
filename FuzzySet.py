''' Модуль для работы с нечеткими множествами

Модуль реализует функциональность аппарата нечеткой логики в части работы с
нечеткими множествами. Он включает:
    - абстрактный класс нечеткого множества,
    - шаблоны для создания классификаторов различных видов.

В основном, модуль предназначен длясоздания и спользования нечетких
классификаторов. С помощью него можно создать классификатор как в ручном режиме
и заполнить его термами самостоятельно, так и воспользоваться одним из
конструкторов, описанных ниже.

Нечеткий классификатор - это одно из применений нечеткого множества. Он состоит
из нескольких нечетких подмножеств (см. FuzzySubset), определенных на одном
носителе (интервале определения). Термы множества имеют метки,которые
используются в качестве значений лингвистических переменных вместо обычных
чисел.
'''

# -*- coding: UTF-8 -*-

from FuzzyCalc_Common import *
from FuzzySubset import *
from FuzzyNumbers import *

class FuzzySet:
    '''
    Нечеткое множество, или классификатор, состоящее из набора нечетких
    подмножеств, определенных на одном и том же носителе.
    Синтаксис:
    >>> A=FuzzySet(0, 100, name='Classifier')
    >>> A.begin
    0.0
    >>> A.end
    100.0
    >>> A.name
    'Classifier'
    >>> A.Sets
    {}

    Параметры конструктора:
    begin
         начало интервала определения классификатора
    end
         конец интервала определения классификатора
    name
         имя классификатора

    Поля класса:
    Sets
        Ассоциативный массив, содержащий, соответственно, имя и объект типа
        Subset, для каждого терма нечеткого множества.
    '''
    begin=0.0
    end  =1.0
    Sets={}
    name=''
    def __init__(self, begin, end, name=''):
        self.begin=float(begin)
        self.end=float(end)
        self.Sets={}
        self.name=name
    def __iter__(self):
        '''Процедура перебора термов классификатора.
        Синтаксис:
            >>> for term in Classifier:
            >>>     print term.centr()
        '''
        for i in self.Sets.iterkeys():
            yield i
    def __getitem__(self, param):
        '''
        Для быстрого доступа к подмножеству нечеткого множества, терму
        классификатора или значению лингвистической переменной можно
        использовать следующий синтаксис:
            >>> Clas=Classifier(p=[0.0, 0.1, 0.3, 0.4, 0.6, 1.0], u=1.2)
            >>> Clas['1']
        '''
        return self.Sets[param]
    def add_term(self, sub, name=''):
        '''
        Добавляет терм к данному классификатору. Порядок термов не важен.
        Синтаксис:
        >>> A=FuzzySet(0, 100)
        >>> S=Gaussian(20, 10)
        >>> A.add_term(S, name='term1')
        >>> A.Sets['term1'].mu
        20.0
        >>> A.add_term(Triangle(30, 50, 75), name='term2')
        >>> A.Sets['term2'].b
        50.0

        Параметры:
        S
            Нечеткое подмножество типа Subset, или любого производного,
            играющее роль терма нечеткого множества (классификатора)
        name
            Строка, идентифицирующая терм в составе данного множества.
            Используется для построении легенды в методе plot(), а также как
            ключ ассоциативного массива Sets

        '''
##        sub.begin=self.begin
##        sub.end=self.end
        self.Sets[name]=sub
    def find(self, x, term):
        '''
        Возвращает значение принадлежности точки x терму term
        Синтаксис:
            >>> for key, value in Clas.Sets.iteritems():
            >>>    sum+=Clas.find(i, key)
        '''
        return self.Sets[term].value(x)
        pass
    def classify(self, ss):
        '''
        Возвращает имя терма, наиболее соответствующего переданному элементу.
        Будучи вызванным у квалификатора, соответствует квалификации точного
        значения или значения, выраженного нечетким подмножеством или числом.
        Синтаксис:
            >>> C=std_5_Classificator()
            >>> C.classify(0.2)
            'II'
            >>> C.classify(0.8)
            'IV'
            >>> C.classify(1.0)
            'V'
            >>> C.classify(0.0)
            'I'
            >>> C.classify(Triangle(0.4, 0.5, 0.6))
            'III'
            >>> C.classify(Triangle(0.4, 0.5, 1.6))
            'IV'
            >>> C.classify(Triangle(-1.4, 0.5, 0.6))
            'II'
            >>> C.classify(Triangle(-1.4, 0.0, 0.6))
            'I'
        '''
        # XXX различные методы классификации: встроить как поле в классификатор?
        res={}
        if isinstance(ss, Subset):
            for i in self.Sets.iterkeys():
                t=ss & self.Sets[i]
                res[i]=t.card()
        else:
            for i in self.Sets.iterkeys():
                t=self.Sets[i].value(ss)
                res[i]=t
        maxim=0
        name=None
        for i in res.iterkeys():
            if res[i]>maxim:
                maxim=res[i]
                name=i
        return name
    def __str__(self, ss):
        '''
        Процедура для вывода описания классификатора в текстовом виде
        Синтаксис:
            >>> print Classifier
        '''
        res={}
        if isinstance(ss, Subset):
            for i in self.Sets.iterkeys():
                t=ss & self.Sets[i]
                r=t.card()
                if r<>0.0:res[i]=r
        else:
            for i in self.Sets.iterkeys():
                t=self.Sets[i].value(ss)
                if t<>0.0:res[i]=t
        return res
    def plot(self):
        '''
        Отображает нечеткое множество графически. Все термы представляются на
        одном графике.
        '''
        labels=[]
        for name, sub in self.Sets.iteritems():
            sub.plot(verbose=False)
##            x=[]
##            y=[]
##            for i in self.traversal():
##                x.append(i)
##                y.append(sub.value(i))
##            p.plot(x, y)
            labels.append(name)
##            print sub
        p.legend(labels, loc='upper right')
        p.plot(self.begin, 1.01)
        p.plot(self.end+(self.end-self.begin)/5, -0.01)
        p.title(self.name)
        p.grid()

class TriangleClassifier(FuzzySet):
    '''
    Равномерный классификатор с термами в виде равноскатных треугольных чисел.

    Синтаксис:
    >>> A=TriangleClassifier(begin=0.0, end=1.0, name='', names=[], edge=0, cross=1)

    Параметры конструктора (см. FuzzySet):
    names
         список строк, каждая из которых представляет собой имя терма,
         входящего в данный классификатор. Порядок термов соблюдается.
    edge
         параметр, задающий расположение термов.
         Если edge=False, то первый и последний термы будут иметь вершины в точках,
         соответственно, начала и конца интервала определения классификатора:
         >>> names=['1', '2', '3']
         >>> A=TriangleClassifier(names=names, edge=0)
         >>> A.Sets['1'].b
         0.0
         >>> A.Sets['2'].b
         0.5
         >>> A.Sets['3'].b
         1.0

         Если edge=True, то первый и последний термы будут иметь отступ от границ
         интервала определения, равный отступу между термами:
         >>> A=TriangleClassifier(names=names, edge=1)
         >>> A.Sets['1'].b
         0.25
         >>> A.Sets['2'].b
         0.5
         >>> A.Sets['3'].b
         0.75

    cross
         Параметр задает степень пересечения термов классификатора.
         Может принимать значения от 0 до бесконечности.
         При cross=1 каждый объект области определения принадлежит только одному
         множеству.
         Функции принадлежности соседних термов расположены "впритык".
         >>> A=TriangleClassifier(names=names, cross=1.0)
         >>> A.Sets['1'].c
         0.25
         >>> A.Sets['2'].a
         0.25
         >>> A.Sets['2'].c
         0.75
         >>> A.Sets['3'].a
         0.75

         При cross=2 функции принадлежности строятся таким образом, что каждый
         терм покрывает ровно половину ширины соседних термов. Таким образом,
         каждая точка области определения принадлежит двум нечетким
         подмножествам.
         >>> A=TriangleClassifier(names=names, cross=2.0)
         >>> A.Sets['1'].c
         0.5
         >>> A.Sets['2'].b
         0.5
         >>> A.Sets['2'].c
         1.0
         >>> A.Sets['3'].a
         0.5
         >>> A.Sets['3'].b
         1.0

         При 0 < cross < 1 между термами классификатора появляются интервалы,
         значения в которых не принадлежат ни одному терму.
         При cross=0 термы вырождаются в точку.
    '''
    names=[]
    edge=0
    cross=1
    def __init__(self, begin=0.0, end=1.0, name='', names=[], edge=False, cross=1.0):
        self.begin=float(begin)
        self.end=float(end)
        self.Sets={}
        self.name=name
##        print names
        if not names: return None
        if not edge:
            wide=(end-begin)*(cross)/(len(names)*2-2)
            step=(end-begin)/(len(names)-1)
            p=0
        else:
            wide=(end-begin)*(cross)/((len(names)+1)*2)
            step=(end-begin)/(len(names)+1.0)
            p=(end-begin)/(len(names)+1.0)
        for name in names:
##            print name, p
            self.add_term(Triangle(p-wide, p, p+wide), name=name)
            p=p+step
class GaussianClassifier(FuzzySet):
    '''
    Равномерный классификатор с термами в виде гауссиан.

    Синтаксис:
    >>> A=GaussianClassifier(begin=0.0, end=1.0, name='', names=[], edge=0, cross=1)

    Параметры конструктора (см. FuzzySet, TriangleClassifier):
    '''
    def __init__(self, begin=0.0, end=1.0, name='', names=[], edge=0, cross=1.0):
        self.begin=float(begin)
        self.end=float(end)
        self.Sets={}
        self.name=name
        if not names: return None
        if edge==0:
            wide=(end-begin)*(cross)/(len(names)*2-2)
            step=(end-begin)/(len(names)-1)
            p=0
        else:
            wide=(end-begin)*(cross)/((len(names)+1)*2)
            step=(end-begin)/(len(names)+1)
            p=(end-begin)/(len(names)+1)
        for name in names:
            self.add_term(Gaussian(p, wide), name=name)
            p=p+step
def std_2_Classificator(begin=0.0, end=1.0, name='', gauss=False):
        '''
        Процедура создания равномерного линейного или гауссового классификатора,
        состоящего из двух термов. Термы маркируются латинскими цифрами ('I', 'II',
        и т. д. ). Вспомогательная процедура, призванная облегчить и ускорить
        создание классификаторов.
        Синтаксис:
            >>> D=std_2_Classificator(begin=0, end=100, name='percentage', gauss=True)
        Параметры:
            begin, end
                задают границы области определения классификатора
            name
                имя классификатора
            gauss
                если True, создается классификатор с термами в виде гауссиан. Иначе
                 - с треугольными термами. По умолчанию - False
        '''
        if gauss:
            return GaussianClassifier(begin=begin, end=end, names=['I', 'II'], name=name, cross=2.0)
        else:
            return TriangleClassifier(begin=begin, end=end, names=['I', 'II'], name=name, cross=2.0)
def std_3_Classificator(begin=0.0, end=1.0, name='', gauss=False):
        '''
        Процедура создания равномерного линейного или гауссового классификатора,
        состоящего из трех термов. Термы маркируются латинскими цифрами ('I', 'II',
        и т. д. ). Вспомогательная процедура, призванная облегчить и ускорить
        создание классификаторов.
        Синтаксис:
            >>> D=std_3_Classificator(begin=0, end=100, name='percentage', gauss=True)
        Параметры:
            begin, end
                задают границы области определения классификатора
            name
                имя классификатора
            gauss
                если True, создается классификатор с термами в виде гауссиан. Иначе
                 - с треугольными термами. По умолчанию - False
        '''
        if gauss:
            return GaussianClassifier(begin=begin, end=end, names=['I', 'II', 'III'], name=name, cross=2.0)
        else:
            return TriangleClassifier(begin=begin, end=end, names=['I', 'II', 'III'], name=name, cross=2.0)
def std_5_Classificator(begin=0.0, end=1.0, name='', gauss=False):
        '''
        Процедура создания равномерного линейного или гауссового классификатора,
        состоящего из пяти термов. Термы маркируются латинскими цифрами ('I', 'II',
        и т. д. ). Вспомогательная процедура, призванная облегчить и ускорить
        создание классификаторов.
        Синтаксис:
            >>> D=std_5_Classificator(begin=0, end=100, name='percentage', gauss=True)
        Параметры:
            begin, end
                задают границы области определения классификатора
            name
                имя классификатора
            gauss
                если True, создается классификатор с термами в виде гауссиан. Иначе
                 - с треугольными термами. По умолчанию - False
        '''
        if gauss:
            return GaussianClassifier(begin=begin, end=end, names=['I', 'II', 'III', 'IV', 'V'], name=name, cross=2.0)
        else:
            return TriangleClassifier(begin=begin, end=end, names=['I', 'II', 'III', 'IV', 'V'], name=name, cross=2.0)
def std_7_Classificator(begin=0.0, end=1.0, name='', gauss=False):
        '''
        Процедура создания равномерного линейного или гауссового классификатора,
        состоящего из семи термов. Термы маркируются латинскими цифрами ('I', 'II',
        и т. д. ). Вспомогательная процедура, призванная облегчить и ускорить
        создание классификаторов.
        Синтаксис:
            >>> D=std_7_Classificator(begin=0, end=100, name='percentage', gauss=True)
        Параметры:
            begin, end
                задают границы области определения классификатора
            name
                имя классификатора
            gauss
                если True, создается классификатор с термами в виде гауссиан. Иначе
                 - с треугольными термами. По умолчанию - False
        '''
        if gauss:
            return GaussianClassifier(begin=begin, end=end, names=['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'], name=name, cross=2.0)
        else:
            return TriangleClassifier(begin=begin, end=end, names=['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'], name=name, cross=2.0)

class Classifier(FuzzySet):
      '''
      Данный класс создает линейный неравномерный классификатор по точкам,
      указанным в параметрах. Характерной особенностью данного классификатора
      являтеся то, что для каждого элемента носителя сумма принадлежностей всех
      термов равна 1,0. Классификатор строится на действительном интервале.
      Термы классификатора именуются арабскими числами, начиная с 1.
      Синтаксис:
        >>> Clas=Classifier(p=[0.0, 0.1, 0.3, 0.4, 0.6, 1.0], u=0.2)
      Параметры:
        name
            имя классификатора
        begin
            начало области определения
        end
            конец области определения
        p
            массив чисел, представляющих центры интервалов толерантности термов
        u
            параметр, задающий крутизну скатов ФП термов и ширину интервала
            толерантности. При u=0 классификатор становится четким, при
            u=1 ФП термов становятся треугольными.
      '''
      def __init__(self, begin=0.0, end=1.0, p=[], u=1.0, name=''):
          self.begin=float(begin)
          self.end=float(end)
          self.Sets={}
          self.name=name
          n=len(p)
          p=sorted(p)
          p.insert(0, begin)
          p.append(end)
          u=math.tan(float(u)*math.pi/2)
          for i in range(n):
              ly=(p[i+1]-p[i])/(u+2)
              ry=(p[i+2]-p[i+1])/(u+2)
              a=p[i+1]-ly*(1+u)
              b=p[i+1]-ly
              c=p[i+1]+ry
              d=p[i+1]+ry*(1+u)
              Ss=Trapezoidal(begin=a, begin_tol=b, end_tol=c, end=d)
              self.add_term(Ss, name=str(i))

##if __name__ == "__main__":
##    import doctest
####    doctest.testmod(verbose=False)
##    doctest.testmod(verbose=True)