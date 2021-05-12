import numpy

arrs = input().strip().split(' ')

if len(arrs) == 4:
    print(numpy.zeros((int(arrs[0]), int(arrs[1]), int(arrs[2]), int(arrs[3])), int))
    print(numpy.ones((int(arrs[0]), int(arrs[1]), int(arrs[2]), int(arrs[3])), int))

elif len(arrs) == 3:
    print(numpy.zeros((int(arrs[0]), int(arrs[1]), int(arrs[2])), int))
    print(numpy.ones((int(arrs[0]), int(arrs[1]), int(arrs[2])), int))
elif len(arrs) == 2:
    print(numpy.zeros((int(arrs[0]), int(arrs[1])), int))
    print(numpy.ones((int(arrs[0]), int(arrs[1])), int))
elif len(arrs) == 1:
    print(numpy.zeros((int(arrs[0])), int))
    print(numpy.ones((int(arrs[0])), int))
