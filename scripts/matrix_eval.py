import numpy as np

X_init_data = np.array([[3], [4]])
F_data = np.array([[1, 0.001], [0, 1]])
P_init_data = np.array([[9999, 9999], [9999, 9999]])
Q_data = np.array([[1, 0], [0, 1]])
R_data = np.array([[1]])
H_data = np.array([[1, 0]])

Z = np.array([[0]])

# do a KF update

# calculate innovation
X = np.array(X_init_data)
P = np.array(P_init_data)

Y = Z - np.matmul(H_data, X)

S = np.matmul(np.matmul(H_data, P), H_data.T) + R_data

K = np.matmul(np.matmul(P, H_data.T), np.linalg.inv(S))

X = X + np.matmul(K, Y)
P_new = P - np.matmul(np.matmul(K, H_data), P)
breakpoint()
