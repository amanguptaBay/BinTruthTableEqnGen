import pandas, numpy
import core

def get_eqn_from_table(csv_file):
    tbl = pandas.read_csv(csv_file, dtype="str")
    minterm_unreduced = core.get_minterms(tbl)
    return core.simplify_minterms(minterm_unreduced, tbl)
def eqn_to_string(eqn):
    arr_mterms = []
    arr_mterms = map(lambda i: str(i),eqn)
    return ("+ \n".join(arr_mterms))

if __name__ == "__main__":
    print("Provide CSV files to get a equation")
    file_csv = input("CSV File Path: ")
    eqn = get_eqn_from_table(file_csv)
    print("Minimized Solution:")
    print(eqn_to_string(eqn))
