import pandas as pd
import collections
import itertools
import copy

tbl = pd.read_csv("tests/Test2.csv",dtype=str)
#Table's first column is the state (not a index)

"Splits and joins a array according to the splits"
class SplitTuple():
    def __init__(self,splits:[int,...]):
        self.splits = splits
    def split(self,arr):
        if len(arr) != sum(self.splits):
            raise ValueError(f"Inputted Array({arr}) is not valid")
        out = []
        for s in self.splits:
            out.append(tuple(arr[:s]))
            arr = arr[s:]
        return tuple(out)
    def merge(self, merged):
        out = []
        for i,size in zip(merged,self.splits):
            if len(i) != size:
                raise ValueError("Could not convert the inputted array into a array, since one of the splits is mis-sized")
            out.extend(i)
        return tuple(out)

def _values_tbl(tbl):
    InputState = collections.namedtuple("InputState", "Input State")
    #Note: These are both to be used with the table's get operator to get the values of the column in question
    first,cols = tbl.columns[0], tbl.columns[1:]
    f=True
    for col in cols:
        for index, value in enumerate(tbl.get(col)):
            yield InputState(tbl.get(first)[index],col),value

def mintermInList(minterm, li):
    for l in li:
        breaked = False
        for idx,_ in enumerate(l):
            if (minterm[idx] in ["0","1"]) and l[idx] in ["0","1"] and (l[idx] != minterm[idx]):
                breaked = True
                break
        if not breaked:
            return True
    return False

def reduceMinterm(minterm, exclusion):
    minterm = list(minterm)
    new_minterm = copy.deepcopy(minterm)
    for index,term in enumerate(minterm):
        if term == "X":
            continue
        test = list(copy.deepcopy(new_minterm))
        test[index] = "X"
        test = tuple(test)
        if not mintermInList(test,exclusion):
            #Accepted
            new_minterm[index] = "X"
    return tuple(new_minterm)

def equationForSingleVariableTable(tbl):
    vals = list(_values_tbl(tbl))
    BinaryTerm = SplitTuple([len(vals[0][0][0]),len(vals[0][0][1])])
    mergeBinaryTerm = lambda t: BinaryTerm.merge(t[0])
    valid = list(map(mergeBinaryTerm,filter(lambda tup: tup[1]=="1",vals)))
    zeroes = list(map(mergeBinaryTerm,filter(lambda tup: tup[1]=="0",vals)))
    valid_reduced = set(map(lambda v:reduceMinterm(v,zeroes),valid))
    return list(map(BinaryTerm.split,valid_reduced))