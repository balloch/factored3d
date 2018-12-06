'''
Script for perturbing data in the SUNCG dataset.

Defaults perturb with following [default] rules:
 - Perturbation is random 4-DoF (x,y,z,phi (z-axis rotation))
 - Remove all people
 - Perturb only one object per room
 - Apply gravity (i.e. no floating objects)
 - No collisions (no overlapping bounding boxes beyond a certain threshold)
 - No small perturbations

Command line Inputs:
    path/to/house.JSON/file

Output:
    perturbed_xxx_house.json
'''

from __future__ import print_function
import sys
import json
import numpy as np

def check_collision(bbox1, collision_grid): #for if I project objects to ceiling. assumes cannot be under stuff
    if (bbox2['min'][0] < bbox1['min'][0] < bbox2['max'][0]): # || ...
        return True

def cuboid_collision(bbox1, bbox2): #Separating Axis test, https://stackoverflow.com/questions/5009526/overlapping-cubes
    pass
# you want to verify that each face is outside the other face. could do before rotation
# if any faces are outside of their antipotal face, (i.e. separating plane) they dont collide


def find_support_height(new_pose, support_grid): #projects down to support
    pass

def check_real_support(bbox1, support_grid, IoU=.5): #checks if bbox is at least IoU overlapping with support bbox 
    pass

def perturb_json(input_file_name):
    house_dict={}
    with open(input_file_name, 'r') as json_if:
        house_dict = json.load(json_if)
        rooms = {}
        for level in house_dict['levels']:
            rand_pert = np.random.rand(3,)
            # pert_obj = np.random.randint(7,100)
            pert_obj = 59 #television, model Id 228, id 0_59 in room 5 in sample house
            room_count = 0
            object_count = 0
            for node in level['nodes']:
                if node['type'] == 'Room':
                    room_count += 1
                #needs a way yot tell if an object is in a room: has "nodeIndices"
                elif node['type'] == 'Object':
                    if int(node['id'][2:]) is obj_pert:
                        old_min=np.asarray(node['bbox']['min'])
                        old_max=np.asarray(node['bbox']['max'])
                        new_min = np.multiply(rand_pert,old_min)
                        new_max = old_max + (new_min-old_min)
                        node['bbox']['min']=list(new_min)
                        node['bbox']['max']=list(new_max)
                    object_count += 1
            print('number of rooms = ', room_count)
            print('number of objects = ', object_count)

    with open(input_file_name[:-5]+'_pert'+input_file_name[-5:], 'w') as of:
        json.dump(house_dict, of, indent=4)
            

if __name__ == "__main__":
    if len(sys.argv) > 1:
        perturb_json(str(sys.argv[1]))
    else:
        perturb_json("../sample_data/house.json")
