import numpy

PHI = (1 + 5**0.5) / 2.0
def getFibonocciNumber(index):
    if index < 2:
        return index

    return int(round((PHI**index - (1 - PHI)**index) / 5**0.5))

# polynomialExpressionArray is an array in the format of increasing order; 
#   ie. [ 1, 2, 3 ] = c + 2z + 3z**2 ; [ 4, 0, 1, 0, 5 ] = 4c + z**2 + 5z**4
def evaluatePolynomial1D(coefficientArray, zValues, cValues):
    # Calculate Polynomial Constant Expression
    constantCoefficient = coefficientArray[0]
    constantValues = cValues * constantCoefficient
    
    # Calculate Polynomial Exponential Expressions
    exponentAccumulator = numpy.ones(zValues.shape, dtype=zValues.dtype)
    exponentValues = numpy.empty(zValues.shape, dtype=zValues.dtype)
    zValuesNew = numpy.zeros(zValues.shape, dtype=zValues.dtype)
    for exponentCounter in range(1, len(coefficientArray)):
        numpy.multiply(exponentAccumulator, zValues, exponentAccumulator)
        exponentCoefficient = coefficientArray[exponentCounter]

        numpy.multiply(exponentAccumulator, exponentCoefficient, exponentValues)
        numpy.add(zValuesNew, exponentValues, zValuesNew)

    # Add Constant and Exponential Expressions
    zValuesNew = zValuesNew + constantValues

    return zValuesNew

def removeIndexes(originalArrays, remainingIndexes):
    returnArray = [ ]
    for array in originalArrays:
        newArray = array[remainingIndexes]
        returnArray.append(newArray)

    return returnArray