import argparse
from .dipole_generator import DipoleGenerator
from .collect import PoscarCollector


def main():
    parser = argparse.ArgumentParser(description="Generate and collect dipole structures.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 子命令：生成结构
    generate_parser = subparsers.add_parser("gen", help="Generate dipole structures.")
    generate_parser.add_argument("-p", "--params", type=str, required=True, help="Path to parameter JSON file.")

    # 子命令：合并结构
    collect_parser = subparsers.add_parser("collect", help="Collect POSCAR files into an XYZ file.")
    collect_parser.add_argument("-i", "--input", type=str, required=True, help="Input folder containing POSCAR files.")
    collect_parser.add_argument("-o", "--output", type=str, required=True, help="Output XYZ file.")

    args = parser.parse_args()

    if args.command == "gen":
        generator = DipoleGenerator(args.params)
        generator.generate_structures()
        print(f"Successfully generated structures in {generator.params['output_folder']}!")

    elif args.command == "collect":
        PoscarCollector.collect(args.input, args.output)

if __name__ == "__main__":
    main()
