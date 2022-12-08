## Image tiler utility script 

This assumes that individual tiles are square. 
The tool stitches together many individual tiles to form one single large image. 

Files in the input folder are read in a numeric ascending order, so label your files accordingly.   
These are then tiled in the following order: (left to right, bottom to top)

|    	|    	|    	|    	|    	|
|----	|----	|----	|----	|----	|
| 21 	| 22 	| 23 	| 24 	| 25 	|
| 16 	| 17 	| 18 	| 19 	| 20 	|
| 11 	| 12 	| 13 	| 14 	| 15 	|
| 06  	| 07  	| 08  	| 09  	| 10 	|
| 01  	| 02  	| 03  	| 04  	| 05  	|

Grid can be any size you want, I've only tested with square configurations but I'm pretty sure rectangular grids also work.