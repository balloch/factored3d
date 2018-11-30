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

import sys
import json

person_modelIds = ['323','324','325','333','346','s__1779','s__1780','s__1781',
                    's__1782','s__1783','s__1784','s__1785','s__1786','s__1787',
                    's__1788','s__1789','s__1957','s__1957','s__1957','s__1957',
                    's__1957','s__1957']

def perturb_json(input_file):
    with open(input_file, 'r') as json_f:
        house_dict = json.load(json_f)
        for level in house_dict['levels']:
            room_count = 0
            object_count = 0
            for node in level['nodes']:
                if node['type'] == 'Room':
                    room_count += 1
                elif node['type'] == 'Object':
                    if object_count == 0:
                        print(type(node['modelId']))
                    if node['modelId'] in person_modelIds:
                        print('person')
                        continue
                    object_count += 1
            print('number of rooms = ', room_count)
            print('number of objects = ', object_count)


            

if __name__ == "__main__":
    perturb_json(str(sys.argv[1]))