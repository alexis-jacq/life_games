import numpy as np
import metabolism

class cell(object):
    def __init__(self, dna=None):
        if dna:
            self.dna = dna
        else:
            self.dna = metabolism()
        self.energy = 1.

    def divide(self):
        return copy.deepcopy(self)

    def divide_mutation(self):
        son = self.divide()
        son.dna.mutate()
        return son
