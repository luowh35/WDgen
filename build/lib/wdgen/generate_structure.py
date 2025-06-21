from wdgen.dipole_generator import DipoleGenerator

def generate_structures_from_params(param_file):
    """
    Generate molecular structures based on a parameter file.

    :param param_file: Path to the parameter JSON file.
    """
    generator = DipoleGenerator(param_file)
    generator.generate_structures()
    print(f"Structures generated in {generator.params['output_folder']}.")
