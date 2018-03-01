import numpy

def update_indexes_with_value(array, initial_value, new_value):
    updated_array = numpy.copy(array)
    updated_array[updated_array == initial_value] = new_value
    return updated_array

def remove_indexes(original_arrays, remaining_indexes):
    return_array = [ ]
    for array in original_arrays:
        array_subset = array[remaining_indexes]
        return_array.append(array_subset)

    return return_array
