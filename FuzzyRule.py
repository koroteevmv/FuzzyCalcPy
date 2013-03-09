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
from FuzzyCalc_Common import *
from FuzzySubset import *

class Ruled(Tree):
    '''
    Данный класс используется при построении дерева нечетких оценок, в котором
    оценка текущего  узла связана с оценками его потомков набором правил
    нечеткого вывода.
    Синтаксис:
        см. FuzzyDomain.Tree
    '''
    # TODO описание с примерами
    # XXX графическое отображение всего FES. классификаторы, правила, четкие значения, результирующее НПМ, вывод.
    rules=[]
    def add_rule(self, ant={}, concl='',  name=''):
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
            >>> T.add_rule(name='rule 1', ant={'factor': 'value'}, concl='value')  #doctest: +SKIP

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
        # проверяем првильность параметров:
        for param, value in ant.iteritems():
            # param должен быть среди потомков
            self[param]
            # value должен быть среди термов его классификатора
            self[param].classifier[value]
        # concl должен быть среди термов собственного классификатора
        self.classifier[concl]
        self.rules.append(Rule(ant=ant, concl=concl, name=name))
        pass
    def _calculate(self):
        # Начальное значение итогового НПМ. Для конормы это 0 уровень
        res=Interval(self.classifier.begin, self.classifier.end, tnorm=self.tnorm) * 0.0
        self._weights() # считаем веса всех правил
        for rule in self.rules:
            # обрезаем терм собственного классификатора уровнем альфа
            Z=Interval(self.classifier.begin, self.classifier.end)*rule.alpha & self.classifier[rule.concl]
            # и прибавляем его к существующим, используя конорму
            res=res.t_conorm(Z)
        return res
    def _weights(self):
        # для каждого правила вычисляем его альфу
        for rule in self.rules:
            alpha=1.0 # Для t-нормы начальным значением будет 1
            for param, value in rule.ant.iteritems(): # для каждого фактора в правиле
                fact=self[param].get_estim()   # значение фактора
                mem=self[param].classifier[value].value(fact)   # его принадлежность в классификаторе
                alpha=self.tnorm.t_norm(alpha, mem)
##                print rule.name, fact, mem, alpha
            rule.alpha=alpha

class Rule:
    ant={}
    concl=''
    name=''
    alpha=''
    def __init__(self, ant={}, concl='',  name=''):
        self.concl=concl
        self.name=name
        self.ant=ant

# XXX интерфейс FES с модельными параметрами и возможностью задания пользовательских и изменения на лету.

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    #~ doctest.testmod(verbose=True)
