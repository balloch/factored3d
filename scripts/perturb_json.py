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


def perturb_json(input_file_name):
    house_dict={}
    with open(input_file_name, 'r') as json_if:
        house_dict = json.load(json_if)
        for level in house_dict['levels']:
            rand_pert=np.random.rand(3,1)
            obj_pert=np.random.randint(100)
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
                        node['bbox']['min']=new_min
                        node['bbox']['max']=new_max
                    object_count += 1
            print('number of rooms = ', room_count)
            print('number of objects = ', object_count)

    with open(input_file_name[:-5]+'pert'+input_file_name[-5:], 'w') as of:
        json.dump(house_dict, of, indent=4)
            

if __name__ == "__main__":
    if len(sys.argv) > 1:
        perturb_json(str(sys.argv[1]))
    else:
        perturb_json("../sample_data/house.json")
