import matplotlib
import numpy as np
np.set_printoptions(suppress=True)

def computeH(t1, t2):
    assert t1.shape == t2.shape
    points1 = t1.transpose()
    points2 = t2.transpose()
    L = []
    for i in range(len(points1)):
        pi = np.append(points1[i], [1])
        mi = pi * -1 * points2[i][0]
        first = np.concatenate((pi, [0,0,0,0], [0,0,0,0], mi))

        ni = pi * -1 * points2[i][1]
        second = np.concatenate(([0,0,0,0], pi, [0,0,0,0], ni))

        oi = pi * -1 * points2[i][2]
        third = np.concatenate(([0,0,0,0], [0,0,0,0], pi, oi))

        L.append(first)
        L.append(second)
        L.append(third)
    L = np.asarray(L)
    temp = np.matmul(L.transpose(), L)
    vals, vecs = np.linalg.eig(temp)
    vecs = vecs.transpose()
    return np.reshape(vecs[np.argmin(vals)], (4,4))

if __name__ == '__main__':
    t1 = np.array([[46.485,  0.674, 38.613], [46.608,  0.23, 38.603], [46.7,    0.16, 38.613], [46.598,  0.101, 38.593], [46.649,  0.06,  38.562]])
    t2 = np.array([[38.613,  0.674, 46.485], [38.603,  0.23, 46.608], [38.613,  0.16, 46.7], [38.593,  0.101, 46.598], [38.562,  0.06,  46.649]])
    H = computeH(t1.T, t2.T)
    print (H)
    q = np.matmul(H, np.array([6,3,10,1]).T)
    q /= q[3]
    print (q)