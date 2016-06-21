import numpy as np
import metabolism
import copy

class Cell(object):
    def __init__(self, nb_atoms, i, j, dna=None):
        if dna:
            self.dna = dna
        else:
            self.dna = metabolism.Metabolism(nb_atoms)
        self.i = i
        self.j = j
        self.energy = 0. # -1 => death, +1 => division
        self.constitution = np.zeros(nb_atoms)

    def divide(self):
        self.energy *= 0.
        self.constitution *= 0.
        return copy.deepcopy(self)

    def divide_mutation(self):
        son = self.divide()
        son.dna.mutate()
        return son

    def food(self,place):
        for i in range(np.shape(place)[0]):
            for j in range(np.shape(place)[1]):
                #print "##############"
                #print place[i,j]
                #print self.dna.constitution
                u = np.dot(self.dna.constitution, place[i,j])
                u = u*np.sum(place[i,j])/np.sum(u)
                #print u
                self.constitution += u/10.
                place[i,j] -= u/10.
                place[i,j,place[i,j]<0]=0
        self.energy = np.dot(self.dna.energy, self.constitution)-0.1
        #print self.energy
        return place

    def move(self,moves):
        values = []
        for i in range(np.shape(moves)[0]):
            for j in range(np.shape(moves)[1]):
                values.append(np.dot(self.dna.attraction, moves[i,j])+np.random.rand()/10000.)
        return np.argmax(values)
