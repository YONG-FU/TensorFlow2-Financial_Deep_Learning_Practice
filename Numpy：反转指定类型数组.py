import numpy


def arrays(arr):
    # complete this function
    # use numpy.array
    res = numpy.array(arr, float)
    res = res[::-1]
    return res


arr = input().strip().split(' ')
result = arrays(arr)
print(result)
