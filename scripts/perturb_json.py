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


person_modelIds =  ['323','324','325','333','346','s__1779','s__1780','s__1781',
                    's__1782','s__1783','s__1784','s__1785','s__1786','s__1787',
                    's__1788','s__1789','s__1957','s__1957','s__1957','s__1957',
                    's__1957','s__1957']

# Floor='Floor', box(unkown)='Box', and the rest are real objects. List onlu through 600
# important obj: table,stand,shelf,dresser,bed,desk,ottoman,rug
# TODO should probably make "region of support" annotations for objects (e.g. chair, sofa,bookshelf)
support_modelIds = ['40','41','75','77','78','104','105','107','108','109',
                    '115','116','117','119','128','129','134','140','141','146',
                    '147','153','171','172','173','174','188','192','193','195',
                    '197','198','199','200','201','202','203','204','205','207',
                    '233','235','238','252','268','270','293','294','311','312',
                    '315','318','390','396','397','398','403','404','404','417',
                    '424','428','430','431','440','451','452','454','455','456',
                    '457','458','459','464','468','469','470','472','473','474',
                    '477','478','480','483','484','485','486','487','488','489',
                    '490','492','493','494','495','504','505','506','508','509',
                    '513','514','525','533','534','541','542','543','544','545',
                    '546','547','548','549','550','551','552','553','554','555',
                    '556','557','558','559','560','561','563','564','565','566',
                    '567','568','569','570','577','579','580','586','587','589',
                    '590','591','592']

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

'''
Checks if bbox is at least IoU overlapping with support bbox and if bbox of support smaller than obj
'''
def check_real_support(bbox1, support_grid, IoU=.25):
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
                for room in rooms: # TODO: can be maybe faster with numpy binary mask
                    room['nodeIndices'][:] = [x for x in room['nodeIndices'] if x==node_idx[1]]
                del level['nodes'][node_idx[0]] # UNITTEST: make sure this doesn't delete necessary stuff like rooms
            print("Removed %d nodes" %len(for_deletion))
            for_deletion = []
            rooms = []
            #TODO order all rooms to show up first
        json_if.seek(0)
        json.dump(house_dict, json_if, indent=4)
        # json_if.truncate() #do not know if this is necessary

'''
Adds a 4-DoF perturbation to one object per room in a SUNCG house JSON file, checking for
bounding box collisions, and ensuring realistic support. Y-up

Input: SUNCG house JSON file
Return: JSON file with all perturbations, house_pert.json
'''
def perturb_json(input_file_name):
    house_dict={}
    with open(input_file_name, 'r') as json_if:
        house_dict = json.load(json_if)
        for level in house_dict['levels']:
            #thought about doing this with polygons, too hard, see https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
            # rand_pert = np.random.rand(3,)
            pert_obj = 59 #television, model Id 228, id 0_59 in room 5 in sample house
            room_count = 0 #TEST
            object_count = 0 #TEST
            for node in level['nodes']:
                rooms = [] # TODO i think there is a bug here
                if 'nodeIndices' in node:  #node['type'] == 'Room': #room is more correct, but we don't care about rooms that don't have 'nodeIndices'
                    grid_shape = np.ceil((np.asarray(node['bbox']['max'])-np.asarray(node['bbox']['min']))[0::2]*100).astype(int)
                    rooms.append({'data':node, 'grid':np.empty(shape=grid_shape)})
                elif node['type'] == 'Object':
                    # wrongly assume you see all of the rooms first. add to clean_json?
                    for room in rooms:
                        # Add grid collision, then support. this does not account for "good" support
                        if int(node['id'][2:]) in room['data']['nodeIndices']: #this may need to be a string compare not an int compare
                            obj_grid_ind_mins = np.floor((np.asarray(node['bbox']['min'])-np.asarray(room['data']['bbox']['min']))[0::2]*100).astype(int)
                            obj_grid_ind_maxs = np.ceil((np.asarray(node['bbox']['max'])-np.asarray(room['data']['bbox']['min']))[0::2]*100).astype(int)
                            obj_grid_ind_slice = [slice(obj_grid_ind_mins[0],obj_grid_ind_maxs[0]),slice(obj_grid_ind_mins[1],obj_grid_ind_maxs[1])]
                            if node['modelId'] in support_modelIds:
                                room['grid'][obj_grid_ind_slice][ node['bbox']['max'][1] > np.abs(room['grid'][obj_grid_ind_slice]) ] = node['bbox']['max'][1]
                            else:
                                room['grid'][obj_grid_ind_slice][ node['bbox']['max'][1] > np.abs(room['grid'][obj_grid_ind_slice]) ] = -1*node['bbox']['max'][1]
                            if int(node['id'][2:]) is pert_obj:
                                old_min=np.asarray(node['bbox']['min'])
                                old_max=np.asarray(node['bbox']['max'])
                                #rand_pert=np.random.rand(3,) #TODO should do this with quaternions?
                                yaw = np.random.rand(1) # y (yaw) angle 
                                transl = np.random.rand(3)


                        
                        
                        new_min = np.multiply(rand_pert,old_min)
                        new_max = old_max + (new_min-old_min)
                        node['bbox']['min']=list(new_min)
                        node['bbox']['max']=list(new_max)
                    object_count += 1
            print('number of rooms = ', len(rooms)) #TEST
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
