import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from src.kinematik import Kinematics
from src.mechanismus import Mechanism

def export_kinematics_to_csv(kinematics: Kinematics, filename="kinematics.csv"):
    angles = range(0, 361, 10)

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        headers = ["Angle"] + [f"Joint_{i}_x" for i in range(len(kinematics.mechanism.joints))] + \
                  [f"Joint_{i}_y" for i in range(len(kinematics.mechanism.joints))]
        writer.writerow(headers)

        for angle in angles:
            joints = kinematics.calculate_positions(angle)
            row = [angle] + [joint.x for joint in joints] + [joint.y for joint in joints]
            writer.writerow(row)

    print(f"Kinematik-Daten gespeichert als {filename}")

if __name__ == "__main__":
    mech = Mechanism()
    j1 = mech.add_joint(0, 0, fixed=True)
    j2 = mech.add_joint(2, 0)
    j3 = mech.add_joint(2, 2)
    j4 = mech.add_joint(0, 2, fixed=True)

    mech.add_link(j1, j2)
    mech.add_link(j2, j3)
    mech.add_link(j3, j4)
    mech.add_link(j4, j1)

    kin = Kinematics(mech, j2)
    export_kinematics_to_csv(kin)