from numpy import uint8
import numpy as np

getH1 = np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]], uint8)

getH1C = np.array([9,8,7,6,5,4,3,2,1,0], uint8)

getH2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]*20, uint8)

getH2C = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], uint8)

getXYV1 = np.array(
    [[1,1,0,0],
     [0,1,1,0]], uint8)

getXYV1C = np.array(
    [[1,1,0,0],
     [0,1,1,2]], uint8)

getXYV2 = np.array(
    [[1,1,1,1],
     [0,0,0,0]], uint8)

getXYV2C = np.array(
    [[1,1,1,1],
     [0,1,2,3]], uint8)

getXYV3 = np.array(
    [[0,1,1,0],
     [0,1,1,0]], uint8)

getXYV3C = np.array(
    [[1,1,0,0],
     [1,2,1,2]], uint8)

getQB1 = np.array(
    [[1,1,0,0],
    [0,1,1,0],
    [0,0,0,0],
    [0,0,1,1],
    [0,1,1,0],
    [0,0,0,0],
    [1,1,1,1],
    [0,0,0,0],
    [0,0,0,0],
    [0,1,1,0],
    [0,1,1,0],
    [0,0,0,0],
    [1,1,1,0],
    [0,0,1,0],
    [0,0,0,0],
    [0,1,1,1],
    [0,1,0,0]], uint8)

getQB1C = np.array(
    [[[1,1,0,0],
    [0,1,1,2]],
    [[1,1,0,0],
    [2,3,1,2]],
    [[1,1,1,1],
    [0,1,2,3]],
    [[1,1,0,0],
    [1,2,1,2]],
    [[1,1,1,0],
    [0,1,2,2]],
    [[1,1,1,0],
    [1,2,3,1]]], uint8)

z1 = np.array(
    [[19,19,18,18],
    [5,6,6,7]], uint8)

z1C = np.array(
    [[1,1,0,0],
    [0,1,1,2]], uint8)

getLB1 = np.array(
    [[1,1,1,1],
    [0,1,2,3]], uint8)

getLB1C = np.array([0,0,0,0], uint8), 0

getLB2 = np.array(
    [[19,19,18,18],
    [5,6,6,7]], uint8)

getLB2C = np.array([0,1,1], uint8), 1

getLB3 = np.array(
    [[19,19,18,18],
    [5,6,5,6]], uint8)

getLB3C = np.array([1,1], uint8), 1

getW1 = np.array(
    [[1,1,1,1],
    [0,1,2,3]])

getW1C = 4

getW2 = np.array(
    [[19,19,18,18],
    [5,6,6,7]], uint8)

getW2C = 3

getW3 = np.array(
    [[19,19,18,18],
    [5,6,5,6]], uint8)

getW3C = 2

r1 = np.array(
    [[1,1,1,1],
    [0,1,2,3]], uint8)

r1C1 = np.array([[0,1,2,3],[0,0,0,0]], uint8), 1
r1C2 = np.array([[0,0,0,0],[3,2,1,0]], uint8), 4
r1C3 = np.array([[3,2,1,0],[0,0,0,0]], uint8), 1

r2 = np.array(
    [[1,1,0,0],
    [1,2,1,2]], uint8)

r2C1 = np.array(
    [[0,1,0,1],
    [0,0,1,1]], uint8), 2

r2C2 = np.array(
    [[0,0,1,1],
    [1,0,1,0]], uint8), 2

empty = np.array([[],[]], uint8)

dBCLast1 = np.array(
    [[1,1,0,0],
    [0,1,1,0],
    [0,0,0,0],
    [0,0,1,1],
    [0,1,1,0],
    [0,0,0,0],
    [1,1,1,1],
    [0,0,0,0],
    [0,0,0,0],
    [0,1,1,0],
    [0,1,1,0],
    [0,0,0,0],
    [1,1,1,0],
    [0,0,1,0],
    [0,0,0,0],
    [0,1,1,1],
    [0,1,0,0]], uint8)

dBCLast2 = np.array(
    [[0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],], uint8)

dBCArr = np.array(
    [[0,0,1,1],
    [0,1,1,0],
    [0,0,0,0],
    [1,1,1,1],
    [0,0,0,0],
    [0,0,0,0],
    [0,1,1,0],
    [0,1,1,0],
    [0,0,0,0],
    [1,1,1,0],
    [0,0,1,0],
    [0,0,0,0],
    [0,1,1,1],
    [0,1,0,0],
    [0,0,0,0],
    [1,1,1,1],
    [0,0,0,0]], uint8)

dBCNext = np.array([[0,0,0,0],[0,0,0,0]], uint8)

dBCNextC = np.array([[1,1,0,0],[0,1,1,0]], uint8)