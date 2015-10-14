# ParallelColoringProblem

##Solving problem acording to PCAM method:

  ![Alt text](http://s8.postimg.org/tfb81mgep/array.png)

###1) Partitioning
  Domain Decomposition will be used in order to solve the problem. Elementary processing unit would be one element of given array (fine grained).

  ![Alt text](http://s12.postimg.org/mf11v7o9l/single_cell.png)

###2) Communication
  Local & Global communication will be used. 

  Communication will occour within nearest neighbours of given array cell. Parallel computing 
  will occour in all contected areas (between every two exists a path of cells adjecnt sides). 

  Local communication will be used between neighbours in order to count the minimum values and propagate them.

  Global communication will be used in order to notify when an area is computed.


  Local communiaction would occour between cells in areas as marked below.

  ![Alt text](http://s23.postimg.org/b6tiuhhtj/array_Copy.png)
     
###3) Aglomeration
  The area of cumpition is created by a set of connected areas. It seems like for this problem, the best would be dividing
  the space in one two dimensions for those connected areas and allocate them to particular processes. 
  This will couse two dimensional local communication as well as one dimensional communication of communication between
  other processes (beetwen previously computed connected areas).

###4) Mapping
  The most suitable mapping would be dividing the space of data for number of processes and then allocate following processes
  to areas of data.
