#!/usr/bin/env python3
import numpy as np
import skfuzzy as skf
import matplotlib.pyplot as plt
from MFIS_Classes import *
from skfuzzy import control as ctrl


def read_fuzzy_sets_file(fle_name):
    """
    This function reads a file containing fuzzy set descriptions
    and returns a dictionary with all of them
    """
    fuzzy_sets_dict = FuzzySetsDict()  # dictionary to be returned
    input_file = open(fle_name, 'r')
    line = input_file.readline()
    while line != '':
        fuzzy_set = FuzzySet()  # just one fuzzy set
        elements_list = line.split(', ')
        set_id = elements_list[0]
        var_label = set_id.split('=')
        fuzzy_set.var = var_label[0]
        fuzzy_set.label = var_label[1]

        x_min = int(elements_list[1])
        x_max = int(elements_list[2]) + 1
        a = int(elements_list[3])
        b = int(elements_list[4])
        c = int(elements_list[5])
        d = int(elements_list[6])
        x = np.arange(x_min, x_max, 1)
        y = skf.trapmf(x, [a, b, c, d])
        fuzzy_set.x = x
        fuzzy_set.y = y
        fuzzy_sets_dict.update({set_id: fuzzy_set})

        line = input_file.readline()
    input_file.close()
    return fuzzy_sets_dict


def read_rules_file():
    input_file = open('Files/Rules.txt', 'r')
    rules = RuleList()
    line = input_file.readline()
    while line != '':
        rule = Rule()
        line = line.rstrip()
        elements_list = line.split(', ')
        rule.ruleName = elements_list[0]
        rule.consequent = elements_list[1]
        lhs = []
        for i in range(2, len(elements_list), 1):
            lhs.append(elements_list[i])
        rule.antecedent = lhs
        rules.append(rule)
        line = input_file.readline()
    input_file.close()
    return rules


def read_applications_file():
    input_file = open('Files/Applications.txt', 'r')
    application_list = []
    line = input_file.readline()
    while line != '':
        elements_list = line.split(', ')
        app = Application()
        app.appId = elements_list[0]
        app.data = []
        for i in range(1, len(elements_list), 2):
            app.data.append([elements_list[i], int(elements_list[i + 1])])
        application_list.append(app)
        line = input_file.readline()
    input_file.close()
    return application_list

