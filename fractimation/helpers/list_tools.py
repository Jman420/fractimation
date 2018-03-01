import numpy

def update_indexes_with_value(array, initialValue, newValue):
    updatedArray = numpy.copy(array)
    updatedArray[updatedArray == initialValue] = newValue
    return updatedArray

def remove_indexes(originalArrays, remainingIndexes):
    returnArray = [ ]
    for array in originalArrays:
        newArray = array[remainingIndexes]
        returnArray.append(newArray)

    return returnArray
