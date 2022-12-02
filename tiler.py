import os
from PIL import Image

# config
INPUTDIR = os.getcwd()+"\\input\\"
OUTPUTDIR = os.getcwd()+"\\output\\"

# this can be detected automatically based on highest tile number in input coordinates
GRIDSIZE_X = 8
GRIDSIZE_Y = 8 
Image.MAX_IMAGE_PIXELS = 933120000

#TODO: parse arguments for commandline operation

input_filenames = []
for file in os.listdir(INPUTDIR):
    input_filenames.append(file)

print(input_filenames)

def merge_images(filelist, gridsize_x, gridsize_y):
    image_objects = [Image.open(INPUTDIR+filename) for filename in filelist]

    # assuming all images have the same size
    (image_width, image_height) = image_objects[0].size

    resulting_width = image_width * gridsize_x
    resulting_height = image_height * gridsize_y

    image_combined = Image.new('RGB', (resulting_width, resulting_height))

    image_index = 0
    for Y_index in range(0, gridsize_y):
        for X_index in range(0, gridsize_x):
            print(f"X: {X_index} Y: {Y_index}, index: {image_index}, image: {image_objects[X_index]}")
            # using an offset height as PIL has the 0,0 coordinate in the upper left corner instead of bottom left
            image_combined.paste(im=image_objects[image_index], box=(X_index*image_width, resulting_height-(Y_index*image_height)-image_height)) 
            image_index += 1

    return image_combined

merged = merge_images(input_filenames, GRIDSIZE_X, GRIDSIZE_Y) 

merged.save(OUTPUTDIR+"TEST.png")