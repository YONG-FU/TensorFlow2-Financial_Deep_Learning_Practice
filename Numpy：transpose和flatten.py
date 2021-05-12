import numpy

n, m = input().strip().split(' ')
arrs = []
for i in range(0, int(n)):
    arr = input().strip().split(' ')
    my_array = numpy.array(arr, int)
    arrs.append(my_array)

my_arrays = numpy.array(arrs)
print(my_arrays.transpose())
print(my_arrays.flatten())
