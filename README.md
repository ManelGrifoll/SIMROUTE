# SIMROUTE
SIMROUTE: Weather Ship Routing (WSR) Code.
The software is constructed considering available Copernicus Marine Environment Monitoring Service (CMEMS) wave predictions systems of free use.  
The code provides the ship optimized route and the minimum distance (i.e. geodetic in free land cases) route jointly additional modules to compute
ship emission and safety on navigation monitoring. SIMROUTE has been used in several scientific problems in short and long-distance routes including real routes 
comparison from Automatic Identification System (AIS) data and may be useful also as inter-comparison of more sophisticated WSR methods. 
SIMROUTE is also used for academic purposes providing skills of ship routing optimization, to assess the impact of the meteo-oceanographic 
on ship navigation and to highlight the relevance of ship routing in the framework of standards of training, certification and watchkeeping (STCW) 
competences-based maritime education and training. The code has been tested using Python 3 and the specific imported modules are included in the 
headers of the code. The repository includes the code, an additional .txt files for a fast start and the results of the benchmark case (i.e. params.py).
Other test cases using diferent CMEMS products are also included in the repository. 

Fast start file (and test case): FastStart_CaseTest.txt

Code developer: Manel Grifoll from Barcelona Innovative Transportation (BIT), Universitat Politècnica de Catalunya (UPC-BarcelonaTech), manel.grifoll@upc.edu

Reference: A comprehensive Ship Weather Routing system using CMEMS products and A* algorithm. Grifoll, M., Borén, C., Castells-Sanabra, M. (2022). Ocean Engineering, (255) - 111427. https://doi.org/10.1016/j.oceaneng.2022.111427


Flow chart of SIMROUTE:

![Fluxe](https://user-images.githubusercontent.com/61749362/119992389-c8514380-bfca-11eb-9a13-0cc7a513f1b3.png)

Test case: params_MEDSEA.py
![Figura_total](https://user-images.githubusercontent.com/61749362/119993720-2a5e7880-bfcc-11eb-942f-5c9767178693.png)

