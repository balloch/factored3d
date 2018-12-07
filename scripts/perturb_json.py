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

if sys.version_info >=(3,0):
    sys.stout.write("Python 2.x recommended, should still work with Python 3.x")


person_modelIds = ['323','324','325','333','346','s__1779','s__1780','s__1781',
                    's__1782','s__1783','s__1784','s__1785','s__1786','s__1787',
                    's__1788','s__1789','s__1957','s__1957','s__1957','s__1957',
                    's__1957','s__1957']

perturbable_modelIds = []

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


'''
Removes unwanted entities and corrects errors in original JSON and rewrites it.
Take note: this does not decrement the node id's as that would mess with the Rooms

Input: SUNCG house JSON file
Return: Error code, 0 for success
'''
def clean_json(input_file_name):
    with open(input_file_name, 'r+') as json_if:
        house_dict = json.load(json_if)
        for_deletion = []
        rooms = []
        for level in house_dict['levels']:
            for idx_n, node in enumerate(level['nodes']):
                if 'nodeIndices' in node:
                    rooms.append(node)
                if node['modelId'] in person_modelIds:
                    for_deletion.append((idx_n,int(node['id'])))
            for node_idx in for_deletion:
                for room in rooms: # TODO: can be much faster with numpy binary mask
                    room['nodeIndices'][:] = [x for x in room['nodeIndices'] if x<1]
                del level['nodes'][node_idx[0]] # UNITTEST: make sure this doesn't delete necessary stuff
            print("Removed %d nodes" %len(for_deletion))
            for_deletion = []
            rooms = []
        json_if.seek(0)
        json.dump(house_dict, json_if, indent=4)
        # json_if.truncate() #do not know if this is necessary

'''
Adds a 4-DoF perturbation to one object per room in a SUNCG house JSON file, checking for
bounding box collisions, and ensuring realistic support

Input: SUNCG house JSON file
Return: JSON file with all perturbations, house_pert.json
'''
def perturb_json(input_file_name):
    house_dict={}
    with open(input_file_name, 'r') as json_if:
        house_dict = json.load(json_if)
        rooms = {}
        for level in house_dict['levels']:
            rand_pert = np.random.rand(3,)
            # pert_obj = np.random.randint(7,100)
            pert_obj = 59 #television, model Id 228, id 0_59 in room 5 in sample house
            room_count = 0 #TEST
            object_count = 0 #TEST
            for node in level['nodes']:
                if node['type'] == 'Room':
                    room_count += 1
                #needs a way yot tell if an object is in a room: has "nodeIndices"
                elif node['type'] == 'Object':
                    if node['modelId'] in person_modelIds:
                        print('person') #TEST
                    if int(node['id'][2:]) is pert_obj:
                        old_min=np.asarray(node['bbox']['min'])
                        old_max=np.asarray(node['bbox']['max'])
                        new_min = np.multiply(rand_pert,old_min)
                        new_max = old_max + (new_min-old_min)
                        node['bbox']['min']=list(new_min)
                        node['bbox']['max']=list(new_max)
                    object_count += 1
            print('number of rooms = ', room_count) #TEST
            print('number of objects = ', object_count) #TEST

    with open(input_file_name[:-5]+'_pert'+input_file_name[-5:], 'w') as json_of:
        json.dump(house_dict, json_of, indent=4)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        clean_json(str(sys.argv[1]))
        perturb_json(str(sys.argv[1]))
    else:
        clean_json("../sample_data/house.json")
        perturb_json("../sample_data/house.json")
