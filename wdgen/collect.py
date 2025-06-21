import os
from ase.io import read

class PoscarCollector:
    @staticmethod
    def extract_metadata(filename):
        parts = filename.split("_")
        return {
            "distance": float(parts[1][1:]),
            "alpha": int(parts[2][1:]),
            "beta": int(parts[3][1:]),
            "gamma": int(parts[4][1:])
        }

    @staticmethod
    def read_lattice_from_poscar(filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
            # POSCAR格式中第3-5行是晶格矢量
            lattice = []
            for i in range(2, 5):
                vec = [float(x) for x in lines[i].split()]
                lattice.append(vec)
            return lattice

    @staticmethod
    def collect(input_folder, output_file):
        poscar_files = sorted(f for f in os.listdir(input_folder) if f.startswith("POSCAR"))
        
        with open(output_file, "w") as fout:
            for file in poscar_files:
                filepath = os.path.join(input_folder, file)
                atoms = read(filepath, format="vasp")
                lattice = PoscarCollector.read_lattice_from_poscar(filepath)
                metadata = PoscarCollector.extract_metadata(file)

                fout.write(f"{len(atoms)}\n")
                lattice_str = " ".join(" ".join(f"{v:.5f}" for v in vec) for vec in lattice)
                fout.write(f'Lattice="{lattice_str}" Properties=species:S:1:pos:R:3\n')
                for sym, pos in zip(atoms.get_chemical_symbols(), atoms.get_positions()):
                    fout.write(f"{sym} {pos[0]:.5f} {pos[1]:.5f} {pos[2]:.5f}\n")
