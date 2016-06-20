import numpy as np

def jump(array):
    noise = (1-2*np.random.rand(np.shape(array)))**3
    return noise - np.abs(noise)*array

class metabolism:
    def __init__(self, nb_atoms):
        self.energy = 1-2*np.random.rand(nb_atoms) # energy from a pixel
        self.constitution = 1-2*np.random.rand(nb_atoms,nb_atoms) # distribution depending on environement ~ DNA
        self.attraction = 1-2*np.random.rand(nb_atoms)
        self.repulsion = 1-2*np.random.rand(nb_atoms)

    def mutate(self):
        self.energy += jump(self.energy)
        self.constitution += jump(self.constitution )
        self.attraction += jump(self.attraction)
        self.repulsion += jump(self.repulsion)
