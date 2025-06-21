import os
import json
from .molecule_reader import MoleculeReader
from .transform_utils import TransformUtils
from .poscar_writer import PoscarWriter


class DipoleGenerator:
    def __init__(self, param_file):
        self.params = self.read_params(param_file)
        self.base_coords = MoleculeReader.read_from_file(self.params["molecule_file"])

        self.distances = TransformUtils.generate_range(
            self.params["distance"]["start"],
            self.params["distance"]["end"],
            self.params["distance"]["step"]
        )
        self.alpha_range = TransformUtils.generate_range(
            self.params["angles"]["alpha"]["start"],
            self.params["angles"]["alpha"]["end"],
            self.params["angles"]["alpha"]["step"]
        ).astype(int)
        self.beta_range = TransformUtils.generate_range(
            self.params["angles"]["beta"]["start"],
            self.params["angles"]["beta"]["end"],
            self.params["angles"]["beta"]["step"]
        ).astype(int)
        self.gamma_range = TransformUtils.generate_range(
            self.params["angles"]["gamma"]["start"],
            self.params["angles"]["gamma"]["end"],
            self.params["angles"]["gamma"]["step"]
        ).astype(int)

        self.angles = [(a, b, g) for a in self.alpha_range for b in self.beta_range for g in self.gamma_range]

    @staticmethod
    def read_params(filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def generate_water_molecule(self, base_coords, shift):
        return [[atom[0], atom[1] + shift[0], atom[2] + shift[1], atom[3] + shift[2]] for atom in base_coords]

    def generate_structures(self):
        water1 = self.generate_water_molecule(self.base_coords, self.params["initial_shift"])
        os.makedirs(self.params["output_folder"], exist_ok=True)

        for distance in self.distances:
            shift2 = [self.params["initial_shift"][0],
                      self.params["initial_shift"][1],
                      self.params["initial_shift"][2] + distance]
            water2 = self.generate_water_molecule(self.base_coords, shift2)
            center = MoleculeReader.geometric_center(water2)

            for angle_set in self.angles:
                rotated_water2 = TransformUtils.rotate(water2, center, angle_set)
                combined_atoms = water1 + rotated_water2
                angle_str = f"a{angle_set[0]}_b{angle_set[1]}_g{angle_set[2]}"
                filename = os.path.join(
                    self.params["output_folder"],
                    f"POSCAR_d{distance:.2f}_{angle_str}"
                )
                PoscarWriter.save(filename, combined_atoms, self.params["box_size"])
