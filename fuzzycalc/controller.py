# -*- coding: UTF-8 -*-

'''
'''

from .aggregation import Simple, Tree, rules
from .tnorm import MinMax


class Controller(object):
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
        input_
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
        trees
            Ассоциативный массив, ключами которого являются имена выходных
            переменных контроллера, а значениями - соответствующие им деревья
            (см. FuzzyDomain.Tree)
        inputs
            Ассоциативный массив, ключами которого являются имена входных
            переменных контроллера, а значениями - соответствующие им множества
            терм-значений (классификаторы). См. FuzzySet.FuzzySet
        method
        tnorm
    '''

    trees = {}
    inputs = {}
    method = None
    tnorm = None

    def __init__(self, input_=None,
                        out=None,
                        rules=None,
                        method=Simple(),
                        tnorm=MinMax()):
        '''
        Описание
        Синтаксис:
            >>>
        '''

        if not input_:
            input_ = {}
        if not out:
            out = {}
        if not rules:
            rules = []

        self.method = method
        self.tnorm = tnorm

        self.define_input(input_)
        self.define_output(out)
        self.define_rules(rules)

    def _char(self):
        print "<Fuzzy controller>"
        for name in self.trees.itervalues():
            for i in name:
                print i
            print
        print 'Rules:'
        for tree in self.trees.itervalues():
            if isinstance(tree.agg, rules):
                for rule in tree.agg.rules:
                    print rule
        print
        print '</Fuzzy controller>'

    def define_input(self, input_):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        self.inputs = {}
        for name in input_.iterkeys():
            self.inputs[name] = Tree(name=name, clas=input_[name])
    def define_output(self, out):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        self.trees = {}
        for name in out.iterkeys():
            tree = Tree(name=name,
                     clas=out[name],
                     agg=self.method(),
                     tnorm=self.tnorm)
            for branch in self.inputs.itervalues():
                tree.add(branch)
            self.trees[name] = tree
    def add_input(self, name, clas):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        self.inputs[name] = Tree(name=name, clas=clas)

    def add_output(self, name, clas):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        tree = Tree(name=name, clas=clas, agg=self.method(), tnorm=self.tnorm)
        for branch in self.inputs.itervalues():
            tree.add(branch)
        self.trees[name] = tree

    def define_rules(self, rules):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        if isinstance(self.method(), rules):
            i = 0
##            print 'Adding rules...'
            for rule in rules:
                ant, conc = rule
                for name in conc.iterkeys():
##                    print ant
                    self.trees[name].agg.add_rule(name='rule '+str(i),
                                                    ant=ant,
                                                    concl=conc[name])
##                    print 'added to', name
##                    for rule in self.trees[name].agg.rules:
##                        print rule
                    i += 1
##                print

    def add_rule(self, rule, name=''):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        # TODO
        pass
    def set(self, input_values):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        for name in input_values.iterkeys():
            self.inputs[name].set_estim(input_values[name])

    def get(self):
        '''
        Описание
        Синтаксис:
            >>>
        '''
        res = {}
        for tree in self.trees.itervalues():
            res[tree.name] = tree.get_estim()
        return res

##    def plot(self):
##        n=len(self.inputs)
##        m=len(self.trees)
##        a=(n+1)*(m+1)
        #TODO вывод классификаторов входов
        #TODO вывод классификаторов выходов
        #TODO вывод двумерных графиков

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    #~ doctest.testmod(verbose=True)
