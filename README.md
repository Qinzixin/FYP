# FYP
This is the Final Year Project code repository for the project **shape approximation**.

Candidate: Zixin Qin

Type of study: Theoretical Study

#Developer's notes

- Implemented Functionalities
  - **replace_by_edge** done, rather trival (2021.1.6)
  - **replace_by_vertex** done, quite hard (2.9), design a test case manually
  - **get_boundary_edges** done,determine whether the edge is exterior
     
     - ~~heart attack, the three transition formula does not work on test case~~
     
     - problem solved: the formula only works when the graph is triangulated. (2.27)
   -  **generate the "ext point set"**, done (2.28)
       -  ~~leaving one potential bug: the boundary could not be stored as global variable (better to use pointer or global variable?)~~
        - use pointer, ideally not contaning global vairable
   -  **sort the edges**, done (2.28)
- Under implementation 
   - find the replace edge
   - experiment


