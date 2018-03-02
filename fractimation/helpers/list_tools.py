"""
Functions related to List/Array Manipulation

Public Methods :
  * update_indexes_with_value - Change values in an array
  * remove_indexes - Remove indexes from arrays
"""

import numpy

def update_indexes_with_value(array, initial_value, new_value):
    """
    Returns a new copy of array where indexes with initial_value are set to new_value

    Parameters :
      * array - Original array to modify
      * initial_value - Value to change from array
      * new_value - Value to update values to in result
    """
    updated_array = numpy.copy(array)
    updated_array[updated_array == initial_value] = new_value
    return updated_array

def remove_indexes(original_arrays, remaining_indexes):
    """
    Culls indexes from arrays in original_arrays not contained in remaining_indexes

    Parameters :
      * original_arrays - An array of arrays to cull indexes from
      * remaining_indexes - A representation of the indexes to remain in the arrays
    """
    return_array = []
    for array in original_arrays:
        array_subset = array[remaining_indexes]
        return_array.append(array_subset)

    return return_array
