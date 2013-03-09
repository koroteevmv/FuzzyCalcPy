# -*- coding: UTF-8 -*-
'''
Модуль, описывающий различные типы носителей нечетких множеств, а также
реализующий функциональность нечетких правил логического вывода.
'''
from FuzzyCalc_Common import *
from FuzzyAggregation import *

class t_norm:
    '''
    Описание
    Синтаксис:
        >>>
    '''
    def t_norm(self, other):
        pass
    def t_conorm(self, other):
        pass

class min_max(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    def t_norm(self, x, y):
        return min(x, y)
    def t_conorm(self, x, y):
        return max(x, y)
class sum_prod(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    def t_norm(self, x, y):
        return x*y
    def t_conorm(self, x, y):
        return x+y-x*y
class margin(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    def t_norm(self, x, y):
        return max(x+y-1, 0)
    def t_conorm(self, x, y):
        return min(x+y, 1)
class drastic(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    def t_norm(self, x, y):
        if x==1: return y
        elif y==1: return x
        else: return 0
    def t_conorm(self, x, y):
        if x==0: return y
        elif y==0: return x
        else: return 1
class norm1(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    p=None
    def __init__(self, p):
        self.p=p
    def t_norm(self, x, y):
        return x*y/(self.p+(1-self.p)*(x+y-x*y))
    def t_conorm(self, x, y):
        return ( x+y-(2-self.p)*x*y )/( 1-(1-self.p)*x*y )
class norm2(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    p=None
    def __init__(self, p):
        self.p=p
    def t_norm(self, x, y):
        return x*y / max(x, y, self.p)
    def t_conorm(self, x, y):
        return (x+y-x*y-min(x, y, 1-self.p)) / max(1-a, 1-b, self.p)
class norm3(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    p=None
    def __init__(self, p):
        self.p=p
    def t_norm(self, x, y):
        try:
            return 1/( 1+ ((1/x - 1)**self.p + (1/y - 1)**self.p)**(1/self.p) )
        except ZeroDivisionError: return 0.0
    def t_conorm(self, x, y):
        return 1/( 1+ ((1/x - 1)**-self.p + (1/x - 1)**-self.p)**(1/self.p) )
class norm4(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    p=None
    def __init__(self, p):
        self.p=p
    def t_norm(self, x, y):
        return 1 - ((1-x)**self.p+(1-y)**self.p-(1-x)**self.p*(1-y)**self.p)**(1/self.p)
    def t_conorm(self, x, y):
        return (x**self.p + y**self.p - x**self.p*y**self.p)**(1/self.p)
class norm5(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    p=None
    def __init__(self, p):
        self.p=p
    def t_norm(self, x, y):
        return max((1 - ((1-x)**self.p + (1-y)**self.p)**(1/self.p)), 0)
    def t_conorm(self, x, y):
        return min((x**self.p + y**self.p), 1)
class norm6(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    p=None
    def __init__(self, p):
        self.p=p
    def t_norm(self, x, y):
        try:
            return math.log((1+ (self.p**x -1)*(self.p**y -1)/(self.p-1) ), self.p)
        except ZeroDivisionError: return 0.0
    def t_conorm(self, x, y):
        return 1 - math.log((1+ (self.p**(1-x) + self.p**(1-y))/(self.p-1) ), self.p)
class norm7(t_norm):
    '''
    Описание
    Синтаксис:
        >>>
    '''
    p=None
    def __init__(self, p):
        self.p=p
    def t_norm(self, x, y):
        return max((x+y-1+self.p*x*y)/(1+self.p), 0)
    def t_conorm(self, x, y):
        return min((x+y-1+self.p*x*y), 1)

class Domain:
    '''
        Абстрактный класс, реализующий интерфейс носителя
        нечеткого множества. Смысловую нагрузку несут подклассы этого класса,
        представляющие различные виды носителей. Преимуществом такого подхода
        является его универсальность: в качестве носителя при определении нечеткого
        множества можно задавать действительный интервал, целочисленный интервал,
        в принципе, любую итерируемую структуру.
    '''
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def char(self):
        for i in self:
            print i
    pass

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
    begin=0.0
    end=1.0
    delta=0.01
    acc=ACCURACY
    def __init__(self, begin=0.0, end=1.0, acc=ACCURACY):
        self.begin=float(begin)
        self.end=float(end)
        self.acc=acc
        pass
    def __iter__(self):
        if (self.begin==self.end):
           for i in range(self.acc):
               yield self.begin
        else:
            self.delta=(self.end-self.begin)/(self.acc)
            i=self.begin
            while i<self.end+self.delta:
                  yield i
                  i+=self.delta
    pass

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

                >>> A=Trapezoidal(begin=0.0, begin_tol=2.0, end_tol=2.0, end=3.0, domain=B)
                >>> print A
                1.66666666667
                >>> A.char()
                0.0 0.0
                1.0 0.5
                2.0 1.0
                3.0 -0.0

      '''
      begin=0
      end=100
      def __init__(self, begin=0.0, end=1.0):
        self.begin=begin
        self.end=end
        pass
      def __iter__(self):
            i=self.begin
            while i<self.end+1:
                  yield i
                  i+=1


class Tree(Domain):
    '''
    Представляет собой носитель нечеткого множества в виде иерархической
    структуры (дерева), в которой оценка данного узла зависит определенным
    образом от оценок его потомков.
    Конструктор данного класса создает как само дерево, так и его потомков.
    Листовой элемент дерева - это тот, для которого не создано ни одного потомка.
    Синтаксис:
        >>> A=Tree('tree')
        >>> A.add(Tree('branch 1'))
        >>> A.add(Tree('branch 2'))
        >>> A.add(Tree('branch 3'))
        >>> A['branch 1'].add(Tree('branch 1 1'))
        >>> A['branch 1'].add(Tree('branch 1 2'))
        >>> A['branch 1'].add(Tree('branch 1 3'))
        >>> A['branch 1']['branch 1 2'].add(Tree('leaf 1 2 1'))
        >>> A['branch 1']['branch 1 2'].add(Tree('leaf 1 2 2'))
        >>> A['branch 1']['branch 1 2'].add(Tree('leaf 1 2 3'))
        >>> A.char()
        branch 1 3 - None (1.0)
        leaf 1 2 1 - None (1.0)
        leaf 1 2 3 - None (1.0)
        leaf 1 2 2 - None (1.0)
        branch 1 2 - None (1.0)
        branch 1 1 - None (1.0)
        branch 1 - None (1.0)
        branch 2 - None (1.0)
        branch 3 - None (1.0)
        tree - None (1.0)
        >>> A=Tree('name', estim=2.5, weight=0.23, clas=std_3_Classifier(), tnorm=sum_prod)

    Параметры:
        name
            задает имя узла, по которому к нему можно будет обращаться
        estim
            степень принадлежности данного узла
        clas
            классификатор, используемый для оценки уровня данного параметра
        tnorm
            задает используемые при интеграции t-нормы и кономры. Подробнее см.
            FuzzyDomain.t_norm
        agg
            метод аггрегации частных показателей в интегральный.
            См. FuzzyDomain.AggregationMethod
    Переменные класса:
        childs
        name
        estimation
        weight
        classifier
        tnorm
    '''
    # TODO отделить МАИ от иерархического носителя
    # TODO реализовать в интерфейсе Subset иерархический носитель. Без изъебов типа весов и классификаторов. Но с A.value()
    childs={}
    name=''
    estimation=None
    classifier=None
    agg=simple
    tnorm=min_max()

    def __init__(self, name='', estim=None, agg=simple(), clas=None, tnorm=min_max()):
        self.name=name
        self.estimation=estim
        self.childs={}
        self.agg=agg
        self.classifier=clas
        self.tnorm=tnorm
    def __str__(self):
        '''
        Для быстрого вывода основной информации о дереве, поддереве или листе,
        можно использовать процедуру преобразования к строковому типу.
        Синтаксис:
            >>> T=Tree('tree')
            >>> T.add(Tree('branch 1', 2))
            >>> T.add(Tree('branch 2', 3))
            >>> print T
            tree - 2.5 (1.0)
            >>> print T['branch 1']
            branch 1 - 2 (1.0)

        Данный синтаксис можно комбинировать с синтаксисом __iter__ для вывода
        более полной информации о всех узлах дерева:
            >>> for i in T:
            ...     print i
            ...

        '''
        return self.name+' - '+ str(self.get_estim())
    def __iter__(self):
        '''
        Для быстрого перебора всех дочерних элементов дерева можно использовать
        объект данного класса как итератор. Порядок, в котором возвращаются
        узлы дерева соответствует алгоритму postorder traversal, то есть
        сначала перечисляются все дочерние узлы, затем родительский узел. и так
        для каждого узла, начиная с вершины.
        Синтаксис:
            >>> T=Tree('tree')
            >>> T.add(Tree('branch 1', 2))
            >>> T.add(Tree('branch 2', 3))
            >>> for i in T:
            ...     print i.name
            ...
            branch 1
            branch 2
            tree
        '''
        for leaf in self.childs.values():
            for i in leaf:
                yield i
        yield self
    def add(self, addition):
        '''
        Описание
        Синтаксис:
        Параметры:
            Параметр
                описание
        '''
        self.childs[addition.name]=addition
    def get_estim(self):
        if self.estimation or self.estimation==0.0:
            return self.estimation
        else:
            if self.childs==[]:
                return None
            return self.agg._calculate(self)
    def set_estim(self, e):
        self.estimation=e
    def __getitem__(self, param):
        '''
        Для быстрого доступа к любому из дочерних узлов дерева (не обязательно
        прямых потомков) по названию можно использовать следующий синтаксис:
            >>> T=Tree('tree')
            >>> T.add(Tree('branch 1', 2))
            >>> T.add(Tree('branch 2', 3))
            >>> T.char()
            branch 1 - 2 (1.0)
            branch 2 - 3 (1.0)
            tree - 2.5 (1.0)
            >>> print T['branch 1']
            branch 1 - 2 (1.0)
        '''
##        print 'im here!'
        return self.childs[param]
        pass

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    #~ doctest.testmod(verbose=True)
