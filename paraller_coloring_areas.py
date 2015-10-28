import numpy as np
import random
import string
import math
from mpi4py import MPI

# define globals
#
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
MAX = 10000000
SIZE = 1024
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
            print ("%8d") %(array[i][j]) ,
        print ""
    print ""

def array_min(array):
    min = MAX
    for ele in array:
        if(ele < min and ele != 0):
            min = ele

    return min

def iterative_solve(south_border, north_border, east_border, west_border, parallel_array):
    changed = True
    outcome_min = MAX
    if parallel_array:
        outcome = [[0 for i in range(0, size)] for j in range(0, size)]
    else:
        outcome = [[0 for i in range(SIZE)] for j in range(SIZE)]

    while(changed):
        k = -1 
        changed = False
        for i in range(north_border, south_border + 1):
            k = k + 1
            l = -1
            for j in range(west_border, east_border + 1):
                l = l + 1        
                if(areas_array[i][j] != 0):
                    north_value = MAX
                    south_value = MAX
                    east_value = MAX
                    west_value = MAX

                    if (i != north_border and areas_array[i-1][j] != 0):
                        north_value = values_array[i-1][j]
                    if (i != south_border and areas_array[i+1][j] != 0):
                        south_value = values_array[i+1][j]
                    if (j != east_border and areas_array[i][j+1] != 0):
                        east_value = values_array[i][j+1]
                    if (j != west_border and areas_array[i][j-1] != 0):
                        west_value = values_array[i][j-1]

                    new_min = array_min([values_array[i][j], north_value, south_value, east_value, west_value])
                    if parallel_array:
                        outcome[k][l] = new_min
                    else:
                        outcome[i][j] = new_min
                        
                    if (values_array[i][j] != new_min):
                        values_array[i][j] = new_min
                        changed = True

    #pretty_print_2d_array(outcome)
    return outcome

# Execution
#
start_time = MPI.Wtime()
                        

if(comm.Get_rank() == 0): 
    areas_array = randomized_array(SIZE)
    values_array = [[int(MAX * random.random()) for i in range(SIZE)] for j in range(SIZE)]
    #print "AREAS INITIAL ARRAY"
    #pretty_print_2d_array(areas_array)
    #print "VALUES INITIAL ARRAY"
    #pretty_print_2d_array(values_array)
    data = { 'addresses' : values_array,
             'areas' : areas_array }

else:
    data = None

data = comm.bcast(data, root=0)
values_array = data['addresses']    
areas_array = data['areas']    

comm_2d = comm.Create_cart(dims, [True, True], True)
my_rank = comm_2d.Get_rank()
my_coords = comm_2d.Get_coords(my_rank)

neigh = [0,0,0,0]
neigh[NORTH], neigh[SOUTH] = comm_2d.Shift(0, 1)
neigh[WEST], neigh[EAST] = comm_2d.Shift(1, 1)
    
# Mapping processes
#
size = int(math.sqrt((SIZE * SIZE) / cw_size))
north_border = int(my_coords[0] * size)
south_border = int(my_coords[0] * size + size - 1)
west_border = int(my_coords[1] * size)
east_border = int(my_coords[1] * size + size - 1)

# Solving for each process
#
outcome = iterative_solve(south_border, north_border, east_border, west_border, True)

# Gathering data to root
#
data = comm.gather(outcome, root=0)
if(my_rank == 0):
    for rank in range(cw_size):
        # pretty_print_2d_array(data[rank])
        outcome = data[rank]
        coords = comm_2d.Get_coords(rank)
        north_border = int(coords[0] * size)
        south_border = int(coords[0] * size + size - 1)
        west_border = int(coords[1] * size)
        east_border = int(coords[1] * size + size - 1)
        k = -1 
        for i in range(north_border, south_border + 1):
            l = -1
            k = k + 1
            for j in range(west_border, east_border + 1):
                l = l + 1
                values_array[i][j] = outcome[k][l]

    # Solving as whole
    #
    iterative_solve(len(values_array)-1, 0, len(values_array)-1, 0, False)
    end_time = MPI.Wtime()  
    print 'SOLUTION FOUND IN TIME: ', end_time - start_time
    #pretty_print_2d_array(values_array)
