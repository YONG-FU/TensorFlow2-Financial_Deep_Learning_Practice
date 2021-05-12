import numpy

n, m = input().strip().split(' ')

arrs1 = []

for i in range(0, int(n)):
    arr = input().strip().split(' ')
    my_array = numpy.array(arr, int)
    arrs1.append(my_array)

my_arrays1 = numpy.array(arrs1)
print(numpy.prod(numpy.sum(my_arrays1, axis=0)))
