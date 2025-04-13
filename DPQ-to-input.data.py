import numpy as np

n_beads = 8
n_atoms = 192
total_atoms = n_beads * n_atoms

frame_counter = 0
atom_counter = 0

energy_file = np.loadtxt("NNENERGY", comments="#", usecols=(1))
energy_dict = {i: energy_file[i // n_beads]/n_beads for i in range(len(energy_file)*n_beads)}
energy_index = 0

charge_file = np.loadtxt("NNCHARGE", comments="#", usecols=(3))
charge_dict = {i: charge for i, charge in enumerate(charge_file)}
charge_index = 0

with open('HISTORY', 'r') as f, open('input.data', 'w') as out:
    f.readline()
    f.readline()

    while True:
        line = f.readline()

        if not line:
            break

        if line.strip().startswith("timestep"):

            out.write("begin\n")
            out.write(f"comment Frame {frame_counter}\n")

            timestep_line = line
            frame_number = int(timestep_line.split()[1])
            
            box_lines = [f.readline() for _ in range(3)]
            ang_to_bohr = 1.88973
            force_conversion = 262547.123*1.889726126*1/n_beads
            def convert_box_line(line):
                parts = line.split()
                converted_parts = [str(float(x) * ang_to_bohr) for x in parts]
                return " ".join(converted_parts)
            out.write(f"Lattice {convert_box_line(box_lines[0])}\n")
            out.write(f"Lattice {convert_box_line(box_lines[1])}\n")
            out.write(f"Lattice {convert_box_line(box_lines[2])}\n")
            
            for i in range(0, n_atoms*4, 4):
                atom_lines = f.readline().split()
                coord_line_raw = f.readline().strip()
                coord_line = " ".join([f"{float(x) * ang_to_bohr:15.9f}" for x in coord_line_raw.split()])
                vel_line = f.readline().strip()
                force_line_raw = f.readline().strip()
                force_line = " ".join([f"{float(x) / force_conversion}" for x in force_line_raw.split()])
                
                charge_value = f"{charge_dict[charge_index]:15.9f}"
                out.write(f"atom {coord_line} {atom_lines[0]} {charge_value} 0 {force_line}\n")
                
                charge_index += 1

            energy_value = f"{energy_dict[energy_index]}"
            energy_index += 1
            out.write(f"Energy   {energy_value}\n")
            out.write("Charge   0\n")
            out.write("end\n")

        frame_counter += 1
        atom_counter += n_atoms

print("Conversion completed. 'input.data' has been generated.")
