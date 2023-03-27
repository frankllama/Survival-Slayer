from csv import reader
from os import walk 
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout: 
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []

    for _,__,image_files in walk(path): #the output for print(import_csv_layout('graphics/grass')) is 
                                     # ('graphics/grass', [], ['grass_3.png', 'grass_2.png', 'grass_1.png'])
                                     #so need to include _,__, to disregard the first two output to get to the png files
        for image in image_files:
            full_path = path + '/' + image
            print(full_path)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list    

# import_folder('graphics/grass')
# print(import_csv_layout('map/map_FloorBlocks.csv'))
# import_csv_layout