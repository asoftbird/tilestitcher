import os
import sys
import getopt
from PIL import Image

argv = sys.argv[1:]

options = "i:o:x:y:v"
longoptions = ["help", "in=", "out=", "xsize=", "ysize=", "verbose"]
helptext = [
    "--help or -h: Print this help list.", 
    "--in or -i: Specify file input folder.", 
    "--out or -o: Specify output file location.",
    "--xsize or -x: Specify tile grid size in the X direction.",
    "--ysize or -y: Specify tile grid size in the Y direction.",
    "--verbose or -v: Write debug info to console during operation."
    ]

try:
    opts, args = getopt.getopt(argv, options, longoptions)
    
except:
    print("Couldn't parse arguments; try again.")

# defaults
Image.MAX_IMAGE_PIXELS = 933120000
INPUT_PATH = os.getcwd()+"\\input\\"
OUTPUT_PATH = os.getcwd()+"\\output\\output.png"
GRIDSIZE_X = 0
GRIDSIZE_Y = 0
DEBUGLOG = False

if not opts:
    sys.exit("Not enough arguments! Use --help for help.")

for opt, arg in opts:
    if opt in ['--help']:
        for i in helptext:
            print(i)
        sys.exit()
    elif opt in ['-i', '--in']: # input folder
        INPUT_PATH = arg
    elif opt in ['-o', '--out']: # output file
        OUTPUT_PATH = arg
    elif opt in ['-x', '--xsize']:
        GRIDSIZE_X = int(arg)
    elif opt in ['-y', '--ysize']:
        GRIDSIZE_Y = int(arg)
    elif opt in ['-v', '--verbose']:
        DEBUGLOG = True
    else:
        sys.exit("Not enough arguments! Use --help for help.")

if GRIDSIZE_X == 0 or GRIDSIZE_Y == 0:
    sys.exit("Grid size cannot be 0; use --xsize and --ysize to specify tile grid dimensions.")

input_filenames = []
for file in os.listdir(INPUT_PATH):
    input_filenames.append(file)


def merge_images(filelist, gridsize_x, gridsize_y):
    global resulting_width, resulting_height

    image_objects = [Image.open(INPUT_PATH+filename) for filename in filelist]

    # assuming all images have the same size
    (image_width, image_height) = image_objects[0].size

    resulting_width = image_width * gridsize_x
    resulting_height = image_height * gridsize_y

    image_combined = Image.new('RGB', (resulting_width, resulting_height))

    image_index = 0
    for y_index in range(0, gridsize_y):
        for x_index in range(0, gridsize_x):
            if DEBUGLOG == True:
                print(f"X: {x_index} Y: {y_index}, index: {image_index}, image: {image_objects[x_index]}")
            # using an offset height as PIL has the 0,0 coordinate in the upper left corner instead of bottom left
            image_combined.paste(im=image_objects[image_index], box=(x_index*image_width, resulting_height-(y_index*image_height)-image_height)) 
            image_index += 1

    return image_combined

merged = merge_images(input_filenames, GRIDSIZE_X, GRIDSIZE_Y) 

merged.save(OUTPUT_PATH, compress_level=5)
if os.path.exists(OUTPUT_PATH):
    print(f"Exported image with dimensions {resulting_width}x{resulting_height} ({round(os.stat(OUTPUT_PATH).st_size/1E6,2)}MB) to {OUTPUT_PATH}.")