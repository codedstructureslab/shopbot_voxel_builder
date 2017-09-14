import numpy as np                       # working with matrixes
import copy                              # working with copies of lists


def seeded(voxMatrix):
    seeded_voxMatrix = copy.deepcopy(voxMatrix)
    seeded_voxMatrix[0][0][0] = 0
    seeded_voxMatrix[0][1][0] = 0
    seeded_voxMatrix[1][0][0] = 0
    seeded_voxMatrix[0][0][1] = 0
    return seeded_voxMatrix
    
    
def seeded7(voxMatrix):
    seeded_voxMatrix = copy.deepcopy(voxMatrix)
    seeded_voxMatrix[0][0][0] = 0
    seeded_voxMatrix[0][1][0] = 0
    seeded_voxMatrix[1][0][0] = 0
    seeded_voxMatrix[0][0][1] = 0
    seeded_voxMatrix[1][0][1] = 0
    seeded_voxMatrix[0][1][1] = 0
    seeded_voxMatrix[1][1][0] = 0
    return seeded_voxMatrix
    

# sample voxel geometries
seed = [[[1, 1],[1, 0]],[[1, 0],[0,0]]]
v2x2x2 = np.ones((2,2,2))    # 3d square 2x2 voxel matrix (z,y,x)
v3x3x3 = np.ones((3,3,3))    # 3d sqaure 3x3 voxel matrix
v4x4x4 = np.ones((4,4,4))    # 3d sqaure 3x3 voxel matrix
v5x5x5 = np.ones((5,5,5))    # 3d sqaure 3x3 voxel matrix
v5x3x2 = np.ones((5,3,2))    # non-square vox structure
v3x3x12 = np.ones((3,3,12))

vWing = np.ones((2,14,5))    # Wing vox structure
vWing[1,:,:] = 0 
vWing[1,:,1] = 1


hollow3x3x3 = copy.deepcopy(v3x3x3)   # 3d sqaure 3x3 voxel matrix
hollow3x3x3[1][1][1] = 0            # add hole
    
v2x2x2_seeded = seeded(v2x2x2)
v3x3x3_seeded = seeded(v3x3x3)

v2x2x2_seeded7 = seeded7(v2x2x2)



