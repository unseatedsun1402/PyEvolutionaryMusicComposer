import numpy

f = numpy.array([1, 1, 4, 7, 1, 16], dtype=float)

try:
    print(numpy.gradient(f))

except:
    print(Exception("NumpyError"))