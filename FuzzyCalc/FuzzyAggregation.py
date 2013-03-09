# -*- coding: UTF-8 -*-

from FuzzyCalc_Common import *

class AggregationMetod():
    '''
    Класс определяет интерфейс к различным методам агрегации частных показателей
    в интегральный. Подклассы данного класса реализуют алгоритмы интеграции
    различных типов нечетких контроллеров.
    '''
    def _calculate(self, host):
        pass

class simple(AggregationMetod):
    '''
    Метод агрегации показателей, в котором интегральный показатель расчитывается
    как среднее арифметическое частных.
    '''
    def _calculate(self, host):
        est=0.0
        w=0.0
        for child in host.childs.values():
            try:
##                est+=float(child.get_estim())*float(child.weight)
                est+=float(child.get_estim())
            except TypeError:
                return None
##            w+=float(child.weight)
            w+=1.0
        if w==0.0: return None
        else:
            host.estimation=est/w
            return host.estimation

class rules(AggregationMetod):
    '''
    Данный класс объединяет группу методов расчета интегральных показетелей,
    основанных на использовании системы нечетких правил. Все типы нечеткого
    вывода, использующие правила вывода реализуются классами, дочерними от
    данного.
    '''
    rules=[]
    def __init__(self):
        self.rules=[]
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
    rules=[]
    def __init__(self):
        self.rules=[]
    def _calculate(self, host):
        from FuzzySubset import Interval
        # Начальное значение итогового НПМ. Для конормы это 0 уровень
        res=Interval(host.classifier.begin, host.classifier.end, tnorm=host.tnorm) * 0.0
        # для каждого правила вычисляем его альфу
        for rule in self.rules:
            alpha=1.0 # Для t-нормы начальным значением будет 1
            for param, value in rule.ant.iteritems(): # для каждого фактора в правиле
                fact=host[param].get_estim()   # значение фактора
                mem=host[param].classifier[value].value(fact)   # его принадлежность в классификаторе
                alpha=host.tnorm.t_norm(alpha, mem)
##                print rule.name, fact, mem, alpha
            rule.alpha=alpha
            # обрезаем терм собственного классификатора уровнем альфа
            Z=Interval(host.classifier.begin, host.classifier.end)*rule.alpha & host.classifier[rule.concl]
            # и прибавляем его к существующим, используя конорму
            res=res.t_conorm(Z)
        return res

class rules_accurate(rules):
    '''
    Данный алгоритм нечеткого вывода в общем аналогичен контроллеру Мамдани,
    однако, результат определяется как среднне арифметическое взвешенное по
    дефаззифицированным термам заключения каждого правила, причем весами
    являются веса соответствующего правила.
    '''
    rules=[]
    def _calculate(self, host):
        sum_a=0.0
        summ=0.0
        # для каждого правила вычисляем его альфу
        for rule in self.rules:
            alpha=1.0 # Для t-нормы начальным значением будет 1
            for param, value in rule.ant.iteritems(): # для каждого фактора в правиле
                fact=host[param].get_estim()   # значение фактора
                mem=host[param].classifier[value].value(fact)   # его принадлежность в классификаторе
                alpha=host.tnorm.t_norm(alpha, mem)
            rule.alpha=alpha
            sum_a+=alpha
            summ+=host.classifier[rule.concl].centr()*alpha
        if sum_a==0: return 0.0
        return summ/sum_a

class Rule:
    '''
    Описание
    Синтаксис:
        >>>
    '''
    ant={}
    concl=''
    name=''
    alpha=''
    def __init__(self, ant={}, concl='',  name=''):
        self.concl=concl
        self.name=name
        self.ant=ant
    def __str__(self):
        res=str(self.name)+': '
        for (name, value) in self.ant.iteritems():
            res+=str(name)+'='+value+' '
        res+=' -> '+str(self.concl) + '(' + str(self.alpha)+')'
        return res
