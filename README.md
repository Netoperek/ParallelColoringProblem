# ParallelColoringProblem

##Solving problem acording to PCAM method:

  Problem will be solved using Python MPI.

  ![Alt text](http://s8.postimg.org/tfb81mgep/array.png)


###1) Partitioning
  Domain Decomposition will be used in order to solve the problem. Every process will obtain a square to solve using itterative algorithm.

  ![Alt text](http://s11.postimg.org/egprpeo9r/image.png)

###2) Communication
  Local & Global communication will be used. 

  Communication will occour within nearest neighbours of areas. Parallel computing 
  will occour in all selected square areas.

  Local communication will be used between neighbours which will represent squared areas.

  Global communication will be used in order to notify when an area is computed.

  Global communication will occour in order to send data from squared areas to the root process.

  ![Alt text](http://s22.postimg.org/ws9aoqne9/image.png)
     
###3) Aglomeration
  The area of compution is created by a set of connected areas. It seems like for this problem, the best would be dividing
  the space in one two dimensions for those connected areas and allocate them to particular processes. 
  This will couse two dimensional local communication as well as one dimensional communication of communication between
  other processes (beetwen previously computed connected areas).

###4) Mapping
  The most suitable mapping would be dividing the space of data for number of processes and then allocate following processes
  to areas of data.

##OUTCOMES


  ![Alt text](http://s21.postimg.org/kyl9e3hfr/TPR.png)
