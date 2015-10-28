import numpy as np
import random
import string
import math
from mpi4py import MPI

# define globals
#
STREET_LETTERS_SIZE = 9
STREET_NUMBER_RANGE = 9
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
MAX = 10000000
LIMIT = 100

# define MPI
#
comm = MPI.COMM_WORLD
cw_size = comm.Get_size()
cw_rank = comm.Get_rank()
dims = MPI.Compute_dims(cw_size, 2)

def randomized_array(size):
    return [[random.randrange(0, 2) for _ in range(0, size)] for _ in range (0, size)]

def pretty_print_2d_array(array):
    print ""
    for i in range(len(array)):
        for j in range(len(array)):
            print ("%5d") %(array[i][j]) ,
        print ""
    print ""

def array_min(array):
    min = MAX
    for ele in array:
        if(ele < min and ele != 0):
            min = ele

    return min

def iterative_solve(south_border, north_border, east_border, west_border):
    changed = True
    while(changed):
        changed = False
        for i in range(west_border, east_border):
            for j in range(north_border, south_border):
                north_value = MAX
                south_value = MAX
                east_value = MAX
                west_value = MAX

                if (north_border != 0 and areas_array[i-1][j] != 0):
                    north_value = values_array[i-1][j]
                if (south_border != len(values_array) and areas_array[i+1][j] != 0):
                    south_value = values_array[i+1][j]
                if (east_border != 0 and areas_array[i][j+1] != 0):
                    east_value = values_array[i][j+1]
                if (west_border != len(values_array) and areas_array[i][j-1] != 0):
                    west_value = values_array[i][j-1]

                new_min = array_min([north_value, south_value, east_value, west_value])
                if (values_array[i][j] != new_min):
                    values_array[i][j] = new_min
                    changed = True
# Execution
#
if(comm.Get_rank() == 0): 
    size = int(math.sqrt(cw_size))
    areas_array = randomized_array(size)
    addresses_array = [[int(MAX * random.random()) for i in range(size)] for j in range(size)]
    pretty_print_2d_array(areas_array)
    pretty_print_2d_array(addresses_array)
    data = { 'addresses' : addresses_array,
             'areas' : areas_array }
else:
    data = None
    
data = comm.bcast(data, root=0)
addresses_array = data['addresses']    
areas_array = data['areas']    

comm_2d = comm.Create_cart(dims, [True, True], True)
my_rank = comm_2d.Get_rank()
my_coords = comm_2d.Get_coords(my_rank)

coloured = areas_array[my_coords[0]][my_coords[1]] 

neigh = [0,0,0,0]
neigh[NORTH], neigh[SOUTH] = comm_2d.Shift(0, 1)
neigh[WEST], neigh[EAST] = comm_2d.Shift(1, 1)

for x in range(0, LIMIT):
    if(x == 0):
        my_value = addresses_array[my_coords[0]][my_coords[1]]
        changed = 0 
    if(not areas_array[my_coords[0]][my_coords[1]]):
        my_value = MAX        
        changed = 1 

    # Sending data betweend neighbours
    #
    comm_2d.send(my_value, dest=neigh[NORTH])
    comm_2d.send(my_value, dest=neigh[SOUTH])
    comm_2d.send(my_value, dest=neigh[EAST])
    comm_2d.send(my_value, dest=neigh[WEST])

    north_value = comm_2d.recv(source=neigh[NORTH])
    south_value = comm_2d.recv(source=neigh[SOUTH])
    east_value = comm_2d.recv(source=neigh[EAST])
    west_value = comm_2d.recv(source=neigh[WEST])

    # Border watchguards
    #
    size = int(math.sqrt(cw_size))
    if(my_coords[0] == 0):
        north_value = MAX
    if(my_coords[0] == size - 1):
        south_value = MAX
    if(my_coords[1] == 0):
        west_value = MAX
    if(my_coords[1] == size - 1):
        east_value = MAX

    my_new_value = array_min(
        [north_value,
        south_value,
        east_value,
        west_value,
        my_value])

    comm.Barrier()
    if(my_value != my_new_value and (areas_array[my_coords[0]][my_coords[1]] != 0)):
        changed = 0
    else:
        changed = 1

    my_value = my_new_value
    result = comm.allreduce(changed, MPI.SUM)
    if(result == cw_size):
        if(areas_array[my_coords[0]][my_coords[1]]):
            print ("[%2d] %d") %(my_rank, my_value)
        break
