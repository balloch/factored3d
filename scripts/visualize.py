import scipy.io
import numpy as np
from mayavi import mlab
import itertools

mat2 = scipy.io.loadmat("000002_voxels.mat")
#print(mat2['gridPtsObjWorlds'][0][0].shape)
print(mat2.keys())
print(mat2['modelIds'].shape)
print(mat2['modelBboxes'].shape)

print(mat2['camPoseArr'].shape)


print(mat2['sceneVox'].shape)
print(mat2.keys())


data = mat2['sceneVox']

#src = mlab.pipeline.scalar_field(data)
#outer = mlab.pipeline.iso_surface(src)
xx, yy, zz = np.where(data == 1)
coords = np.array(np.where(data == 1))/25
print(coords.T)
'''
mlab.points3d(xx/25, yy/25, zz/25,
                     mode="cube",
                     color=(0, 1, 1),
                     scale_factor=1)
'''
#mlab.show()

for idx, bbox in enumerate(mat2['modelBboxes'][0]):
    arr = np.array([x for x in itertools.product(*tuple(bbox))]).transpose()
    print(arr.T)
    #mlab.points3d(*tuple(arr), color=(np.random.random_sample(),np.random.random_sample(),np.random.random_sample()))
    #print(arr.T.shape)
    ones = np.ones((arr.T.shape[0], 1))
    arr = np.concatenate((arr.T, ones), axis=1)
    #print(arr)
    #matrix = mat2['transforms'][0][idx].reshape((4, 4)).T
    #matrix = np.linalg.inv(matrix)
    matrix = mat2['camPoseArr']
    arr1 = []
    for point in arr:
        #print(point.reshape((4,1)))
        new_point = np.matmul(matrix, point.T)
        arr1.append(new_point)
    arr1 = np.array(arr1)[:,0:3]
    arr1 = arr1.T
    print("After")
    print(arr1.T)
    #print(arr)
    #print(bbox)
    mlab.points3d(*tuple(arr1), color=(np.random.random_sample(),np.random.random_sample(),np.random.random_sample()))
#mlab.points3d([20],[20],[20], color=(np.random.random_sample(),np.random.random_sample(),np.random.random_sample()))
#mlab.points3d([0],[0],[0], color=(1,0,0))

#mlab.points3d(*tuple(mat2['objSegPts']), color=(1,0,0))

matrix = mat2['camPoseArr']
arr = mat2['objSegPts']
ones = np.ones((arr.T.shape[0], 1))
arr = np.concatenate((arr.T, ones), axis=1)
arr1 = []
for point in arr:
    new_point = np.matmul(matrix, point.T)
    arr1.append(new_point)
arr1 = np.array(arr1)[:,0:3]
arr1 = arr1.T
mlab.points3d(*tuple(arr1), color=(1,0,0))

#mlab.show()

'''

'''