from scipy.io import loadmat
import numpy as np
from mayavi import mlab
import pptk
import itertools
from computeH import computeH
import cv2

mat2 = loadmat("../external/suncgdir/scene_voxels/0004d52d1aeeb8ae6de39d6bd993e992/000004_voxels.mat")

print(mat2.keys())
print(mat2['modelIds'].shape)
print(mat2['modelBboxes'].shape)
print(mat2['camPoseArr'])
print(mat2['segPts'].shape)
print(mat2.keys())
roombbox = mat2['roomBbox'][0][0]
min_box = roombbox[0].T
max_box = roombbox[1].T


one = np.array([min_box[0], min_box[2], min_box[1]])
two = np.array([min_box[0], min_box[2], max_box[1]])
three = np.array([min_box[0], max_box[2], min_box[1]])
four = np.array([min_box[0], max_box[2], max_box[1]])
five = np.array([max_box[0], min_box[2], min_box[1]])
six = np.array([max_box[0], min_box[2], max_box[1]])
seven = np.array([max_box[0], max_box[2], min_box[1]])
eight = np.array([max_box[0], max_box[2], max_box[1]])

all_box_coords = np.array([one, two, three, four, five, six, seven, eight])
all_box_coords = np.squeeze(all_box_coords, axis=2)

#Assuming sceneVox shape is 128x64x128
corresponding = np.array([[0, 0, 64], [0, 0, 0], [128, 0, 64], [128, 0, 0], [0, 128, 64], [0, 128, 0], [128, 128, 64], [128, 128, 0]]).astype(np.float)

H = computeH(corresponding.T, all_box_coords.T)

new_coords = []
#Add bounding box to vis
for idx, c in enumerate(corresponding):
    c = np.concatenate((c, np.array([1])), axis=0)
    q = np.matmul(H, c.T)
    q/=q[3]
    #new_coords.append(q[0:3])
    new_coords.append(corresponding[idx])
    
#printing points that correspond to eachother
print(corresponding)
print(all_box_coords)

data = mat2['sceneVox'].astype(np.float)
xx, yy, zz = np.where(data == 1)
coords = np.array([xx, yy, zz])


for coord in coords.T:
    coord = np.array([coord[0], coord[2], coord[1]])
    c = np.concatenate((coord, np.array([1])), axis=0)
    q = np.matmul(H, c.T)
    q/=q[3]
    #new_coords.append(q[0:3])
    #print(q[0:3])
    new_coords.append(coord)
new_coords = np.array(new_coords)


mlab.points3d(*tuple(new_coords.T), color=(0, 1, 1))


# The min and max of our bounding box.
min_maxs = np.array([[0,0,64],[128,128,0]])
new_minmaxs = []
for minmax in min_maxs:
    c = np.concatenate((minmax, np.array([1])), axis=0)
    q = np.matmul(H, c.T)
    q/=q[3]
    new_minmaxs.append(q[0:3])
    #new_minmaxs.append(minmax)
new_minmaxs = np.array(new_minmaxs)

# mlab.points3d(*tuple(new_minmaxs.T), color=(1,0,0))

matrix = np.linalg.inv(H)
# Transform all bounding boxes to be within 0,0,0, 128,128,64.
for idx, bbox in enumerate(mat2['modelBboxes'][0]):
    new_bbox = []
    bbox = bbox.T
    new_coords = np.concatenate((new_coords, bbox))
    arr = np.array([x for x in itertools.product(*tuple(bbox.T))]).transpose()

    arr1 = []
    for point in arr.T:
        c = np.concatenate((point, np.array([1])), axis=0)
        #print(point.reshape((4,1)))
        new_point = np.matmul(matrix, c.T)
        new_point/=new_point[3]
        arr1.append(new_point[0:3])
    arr1 = np.array(arr1)
    arr1 = arr1.T
    
    #Uncomment to visualize bboxes (arr1 are the transformed boxes)
    #mlab.points3d(*tuple(arr), color=(np.random.random_sample(),np.random.random_sample(),np.random.random_sample()))
    #mlab.points3d(*tuple(arr1), color=(np.random.random_sample(),np.random.random_sample(),np.random.random_sample()))
#mlab.points3d([20],[20],[20], color=(np.random.random_sample(),np.random.random_sample(),np.random.random_sample()))
#mlab.points3d([0],[0],[0], color=(1,0,0))



#Visualize segpts on mlab
arr1 = []
arr = mat2['segPts'][0][8].T
for point in arr:
    c = np.concatenate((point, np.array([1])), axis=0)
    new_point = np.matmul(matrix, c.T)
    new_point/=new_point[3]
    arr1.append(new_point[0:3])
    #arr1.append(point)

arr1 = np.array(arr1)
arr1 = arr1.T
mlab.points3d(*tuple(arr1), color=(1,0,0))

mlab.show()


#Visualize segpts on their own within pptk
arr1 = []
for i in range(mat2['segPts'][0].shape[0]):
    arr = mat2['segPts'][0][i].T
    for point in arr:
        c = np.concatenate((point, np.array([1])), axis=0)
        new_point = np.matmul(matrix, c.T)
        new_point/=new_point[3]
        #arr1.append(new_point[0:3])
        arr1.append(point)

arr1 = np.array(arr1)
v = pptk.viewer(np.c_[arr1])
colors = np.zeros((arr1.shape))
colors[:, 1:] = 1
v.attributes(colors)
v.set(point_size=0.0005)