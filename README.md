# ParallelColoringProblem

##Solving problem acording to PCAM method:

###1) Partitioning
  Domain Decomposition will be used in order to solve the problem. Elementary processing unit would be one element of given array. 

###2) Communication
  Local communication will be used. Communication will occour within nearest neighbours of given array cell. Parallel computing 
  will occour in all contected areas (between every two exists a path of cells adjecnt sides). 
     
###3) Aglomeration
  The area of cumpition is created by a set of connected areas. It seems like for this problem, the best would be dividing
  the space in one two dimensions for those connected areas and allocate them to particular processes. 
  This will couse two dimensional local communication as well as one dimensional communication of communication between
  other processes (beetwen previously computed connected areas).

###4) Mapping
  The most suitable mapping would be dividing the space of data for number of processes and then allocate following processes
  next areas of data.
