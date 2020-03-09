import numpy as np
import pandas as pd

def output(result):

    '''
    Input : Vector of the predictions and file name

    Output : CSV file generated on Ouput folder

    '''
    filename = input("Enter a filename : ")

    test = pd.read_csv("_database/Input/test.csv", index_col = 0)

    result = pd.DataFrame(data = result, index = test.index, columns = ["SalePrice"])
    result.to_csv("_database/Output/{}.csv".format(filename))

    print("{}.csv was generated".format(filename))
    return 
