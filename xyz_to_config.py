import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Convert an xyz file to a CONFIG file (Cubic) for DL_POLY Quantum")
    parser.add_argument("xyz_file", help="Path to the input xyz file")
    parser.add_argument("-o", "--output", default="CONFIG", help="Path for the output CONFIG file")
    args = parser.parse_args()

    xyz_path = Path(args.xyz_file)
    with open(xyz_path, "r") as f:
        lines = f.readlines()

    natoms = int(lines[0])
    data_lines = lines[2:]
    atoms = []
    for i, line in enumerate(data_lines):
        parts = line.strip().split()
        if parts:
            symbol = parts[0]
            x, y, z = map(float, parts[1:4])
            atoms.append((symbol, i + 1, x, y, z))

    a = float(input("Enter cubic cell length: "))

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        f.write("Built   with    xyz_to_config.py\n")
        f.write(f"{0:>10}{1:>10}{natoms:>10}\n")
        f.write(f"{a:>15.6f}{0.0:>15.6f}{0.0:>15.6f}\n")
        f.write(f"{0.0:>15.6f}{a:>15.6f}{0.0:>15.6f}\n")
        f.write(f"{0.0:>15.6f}{0.0:>15.6f}{a:>15.6f}\n")
        for atom in atoms:
            f.write(f"{atom[0]:<8}{atom[1]:>7}\n")
            f.write(f"{atom[2]:>15.6f}{atom[3]:>15.6f}{atom[4]:>15.6f}\n")
        print(f"Converted {xyz_path} to {output_path}")

if __name__ == "__main__":
    main()
