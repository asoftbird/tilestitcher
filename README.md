## Tilestitcher
The tool stitches together many individual tiles to form one single large image.  
This assumes that individual tiles are square. 

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

## Usage

Run the script in commandline using python, ie.  
`python tilestitcher.py -i input/ -o output/output.png -x 5 -y 5 -v`.    

Use --help for general help on its usage.    
If the input or output directories aren't specified, the script assumes that input images are located in `\current-dir\input\` and will write the output to `\current-dir\output\output.png`. 

**Required arguments:**  
--xsize or -x:      Specify tile grid size in the X direction.  
--ysize or -y:      Specify tile grid size in the Y direction.  

**Optional arguments:**  
--help or -h:       Print this help list.  
--verbose or -v:    Write debug info to console during operation.

--in or -i:         Specify file input folder.  
--out or -o:        Specify output file location, including image file extension of your choice.   


