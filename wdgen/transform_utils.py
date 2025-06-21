import numpy as np

class TransformUtils:
    @staticmethod
    def generate_range(start, end, step):
        if abs(end - start) < 1e-8:
            return np.array([start])
        else:
            return np.arange(start, end + step * 0.5, step)

    @staticmethod
    def euler_to_rotation_matrix(alpha, beta, gamma):
        alpha, beta, gamma = np.radians([alpha, beta, gamma])
        Rz1 = np.array([[np.cos(alpha), -np.sin(alpha), 0],
                        [np.sin(alpha),  np.cos(alpha), 0],
                        [0,             0,             1]])
        Ry = np.array([[np.cos(beta),  0, np.sin(beta)],
                       [0,             1, 0],
                       [-np.sin(beta), 0, np.cos(beta)]])
        Rz2 = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                        [np.sin(gamma),  np.cos(gamma), 0],
                        [0,              0,             1]])
        return Rz2 @ Ry @ Rz1

    @staticmethod
    def rotate(coords, center, euler_angles):
        rot_mat = TransformUtils.euler_to_rotation_matrix(*euler_angles)
        rotated = []
        for atom in coords:
            pos = np.array([atom[1], atom[2], atom[3]]) - center
            rotated_pos = rot_mat @ pos + center
            rotated.append([atom[0], *rotated_pos])
        return rotated
