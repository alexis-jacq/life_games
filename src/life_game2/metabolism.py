import numpy as np

def jump1(array):
    biarray = 1.-2*array
    noise = 1.-2*np.random.rand(array.size)**3
    noise = noise.reshape(np.shape(biarray))
    biarray += noise - np.abs(noise)*biarray
    return (biarray - 1.)/2.

def jump2(array):
    noise = 1.-2*np.random.rand(array.size)**3
    noise = noise.reshape(np.shape(array))
    array += noise - np.abs(noise)*array
    return array

class Metabolism(object):
    def __init__(self, nb_atoms):
        self.energy = np.random.rand(nb_atoms) # energy from a pixel
        self.constitution = np.random.rand(nb_atoms,nb_atoms) # distribution depending on environement ~ DNA
        self.attraction = 1-2*np.random.rand(nb_atoms)

    def mutate(self):
        self.energy = jump1(self.energy)
        self.constitution = jump1(self.constitution )
        self.attraction = jump2(self.attraction)
