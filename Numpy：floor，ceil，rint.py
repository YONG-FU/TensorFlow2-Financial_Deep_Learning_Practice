import numpy

numpy.set_printoptions(sign=' ')
arr = input().strip().split(' ')
my_array = numpy.array(arr, float)

print(numpy.floor(my_array))
print(numpy.ceil(my_array))
print(numpy.rint(my_array))
