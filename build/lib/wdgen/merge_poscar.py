import os
from ase.io import read, write

def extract_metadata(filename):
    """
    Extract metadata (distance, alpha, beta, gamma) from the filename.

    :param filename: Filename of the POSCAR file.
    :return: Dictionary containing distance and Euler angles.
    """
    parts = filename.split("_")
    metadata = {
        "distance": float(parts[1][1:]),
        "alpha": int(parts[2][1:]),
        "beta": int(parts[3][1:]),
        "gamma": int(parts[4][1:])
    }
    return metadata

def merge_poscars(input_folder, output_file):
    """
    Merge all POSCAR files in the input folder and save to the output XYZ file.

    :param input_folder: Path to the folder containing POSCAR files.
    :param output_file: Path to the output XYZ file.
    """
    poscar_files = sorted(f for f in os.listdir(input_folder) if f.startswith("POSCAR"))
    all_atoms = []
    all_comments = []

    for file in poscar_files:
        filepath = os.path.join(input_folder, file)
        atoms = read(filepath, format="vasp")
        metadata = extract_metadata(file)

        # Add metadata as a comment line
        comment = f'distance={metadata["distance"]} alpha={metadata["alpha"]} beta={metadata["beta"]} gamma={metadata["gamma"]}'
        all_comments.append(comment)
        all_atoms.append(atoms)

    # Write to XYZ format with comments
    with open(output_file, "w") as xyz_file:
        for atoms, comment in zip(all_atoms, all_comments):
            write(xyz_file, atoms, format="xyz", append=True)
            xyz_file.write(f"{comment}\n")

    print(f"Merged {len(poscar_files)} POSCAR files into {output_file}.")
