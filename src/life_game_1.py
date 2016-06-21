import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as manimation

"""FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib', comment='growing cells')
writer = FFMpegWriter(fps=15, metadata=metadata)"""

# cell action : operation matriciel 9 cases qui l'entourent
# cell a besoin d'un seuil d'nergie suffisent pour survivre
# cell peut se reproduire si elle-meme + case voisine assez energie

# cell matrix norm = 1

# word = 2 matrix : map of energy + map of cells

cmap = mpl.colors.ListedColormap(['white','green','yellow'])

N = 200
# rand map
energy = np.random.rand(N,N)

# create islands
energy[energy<0.5] /= 10
energy = (2*energy)**3

# uniform map
energy = np.ones([N,N])

class Cell:
    def __init__(self,kind):# add weigth for action and matrix for cell_division
        if kind==0:
            self.kind = 0
            #self.matrix = np.random.rand(3,3)
            #self.matrix = np.array([[1,2,3],[1,1,1],[3,2,1]])
            #self.matrix = self.matrix/np.sum(self.matrix)

            """
            self.matrix = np.array([[3,3,3],[3,0,3],[3,3,3]])
            self.matrix = np.random.rand(3,3)*self.matrix
            self.matrix = self.matrix/np.sum(self.matrix)"""

            self.matrix = np.array([[1.,3.,4.],[1.,2.,3.],[1.,1.,2.]])
            self.matrix = self.matrix/np.sum(self.matrix)

            self.weight = np.array([[1,1,1],[1,3,1],[1,1,1]])/10.
            #np.random.shuffle(self.weight)
            #self.weight = np.random.rand(3,3)
            #self.weight = 0.3*(self.weight/np.max(self.weight))

        if kind==1:
            self.kind = 1
            self.matrix = np.array([[1.,3.,4.],[1.,2.,3.],[1.,1.,2.]]).T
            self.matrix = self.matrix/np.sum(self.matrix)
            self.weight = np.array([[1,1,1],[1,3,1],[1,1,1]])/10.

cells = {}
cell_map = np.zeros([N,N])
kind_map = [np.zeros([N,N]),np.zeros([N,N])]
population_map = np.zeros([N,N])

"""
cells[(N/2,N/2)] = Cell()
cell_map[N/2,N/2]=1
"""
cells[(N/3,N/3)] = Cell(0)
cells[(2*N/3,2*N/3)] = Cell(1)

population_map[(N/3,N/3)]= 1
population_map[(2*N/3,2*N/3)] = 2

def action():
    global energy
    global cells
    global kind_map
    for pos in cells:
        x = pos[0]
        y = pos[1]
        cell = cells[pos]
        kind = cell.kind
        if x>0 and x<N-1 and y>0 and y<N-1:
            place = energy[x-1:x+2,y-1:y+2]
            #weight = np.array([[1,1,1],[1,3,1],[1,1,1]])/10. # or the weight can depend on the cell
            win = np.sum(cell.weight*place)
            energy[x-1:x+2,y-1:y+2] = cell.matrix*win + place-cell.weight*place
            kind_map[kind][x-1:x+2,y-1:y+2] = energy[x-1:x+2,y-1:y+2]
        else:
            # torus conditions :
            place = np.zeros([3,3])
            xp = 0
            for xi in [x-1, x, (x+1)%N]:
                yp=0
                for yi in [y-1, y, (y+1)%N]:
                    place[xp,yp] = energy[xi,yi]
                    yp+=1
                xp+=1
            win = np.sum(cell.weight*place)
            xp = 0
            for xi in [x-1, x, (x+1)%N]:
                yp = 0
                for yi in [y-1, y, (y+1)%N]:
                    energy[xi,yi] = cell.matrix[xp,yp]*win + place[xp,yp]-cell.weight[xp,yp]*place[xp,yp]
                    kind_map[kind][xi,yi] = energy[xi,yi]
                    yp+=1
                xp+=1


def life():
    global energy
    global cells
    global cell_map
    global population_map
    for x in range(N):
        for y in range(N):
            if energy[x,y]>1.5 and cell_map[x,y]<1:
                cell_map[x,y]=1
                kind = 0
                if kind_map[1][x,y]>kind_map[0][x,y]:
                    kind = 1
                cells[(x,y)] = Cell(kind)
                population_map[x,y] = kind+1
            if cell_map[x,y]>0 and energy[x,y]<0.5:
                _=cells.pop((x,y))
                cell_map[x,y]=0
                population_map[x,y] = 0

fig = plt.figure()
#plt.subplot(211)
#im = plt.imshow(population_map,interpolation='nearest', cmap=cmap)
#plt.subplot(212)
im = plt.imshow(energy[1:-1,1:-1],interpolation='nearest')

def update(*args):
    global energy
    global cells
    global cell_map
    global kind_map
    global population_map
    global im
    action()
    life()
    #im = plt.imshow(population_map,interpolation='nearest', cmap=cmap)
    im = plt.imshow(energy[1:-1,1:-1],interpolation='nearest')
    print 'max : %s, min : %s, num cells : %s' %(np.max(energy[1:-1,1:-1]), np.min(energy[1:-1,1:-1]), len(cells))
    return im,


if __name__=='__main__':

    """
    action()
    life()
    #plt.figure(1)
    #img = plt.imshow(cell_map, interpolation='nearest', cmap = cmap)
    #plt.show()
    with writer.saving(fig, "writer_test.mp4", 100):
        for i in range(100):
            action()
            life()
            img = plt.imshow(cell_map, interpolation='nearest',cmap = cmap)
            writer.grab_frame()
    #plt.figure(2)
    #img = plt.imshow(cell_map, interpolation='nearest', cmap = cmap)
    #plt.show()
    #plt.figure(3)
    #img = plt.imshow(energy, interpolation='nearest')
    #plt.show()
    """
    ani = manimation.FuncAnimation(fig, update, interval=50, blit=True)
    plt.show()



    

