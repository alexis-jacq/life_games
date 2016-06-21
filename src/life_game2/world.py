import numpy as np
import metabolism
import cell
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as manimation

N = 200 # map size
NB_ATOMS = 3 # red blue green
MAP = np.ones((N,N,NB_ATOMS))*1.5

THETA = 5
ETA = -0.5
POW = 1

center = np.floor(N/2.)

mother = cell.Cell(NB_ATOMS,center,np.floor(center/2.))
father = cell.Cell(NB_ATOMS,np.floor(center/2.),center)

cells = set()
cells.add(mother)
cells.add(father)

def div_rest(x):
    return int(np.floor(x/3.)),int(x%3)

def life():
    global cells
    global MAP

    #food step :
    for cell in cells:
        x = int(cell.i)
        y = int(cell.j)
        if x>0 and x<N-1 and y>0 and y<N-1:
            place = MAP[x-1:x+2,y-1:y+2,:]
            new_place = cell.food(place)
            MAP[x-1:x+2,y-1:y+2,:] = new_place
        else:
            # torus conditions :
            place = np.zeros([3,3,NB_ATOMS])
            xp = 0
            for xi in [x-1, x, (x+1)%N]:
                yp=0
                for yi in [y-1, y, (y+1)%N]:
                    place[xp,yp,:] = MAP[xi,yi,:]
                    yp+=1
                xp+=1

            new_place = cell.food(place)
            xp = 0
            for xi in [x-1, x, (x+1)%N]:
                yp = 0
                for yi in [y-1, y, (y+1)%N]:
                    MAP[xi,yi,:] = new_place[xp,yp,:]
                    yp+=1
                xp+=1
        #MAP[x,y,:] += cell.constitution

    #division/death step:
    for cell in frozenset(cells):

        #print str(cell.i)+" , "+str(cell.j)
        #print cell.energy
        if cell.energy > THETA:
            if np.random.rand() < 0.5**POW:
                cells.add(cell.divide_mutation())
            else:
                cells.add(cell.divide())
        if cell.energy < ETA:
            #MAP[cell.i,cell.j,:] += cell.constitution
            cells.remove(cell)

    # move step:
    for cell in cells:
        x = int(cell.i)
        y = int(cell.j)
        if x>0 and x<N-1 and y>0 and y<N-1:
            place = MAP[x-1:x+2,y-1:y+2,:]
            #print place[:,:,0]
            mv = cell.move(place)
            ii,jj = div_rest(mv)
            cell.i += ii-1
            cell.j += jj-1
        else:
            # torus conditions :
            place = np.zeros([3,3,NB_ATOMS])
            xp = 0
            for xi in [x-1, x, (x+1)%N]:
                yp=0
                for yi in [y-1, y, (y+1)%N]:
                    place[xp,yp,:] = MAP[xi,yi,:]
                    yp+=1
                xp+=1

            mv = cell.move(place)
            #print place[:,:,0]
            ii,jj = div_rest(mv)
            cell.i += ii-1
            cell.j += jj-1
        cell.i = cell.i%N
        cell.j = cell.j%N

fig = plt.figure()
im = plt.imshow(MAP,interpolation='nearest')

def update(*args):
    global cells
    global MAP

    life()

    #im = plt.imshow(population_map,interpolation='nearest', cmap=cmap)
    im = plt.imshow(MAP,interpolation='nearest')
    print len(cells)
    return im,

if __name__=='__main__':

    ani = manimation.FuncAnimation(fig, update, interval=50, blit=True)
    plt.show()
