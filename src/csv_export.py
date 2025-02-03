import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from src.kinematik import Kinematics
from src.mechanismus import Mechanism

def export_kinematics_to_csv(kinematics: Kinematics, filename="kinematics.csv"):
    print("CSV-Export START")
    angles = range(0, 361, 10)

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        headers = ["Angle"] + [f"Joint_{i}x, Joint{i}_y" for i in range(len(kinematics.mechanism.joints))]
        writer.writerow(headers)

        for angle in angles:
            joints = kinematics.calculate_positions(angle)
            row = [angle] + [coord for joint in joints for coord in (joint.x, joint.y)]
            writer.writerow(row)

    print(f"Kinematik-Daten gespeichert als {filename}")