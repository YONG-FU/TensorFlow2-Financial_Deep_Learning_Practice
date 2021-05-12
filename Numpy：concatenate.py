import numpy

n, m, p = input().strip().split(' ')
arrs1 = []
arrs2 = []

for i in range(0, int(n)):
    arr = input().strip().split(' ')
    my_array = numpy.array(arr, int)
    arrs1.append(my_array)

for i in range(0, int(m)):
    arr = input().strip().split(' ')
    my_array = numpy.array(arr, int)
    arrs2.append(my_array)

my_arrays1 = numpy.array(arrs1)
my_arrays2 = numpy.array(arrs2)
print(numpy.concatenate((my_arrays1, my_arrays2)))
