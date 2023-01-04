import os
import sys
import getopt
import random
from PIL import Image

argv = sys.argv[1:]

options = "i:o:x:y:g:d:rs:v"
longoptions = ["help", "in=", "out=", "xsize=", "ysize=", "size=", "dpi=", "random", "seed=", "verbose"]
helptext = [
    "--help or -h: Print this help list.", 
    "--in or -i: Specify file input folder.", 
    "--out or -o: Specify output file location.",
    "--xsize or -x: Specify tile grid size in the X direction.",
    "--ysize or -y: Specify tile grid size in the Y direction.",
    "--gridsize or -g: Specify tile grid size in X and Y directions."
    "--dpi or -d: Specify output image DPI (does not affect pixel size)."
    "--random or -r: Randomize placement of tiles in grid.",
    "--seed or -s: Random seed.",
    "--verbose or -v: Write debug info to console during operation.",
    "If there are not enough images available to reach the desired grid size,",
    "random tiles will be selected from the set to pad the input image list."
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
DPI = 300
DEBUGLOG = False
RANDOMIZE = False
SEED = random.random()

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
    elif opt in ['-g', '--gridsize']:
        GRIDSIZE_X = int(arg)
        GRIDSIZE_Y = int(arg)
    elif opt in ['-d', '--dpi']:
        DPI = int(arg)
    elif opt in ['-r', '--random']:
        RANDOMIZE = True
    elif opt in ['-s', '--random']:
        SEED = int(arg)
    elif opt in ['-v', '--verbose']:
        DEBUGLOG = True
    else:
        sys.exit("Not enough arguments! Use --help for help.")

if GRIDSIZE_X == 0 or GRIDSIZE_Y == 0:
    sys.exit("Grid size cannot be 0; use --xsize [int] and --ysize [int] or --size [int] to specify tile grid dimensions.")

input_filenames = []
for file in os.listdir(INPUT_PATH):
    input_filenames.append(file)


def pad_image_list(input_list, newsize):
    image_count = len(input_list)
    add_count = newsize - image_count
    statistics_list = []

    for _ in range(0, add_count):
        randint = random.randint(0, image_count-1)
        input_list.append(input_list[randint])
        statistics_list.append(randint)

    print(f"Padded list from {image_count} to {len(input_list)} items.")
    for variant in range(0, image_count):
        count = statistics_list.count(variant)
        print(f"Tile {variant} occured {count} times in list ({round((count/newsize)*100, 1)}% of total)")

    return input_list


def merge_images(filelist, gridsize_x, gridsize_y):
    global resulting_width, resulting_height

    image_objects = [Image.open(INPUT_PATH+filename) for filename in filelist]

    if (gridsize_x * gridsize_y) > len(image_objects):
        print(f"Expected {gridsize_x * gridsize_y} images while {len(image_objects)} were provided!")
        image_objects = pad_image_list(image_objects, (gridsize_x * gridsize_y))

    if RANDOMIZE == True:
        print(f"Randomizing tile order with seed {SEED}.")
        random.seed(SEED)
        random.shuffle(image_objects)

    # assuming all images have the same size
    (image_width, image_height) = image_objects[0].size

    resulting_width = image_width * gridsize_x
    resulting_height = image_height * gridsize_y

    image_combined = Image.new('RGB', (resulting_width, resulting_height))

    image_index = 0
    for y_index in range(0, gridsize_y):
        for x_index in range(0, gridsize_x):
            # using an offset height as PIL has the 0,0 coordinate in the upper left corner instead of bottom left
            image_combined.paste(im=image_objects[image_index], box=(x_index*image_width, resulting_height-(y_index*image_height)-image_height))
            if DEBUGLOG == True:
                print(f"X: {x_index} Y: {y_index}, index: {image_index}, image: {image_objects[x_index]}")
            image_index += 1

    return image_combined

merged = merge_images(input_filenames, GRIDSIZE_X, GRIDSIZE_Y) 
print(f"Exporting tiled image...")
 
merged.save(OUTPUT_PATH, compress_level=5, dpi=(DPI, DPI))
if os.path.exists(OUTPUT_PATH):
    print(f"Exported image with dimensions {resulting_width}x{resulting_height} ({round(os.stat(OUTPUT_PATH).st_size/1E6,2)}MB, {DPI}dpi) to {OUTPUT_PATH}.")