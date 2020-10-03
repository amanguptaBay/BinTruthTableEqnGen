import pandas, numpy
import core

def get_eqn_from_table(csv_file):
    tbls = pandas.read_csv(csv_file, dtype="str")
    out = []
    for tbl in core.expand_mutivar_table(tbls):
        out.append(core.equationForSingleVariableTable(tbl))
    return out 
def eqn_to_string(eqn):
    vars = ["state","in"]
    dims = len(eqn[0][0]),len(eqn[0][1])
    def varTermsToString(termsForVar,varName):
        out = ""
        for idx,term in enumerate(termsForVar):
            if term == "1":
                out += f"{varName}{idx}"
            elif term == "0":
                out += f"{varName}{idx}'"
        return out
    eqnTerm_to_string = lambda term: varTermsToString(term[0],vars[0]) + varTermsToString(term[1],vars[1])
    arr_mterms = []
    arr_mterms = map(lambda i: eqnTerm_to_string(i),eqn)
    return (" + ".join(arr_mterms))

if __name__ == "__main__":
    print("Provide CSV file to get a equation")
    print("Numbered from left-most bit being 0 and right-most being n-1")
    file_csv = input("CSV File Path: ")
    eqns = get_eqn_from_table(file_csv)
    print("Minimized Solution:")
    for eqn in eqns:
        print(eqn_to_string(eqn))

