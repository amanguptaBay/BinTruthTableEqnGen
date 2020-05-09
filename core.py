#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas
import collections
import itertools
import copy


def _get_variables_count(tbl):
    return len(tbl.get(tbl.columns[0])[0]),len(tbl.columns[1])

def _get_table_variables(tbl):
    varz = []
    variables_count = _get_variables_count(tbl)
    names = "I","S"
    for ind,name in enumerate(names):
        for ind in range(variables_count[ind],0,-1):
            varz.append(name+str(ind-1))
    return varz

#Given a key or something in array form, it splits it up into the v,h components as expected given the variables
def _split_varz(arr_varz):
    count_vars = _get_variables_count()
    return (arr_varz[0:count_vars[0]],arr_varz[count_vars[0]:count_vars[0]+count_vars[1]+1])
#Given the vertical key, this gives its index in terms of the table
def _v_key_index(v):
    return list(tbl.get(tbl.columns[0])).index(v)

class MintermComponent:
    """
        What this is expected to do
    """
    def __init__(self, variables: [str]], terms:[int]):
        if len(variables) != len(terms):
            raise ValueError("Variables and Terms Arrays Not Of Same Length")
        self._terms = collections.defaultdict(lambda:0)
        self._variables = variables #This is so that outputs are in the same order as the variables inserted
        for ind, var in enumerate(variables):
            if terms[ind] in [1,0,-1]:
                self._terms[var] = terms[ind]
    def __str__(self):
        def lmbda(key):
            coe = self._terms[key]
            if coe == 1:
                return f"{key}"
            elif coe == -1:
                return f"{key}'"
            return ""
        terms = list(map(lambda x: lmbda(x), self._terms))
        terms = list(filter(lambda x: x!="", terms))
        return "&".join(terms)
    def __getitem__(self, v:str):
        return self._terms[v]
    def __setitem__(self, var:str, val:int):
        if val not in [1,0,-1]:
            raise ValueError(f"{this.__name__} cannot have any variable of it set to {value}")
        else:
            self._terms[var] = val
    def __iter__(self):
        for key in self._variables:
            yield key,self[key]
    def __eq__(self, other:MintermComponent):
        return self._terms == other._terms

"""
Iterable, that goes over a truth table pandas dataframe and provides the two types of input (V,H) along with its value
"""
def _values_tbl(tbl):
    InputState = collections.namedtuple("InputState", "Input State")
    #Note: These are both to be used with the table's get operator to get the values of the column in question
    first,cols = tbl.columns[0], tbl.columns[1:]
    for col in cols:
        for index, value in enumerate(tbl.get(col)):
            yield InputState(tbl.get(first)[index],col),value
#Debugging
def print_minterms(tbl):
    for minterm in get_minterms(tbl):
        print(minterm)

def get_minterms(tbl):
    varz = _get_table_variables(tbl)
    for pos, val in _values_tbl(tbl):
        inp, ste = list(map(lambda x:int(x),pos.Input)), list(map(lambda x:int(x),pos.State))
        def BinaryToMinterm(coeff):
            """
                Binary : 1 or 0
                Minterm: 1 or -1
            """
            if coeff == 1:
                return coeff
            else:
                return -1
        if val == "1":
            yield MintermComponent(varz,list(map(BinaryToMinterm,inp+ste)))

def _access_flat_key(key,tbl):
    key = "".join(map(lambda y: str(y),key))
    key = _split_varz(key)
    try:
        return tbl.get(key[1])[_v_key_index(key[0])]
    except NameError:
        #Wrong Column
        return "X"
    except ValueError:
        #Wrong Row
        return "X"
    except TypeError:
        return "X"

def _minterm_valid(minterm, tbl):
    keys = _keys_for_minterm(minterm)
    vals = map(lambda key:_access_flat_key(key,tbl), keys)
    return "0" not in vals


def _keys_for_minterm(minterm):
    """
        Outputs a series of "keys" in flat form that must all be true for the minterm to be true
    """
    #Example of a "possibility" [[1,1,-1,1,1,-1,...],[...],...]
    possibilities = [list()]
    for var,val in minterm:
        if val != 0:
            for i,p in enumerate(possibilities):
                possibilities[i].append(1 if val==1 else 0)
        else:
            nlist = []
            for i,p in enumerate(possibilities):
                nlist.append(possibilities[i]+[1])
                nlist.append(possibilities[i]+[0])
            possibilities = nlist
    return list(possibilities)



def simplify_minterms(minterms:list, tbl):
    varz = _get_table_variables(tbl)
    for variable in varz:
        for minterm in minterms:
            new_minterm = copy.deepcopy(minterm)
            new_minterm[variable] = 0
            if _minterm_valid(new_minterm, tbl):
                minterm[variable] = 0
    cache = []
    for minterm in minterms:
        if minterm not in cache:
            cache.append(minterm)
    return cache
