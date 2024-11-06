#!/usr/bin/env python3
class FuzzySetsDict(dict):

    def print_fuzzy_sets_dict(self):
        for elem in self:
            print("setid:     ", elem)
            self[elem].print_set()


class FuzzySet:
    var = ""  # variable of the fuzzy set (ex.: Age)
    label = ""  # label of the specific fuzzy set (ex.: Young)
    x = []  # list of abscissas, from xmin to xmax, 1 by 1
    y = []  # list of ordinates (float)
    memDegree = 0  # membership degree for the current application

    def print_set(self):
        print("var:       ", self.var)
        print("label:     ", self.label)
        # print("x coord:   ", self.x)
        # print("y coord:   ", self.y)
        print("memDegree: ", self.memDegree)
        print()


class RuleList(list):
    def print_rule_list(self):
        for elem in self:
            elem.print_rule()


class Rule:
    ruleName = ""  # name of the rule (str)
    antecedent = []  # list of setids
    consequent = ""  # just one setid
    strength = 0  # float
    consequentX = []  # output fuzzySet, abscissas
    consequentY = []  # output fuzzySet, ordinates

    def print_rule(self):
        print("ruleName: ", self.ruleName)
        print("IF        ", self.antecedent)
        print("THEN      ", self.consequent)
        print("strength: ", self.strength)
        print()


class Application:
    appId = ""  # application identifier (str)
    data = []  # list of ValVarPair

    def print_application(self):
        print("App ID: ", self.appId)
        for elem in self.data:
            print(elem[0], " is ", elem[1])
        print()
