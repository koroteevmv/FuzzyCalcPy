# -*- coding: UTF-8 -*-
from FuzzyCalc_Common import *
from FuzzyDomain import *

class Controller():
    '''
    Данный класс представляет интерфейс для создания нечеткого контроллера со
    множественными входами и выходами. Входом нечеткого контроллера называется
    лингвистическая переменная, имеющая имя и множество терм-значений
    (классификатор), которой присваивается четкое, нечеткое или лингвистическое
    значение. Выходом контроллера называется лингвистическая переменная,
    имеющая имя и множество терм-значений, значение которой рассчитывается,
    исходя из значений входных переменных по определенному алгоритму, который
    называется тип контроллера (см. FuzzyDomain.AggregationMethod).

    Синтаксис:
        >>>
    Параметры конструктора:
        input
            C помощью этого параметра задаются входные переменные контроллера.
            В этот параметр следует передать ассоциативный массив, ключами
            которого являются строки-имена входных переменных, а значениями -
            соответствующие классификаторы, задающие терм-множество каждой
            переменной.
        out
            Подобным же образом задаются и выходные переменные классификатора.
        rules
            В данный параметр передаются нечеткие правила вывода (если они
            требуются). Следует передать массив, в котором каждый элемент это
            правило, представленное в виде пары (tuple) посылки и заключения,
            каждая из которых представлена в виде ассоциативного массива с
            ключами - именами переменны и значениями - именами термов.
        method
            Данный параметр определяет тип контроллера. Фактически он задает
            метод (алгоритм) сводки частных показателей в интегральный. Может
            принимать в качестве значения имя любого подкласса
            FuzzyDomain.AggregationMethod.
        tnorm
            Определяет пару треугольных норм и конорм
    Поля класса:
        Trees
            Ассоциативный массив, ключами которого являются имена выходных
            переменных контроллера, а значениями - соответствующие им деревья
            (см. FuzzyDomain.Tree)
        Inputs
            Ассоциативный массив, ключами которого являются имена входных
            переменных контроллера, а значениями - соответствующие им множества
            терм-значений (классификаторы). См. FuzzySet.FuzzySet
        method
        tnorm
    '''
    Trees={}
    Inputs={}
    method=None
    tnorm=None
    def __init__(self, input={}, out={}, rules=[], method=simple(), tnorm=min_max()):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        self.Trees={}
        self.Inputs={}
        self.method=method
        self.tnorm=tnorm
        for name in input.iterkeys():
            T=Tree(name=name, clas=input[name])
            self.Inputs[name]=T
        for name in out.iterkeys():
            T=Tree(name=name, clas=out[name], agg=self.method(), tnorm=self.tnorm)
            for tree in self.Inputs.itervalues():
                T.add(tree)
            self.Trees[name]=T
            pass
        if isinstance(self.method(), FuzzyDomain.rules):
            i=0
##            print 'Adding rules...'
            for rule in rules:
                ant, conc=rule
                for name in conc.iterkeys():
##                    print ant
                    self.Trees[name].agg.add_rule(name='rule '+str(i), ant=ant, concl=conc[name])
##                    print 'added to', name
##                    for rule in self.Trees[name].agg.rules:
##                        print rule
                    i+=1
##                print
        pass
    def _char(self):
        print "<Fuzzy controller>"
        for name in self.Trees.itervalues():
            for i in name:
                print i
            print
        print 'Rules:'
        for tree in self.Trees.itervalues():
            if isinstance(tree.agg, rules):
                for rule in tree.agg.rules:
                    print rule
        print
        print '</Fuzzy controller>'
    def define_input(self, input):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        self.Inputs={}
        for name in input.iterkeys():
            T=Tree(name=name, clas=input[name])
            self.Inputs[name]=T
        pass
    def define_output(self, out):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        self.Trees={}
        for name in out.iterkeys():
            T=Tree(name=name, clas=out[name], agg=self.method(), tnorm=self.tnorm)
            for tree in self.Inputs.itervalues():
                T.add(tree)
            self.Trees[name]=T
        pass
    def add_input(self, name, clas):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        T=Tree(name=name, clas=clas)
        self.Inputs[name]=T
        pass
    def add_output(self, name, clas):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        T=Tree(name=name, clas=clas, agg=self.method(), tnorm=self.tnorm)
        for tree in self.Inputs.itervalues():
            T.add(tree)
        self.Trees[name]=T
        pass
    def define_rules(self, rules):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        if isinstance(self.method(), FuzzyDomain.rules):
            i=0
##            print 'Adding rules...'
            for rule in rules:
                ant, conc=rule
                for name in conc.iterkeys():
##                    print ant
                    self.Trees[name].agg.add_rule(name='rule '+str(i), ant=ant, concl=conc[name])
##                    print 'added to', name
##                    for rule in self.Trees[name].agg.rules:
##                        print rule
                    i+=1
##                print
        pass
    def add_rule(self, rule, name=''):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        pass
    def set(self, x):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        for name in x.iterkeys():
            self.Inputs[name].set_estim(x[name])
        pass
    def get(self):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        res={}
        for tree in self.Trees.itervalues():
            res[tree.name]=tree.get_estim()
        return res
        pass
##    def plot(self):
##        n=len(self.Inputs)
##        m=len(self.Trees)
##        a=(n+1)*(m+1)
##        # вывод классификаторов входов
##        # вывод классификаторов выходов
##        # вывод двумерных графиков
