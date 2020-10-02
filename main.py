import pandas, numpy
import core

def get_eqn_from_table(csv_file):
    tbl = pandas.read_csv(csv_file, dtype="str")
    return core.equationForSingleVariableTable(tbl)
    
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
    file_csv = input("CSV File Path: ")
    eqn = get_eqn_from_table(file_csv)
    print("Minimized Solution:")
    print(eqn_to_string(eqn))

