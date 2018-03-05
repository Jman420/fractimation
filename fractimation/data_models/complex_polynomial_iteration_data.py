class ComplexPolynomialIterationData(object):

    iteration_values = None
    exploded_indexes = None
    remaining_indexes = None

    def __init__(self, iteration_values, exploded_indexes, remaining_indexes):
        self.iteration_values = iteration_values
        self.exploded_indexes = exploded_indexes
        self.remaining_indexes = remaining_indexes

    def get_iteration_values(self):
        return self.iteration_values

    def get_exploded_indexes(self):
        return self.exploded_indexes

    def get_remaining_indexes(self):
        return self.remaining_indexes
