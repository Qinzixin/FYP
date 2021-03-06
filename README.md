   
# FYP
This is the Final Year Project code repository for the project **shape approximation**.

The shape approxiamation problem has wide application in the field of geography, spatial data mining and computing geometry.
The aim of this project is to review, implement and benchmark algorithms for generating
polygons which characterizes the shape of a set of points. This repository provides my implementation
for the chi algorithm.

Candidate: Zixin Qin

Type of study: Theoretical Study
# Running Method

run experiment.py

# Developer's notes


- Implemented Functionalities
  - **replace_by_edge** done, rather trival (2021.1.6)
  - **replace_by_vertex** done, quite hard (2.9), design a test case manually
  - **get_boundary_edges** done,determine whether the edge is exterior 
        - problem solved: the formula only works when the graph is triangulated. (2.27)
   -  **generate the "ext point set"**, done (2.28)
        - use pointer, ideally not contaning global vairable
   -  **sort the edges**, done (2.28)
   -  **reveal** finished (3.1)
   - **remove edge** done, the edge must be sorted in "small-big" order (3.2)
   - **queue** done, the edges need to be stored in queue structure (3.2)
   - **edge_elimination** 
        -  basically able to run over input graph(3.3)
        - ~~However, there may be a bug: regular constraint, it  may eliminate more edges than expected~~(3.3) bug fixed(3.4)
        - ~~single vertex problem~~ solved(3.5)
        - the edge elimination only works for a single round (3.7) 
           - debug method: need to design specific sample input to debug (3.9 completed)
   - **anti_edge** function improved(3.10)
   - **record data size**, running time, analyze efficiency (3.11 done)
   - **design experiment features**
        - **generate_test_set**
        - (3.16) able to output the constructed polygon(CP)
        - (3.16) calculate the maze of the CP
        - (3.17) finish experiment on image "L"
   - (4.9) **Automate the learning process**
   -   **optimize the parameter setting on "L" dataset**(5.1 done)
   -    the code need to be merged to record time consumption and to be more Object-oriented
   -  to process the whole data set?
   -   **construct comparison between 3 algorithm** (5.6 done)
        
- Tips
     - It is important to download python package with "--target" location, then update the imterpretor in pycharm
     - Begin test in small data set.

# Key dates
Showcase：6th week (4.x)
Final: May 10th
