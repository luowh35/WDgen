import numpy as np

class MoleculeReader:
    @staticmethod
    def read_from_file(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()[1:]
            return [
                [line.split()[0], float(line.split()[1]), float(line.split()[2]), float(line.split()[3])]
                for line in lines if line.strip()
            ]

    @staticmethod
    def geometric_center(coords):
        positions = np.array([[atom[1], atom[2], atom[3]] for atom in coords])
        return positions.mean(axis=0)
