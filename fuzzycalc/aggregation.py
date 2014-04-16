# -*- coding: UTF-8 -*-

'''Модуль для работы с механизмом нечеткого вывода.

Позволяет строить простейшие нечеткие экспертные системы (FES) путем построения
нечетких подмножеств на деревьях особого типа.
Синтаксис:
    >>> from FuzzySet import *
    >>> # создаем классификаторы:
    >>> C1=std_5_Classificator(name='Classifier 1')
    >>> C2=std_3_Classificator(name='Classifier 2', begin=0.0, end=100.0)
    >>> C3=std_2_Classificator(name='Classifier 3', begin=10.0, end=30.0)
    >>> # создаем дерево
    >>> T=Ruled(name='Rule system', clas=C1)
    >>> T.add(Ruled(name='Factor 1', clas=C2))
    >>> T.add(Ruled(name='Factor 2', clas=C3))
    >>> # добавляем правила
    >>> T.add_rule({'Factor 1':'I',   'Factor 2':'I', }, concl='I'  )
    >>> T.add_rule({'Factor 1':'I',   'Factor 2':'II',}, concl='II' )
    >>> T.add_rule({'Factor 1':'II',  'Factor 2':'I', }, concl='II' )
    >>> T.add_rule({'Factor 1':'II',  'Factor 2':'II',}, concl='III')
    >>> T.add_rule({'Factor 1':'III', 'Factor 2':'I', }, concl='III')
    >>> T.add_rule({'Factor 1':'III', 'Factor 2':'II',}, concl='III')
    >>> # добавляем оценки
    >>> T['Factor 1'].set_estim(6.5)
    >>> T['Factor 2'].set_estim(12.6)
    >>> print T.get_estim()
    9.55
    >>> # получаем результат с использованием разных t-норм
    >>> T.tnorm=min_max()
    >>> T._calculate()  #doctest: +SKIP
    <FuzzySubset.Subset instance at 0x0292EF80>
    >>> print T.get_estim()
    9.55
    >>> T.tnorm=sum_prod()
    >>> T._calculate()  #doctest: +SKIP
    <FuzzySubset.Subset instance at 0x02B3A3F0>
    >>> print T.get_estim()
    9.55
    >>> T.tnorm=margin()
    >>> T._calculate()  #doctest: +SKIP
    <FuzzySubset.Subset instance at 0x02B3A788>
    >>> print T.get_estim()
    9.55
'''

from .subset import Interval
from .domain import Domain

class AggregationMetod(object):
    '''
    Класс определяет интерфейс к различным методам агрегации частных показателей
    в интегральный. Подклассы данного класса реализуют алгоритмы интеграции
    различных типов нечетких контроллеров.
    '''
    def _calculate(self, host):
        pass

class Simple(AggregationMetod):
    '''
    Метод агрегации показателей, в котором интегральный показатель расчитывается
    как среднее арифметическое частных.
    '''
    def _calculate(self, host):
        est = 0.0
        w = 0.0
        for child in host.childs.values():
            try:
                est += float(child.get_estim())
            except TypeError:
                return None
            w += 1.0
        if w == 0.0: return None
        else:
            host.estimation = est/w
            return host.estimation

class Rules(AggregationMetod):
    '''
    Данный класс объединяет группу методов расчета интегральных показетелей,
    основанных на использовании системы нечетких правил. Все типы нечеткого
    вывода, использующие правила вывода реализуются классами, дочерними от
    данного.
    '''
    rules = []
    def __init__(self):
        self.rules = []
    def add_rule(self, ant={}, concl='', name=''):
        '''
        Данный метод позволяет добавить систему правил, согласно которой будет
        вычисляться оценка текущего узла дерева (к которому применен метод) в
        зависимости от оценок его потомков.
        Нечеткое правило состоит из посылки и заключения. Посылка описывает
        при каких значениях факторов результирующая оценка принимает значение,
        описанное в заключении. В посылке перечислены имена факторов и имена
        термов соответствующих им классификаторов; а в заключении - имя терма
        результирующего параметра.
        Синтаксис:
            >>> T=Ruled()
            >>> T.add_rule(name='rule 1',
                            ant={'factor': 'value'},
                            concl='value')  #doctest: +SKIP

        Параметры:
            ant
                Посылка нечеткого правила.
                Ассоциативный массив, в ключах которого задаются имена факторов,
                а в значениях - соответствующие имена значений лингвистической
                переменной. Предполагается, что в данном массиве перечислены
                посылки нечеткого правила, связанные логическим И. Для ввода
                правил, в посылке которых встречается союз ИЛИ используйте
                разбиение на несколько правил.
            concl
                Заключение нечеткого правила
                Имя терма классификатора, соответствующее данной посылке.
            name
                имя правила, используемое опционально для удобства.
        '''
##        # проверяем првильность параметров:
##        for param, value in ant.iteritems():
##            # param должен быть среди потомков
##            host[param]
##            # value должен быть среди термов его классификатора
##            host[param].classifier[value]
##        # concl должен быть среди термов собственного классификатора
##        host.classifier[concl]
        self.rules.append(Rule(ant=ant, concl=concl, name=name))
        pass

class Mamdani(rules):
    '''
    Данный класс реализует функциональность контроллера Мамдани, то есть
    классический алгоритм нечеткого композитного вывода.

    Для каждого правила из системы правил считается его вес: как t-норма
    принадлежности фактических значений показателей термам, упомянутым в
    посылке правила. Затем терм, соответствующий заключению правила обрезается
    на уровне, равном весу показателей.
    Таким образом, для каждого правила выводится НПМ на области определения
    результирующего показателя. Они объединяются путем применения к ним
    t-конормы и получившееся НПМ и бдет являться конечным результатом процесса
    нечеткого вывода.
    '''
    rules = []
    def __init__(self):
        self.rules = []
    def _calculate(self, host):
        from FuzzySubset import Interval
        # Начальное значение итогового НПМ. Для конормы это 0 уровень
        res = Interval(host.classifier.begin,
                       host.classifier.end,
                       tnorm=host.tnorm) * 0.0
        # для каждого правила вычисляем его альфу
        for rule in self.rules:
            alpha = 1.0 # Для t-нормы начальным значением будет 1
            # для каждого фактора в правиле
            for param, value in rule.ant.iteritems():
                # значение фактора
                fact = host[param].get_estim()
                # его принадлежность в классификаторе
                mem = host[param].classifier[value].value(fact)
                alpha = host.tnorm.t_norm(alpha, mem)
            rule.alpha = alpha
            # обрезаем терм собственного классификатора уровнем альфа
            Z = Interval(host.classifier.begin,
                         host.classifier.end) * rule.alpha & \
                         host.classifier[rule.concl]
            # и прибавляем его к существующим, используя конорму
            res = res.t_conorm(Z)
        return res

class Rules_accurate(rules):
    '''
    Данный алгоритм нечеткого вывода в общем аналогичен контроллеру Мамдани,
    однако, результат определяется как среднне арифметическое взвешенное по
    дефаззифицированным термам заключения каждого правила, причем весами
    являются веса соответствующего правила.
    '''
    rules = []
    def _calculate(self, host):
        sum_a = 0.0
        summ = 0.0
        # для каждого правила вычисляем его альфу
        for rule in self.rules:
            alpha = 1.0 # Для t-нормы начальным значением будет 1
            for param, value in rule.ant.iteritems(): # для каждого фактора в правиле
                fact = host[param].get_estim()   # значение фактора
                mem = host[param].classifier[value].value(fact)   # его принадлежность в классификаторе
                alpha = host.tnorm.t_norm(alpha, mem)
            rule.alpha = alpha
            sum_a += alpha
            summ += host.classifier[rule.concl].centr()*alpha
        if sum_a == 0:
            return 0.0
        return summ/sum_a

class Rule:
    '''
    Описание
    Синтаксис:
        >>>
    '''
    ant = {}
    concl = ''
    name = ''
    alpha = ''
    def __init__(self, ant={}, concl='',  name=''):
        self.concl = concl
        self.name = name
        self.ant = ant
    def __str__(self):
        res=str(self.name)+': '
        for (name, value) in self.ant.iteritems():
            res+=str(name)+'='+value+' '
        res+=' -> '+str(self.concl) + '(' + str(self.alpha)+')'
        return res

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

class Ruled(Tree):
    '''
    Данный класс используется при построении дерева нечетких оценок, в котором
    оценка текущего  узла связана с оценками его потомков набором правил
    нечеткого вывода.
    Синтаксис:
        см. FuzzyDomain.Tree
    '''

    # TODO описание с примерами
    # XXX графическое отображение всего FES. классификаторы, правила,
    # четкие значения, результирующее НПМ, вывод.

    rules = []

    def __init__(self):
        pass

    def add_rule(self, ant=None, concl='', name=''):
        '''
        Данный метод позволяет добавить систему правил, согласно которой будет
        вычисляться оценка текущего узла дерева (к которому применен метод) в
        зависимости от оценок его потомков.
        Нечеткое правило состоит из посылки и заключения. Посылка описывает
        при каких значениях факторов результирующая оценка принимает значение,
        описанное в заключении. В посылке перечислены имена факторов и имена
        термов соответствующих им классификаторов; а в заключении - имя терма
        результирующего параметра.
        Синтаксис:
            >>> T=Ruled()
            >>> T.add_rule(name='rule 1',
                            ant={'factor': 'value'},
                            concl='value')  #doctest: +SKIP

        Параметры:
            ant
                Посылка нечеткого правила.
                Ассоциативный массив, в ключах которого задаются имена факторов,
                а в значениях - соответствующие имена значений лингвистической
                переменной. Предполагается, что в данном массиве перечислены
                посылки нечеткого правила, связанные логическим И. Для ввода
                правил, в посылке которых встречается союз ИЛИ используйте
                разбиение на несколько правил.
            concl
                Заключение нечеткого правила
                Имя терма классификатора, соответствующее данной посылке.
            name
                имя правила, используемое опционально для удобства.
        '''

        if not ant:
            ant = {}

##        # проверяем првильность параметров:
##        for param, value in ant.iteritems():
##            # param должен быть среди потомков
##            self[param]
##            # value должен быть среди термов его классификатора
##            self[param].classifier[value]
##        # concl должен быть среди термов собственного классификатора
##        self.classifier[concl]
        self.rules.append(Rule(ant=ant, concl=concl, name=name))

    def _calculate(self):
        # Начальное значение итогового НПМ. Для конормы это 0 уровень
        res = Interval(self.classifier.begin,
                       self.classifier.end,
                       tnorm=self.tnorm) * 0.0
        self._weights() # считаем веса всех правил
        for rule in self.rules:
            # обрезаем терм собственного классификатора уровнем альфа
            subset = Interval(self.classifier.begin,
                              self.classifier.end)*rule.alpha & \
                              self.classifier[rule.concl]
            # и прибавляем его к существующим, используя конорму
            res = res.t_conorm(subset)
        return res
    def _weights(self):
        # для каждого правила вычисляем его альфу
        for rule in self.rules:
            alpha = 1.0 # Для t-нормы начальным значением будет 1
            # для каждого фактора в правиле
            for param, value in rule.ant.iteritems():
                # значение фактора
                fact = self[param].get_estim()
                # его принадлежность в классификаторе
                mem = self[param].classifier[value].value(fact)
                alpha = self.tnorm.t_norm(alpha, mem)
            rule.alpha = alpha

# XXX интерфейс FES с модельными параметрами и возможностью задания
# пользовательских и изменения на лету.

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    #~ doctest.testmod(verbose=True)
