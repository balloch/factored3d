from scipy.io import loadmat
import numpy as np
import pptk
from mayavi import mlab
import itertools


mat2 = loadmat("../external/suncgdir/scene_voxels/0004d52d1aeeb8ae6de39d6bd993e992/000007_voxels.mat")

print(mat2['camPoseArr'])
original = mat2['camPoseArr'][:, 0:3].T
print(original)
voxSize = tuple(mat2['voxSize'].reshape((3,)))
voxUnit = np.squeeze(mat2['voxUnit'])
print(voxSize)
print(voxUnit)
voxCoords = -1*np.array([voxSize[0]/2*voxUnit, voxSize[1]/2*voxUnit, 0])
grid = np.mgrid[voxCoords[0]:voxCoords[0]+voxSize[0]*voxUnit:voxUnit,
        voxCoords[1]:voxCoords[1]+voxSize[1]*voxUnit:voxUnit,
        voxCoords[2]:voxCoords[2]+voxSize[2]*voxUnit:voxUnit]

mult = np.matmul(original[:, 0:3], grid.reshape((3, -1)))

added = np.add(mult, original[:, 3].reshape((3,1)))
final = added.reshape(grid.shape)
print(final.shape)

data = mat2['sceneVox']

x, y, z = np.where(data == 1)
X = final[0]
Y = final[1]
Z = final[2]

coords = []
for idx, x_val in enumerate(x):
    x_val = x[idx]
    y_val = y[idx]
    z_val = z[idx]
    x_coord = X[x_val][y_val][z_val]
    y_coord = Y[x_val][y_val][z_val]
    z_coord = Z[x_val][y_val][z_val]
    coord = np.array([x_coord, y_coord, z_coord])
    coords.append(coord)
coords = np.array(coords)

mlab.points3d(*tuple(coords.T), color=(0, 1, 1))

for idx, bbox in enumerate(mat2['modelBboxes'][0]):
    new_bbox = []
    bbox = bbox.T
    arr = np.array([x for x in itertools.product(*tuple(bbox.T))])
    mlab.points3d(*tuple(arr.T), color=(np.random.random_sample(),np.random.random_sample(),np.random.random_sample()))

mlab.show()
