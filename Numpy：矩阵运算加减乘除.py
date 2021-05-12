import numpy

n, m = input().strip().split(' ')
arrs1 = []
arrs2 = []

for i in range(0, int(n)):
    arr = input().strip().split(' ')
    my_array = numpy.array(arr, int)
    arrs1.append(my_array)

for i in range(0, int(n)):
    arr = input().strip().split(' ')
    my_array = numpy.array(arr, int)
    arrs2.append(my_array)

my_arrays1 = numpy.array(arrs1, int)
my_arrays2 = numpy.array(arrs2, int)
print(my_arrays1 + my_arrays2)
print(my_arrays1 - my_arrays2)
print(my_arrays1 * my_arrays2)
print(numpy.array(my_arrays1 / my_arrays2, int))
print(my_arrays1 % my_arrays2)
print(my_arrays1 ** my_arrays2)
