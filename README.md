# FYP
This is the Final Year Project code repository for the project **shape approximation**.
Candidate: Zixin Qin
Type of study: Theoretical Study

#Developer's notes

2021.1.6
- Is implementing the "find exterior edge"
  - **replace_by_edge** done, rather trival
  - **replace_by_vertex** done, quite hard (2.9)
  - **get_boundary_edges** done,determine whether the edge is exterior
     ~~heart attack, the theory does not work~~(2.27)
     the theory only works when the graph is triangulated.
2021.2.28
 - To be finished
   -  **generate the "ext point set"**, done (2.28)
        - leaving one potential bug 
        - the boundary could not be stored as global variable (better to use pointer or global variable?)
   -  sort the edges
   - find the replace edge
   - experiment


