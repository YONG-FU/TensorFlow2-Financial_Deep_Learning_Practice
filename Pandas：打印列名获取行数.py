#!/bin/python

import math
import os
import random
import re
import sys


#
# Complete the 'get_nb_rows' function below.
#
# The function is expected to return an INTEGER.
#
# print the column name in the debug console
#
# You can access the data with the following commands :
# import pandas as pd
# df = pd.read_csv('dataSampleTest.csv')

def get_nb_rows(file_name):
    # Write your code here
    # Start by loading the needed data
    import pandas as pd
    df = pd.read_csv('dataSampleTest.csv')
    # print column names
    print(list(df))
    # return number of rows in the data frame
    return len(df)


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    file_name = input()

    result = get_nb_rows(file_name)

    fptr.write("{}".format(result))

    fptr.close()
