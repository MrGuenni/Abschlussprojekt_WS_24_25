import sys
import os
import numpy as np
from scipy.optimize import fsolve
from src.mechanismus import Mechanism, Joint, Link

class Kinematics:
    def __init__(self, mechanism: Mechanism, driving_joint: Joint):
        self.mechanism = mechanism
        self.driving_joint = driving_joint

    def calculate_positions(self, theta):
        """ Berechnet die Positionen der Gelenke durch Optimierung """
        fixed_joint = next((joint for joint in self.mechanism.joints if joint.fixed), None)
        if fixed_joint is None:
            raise ValueError("Kein festes Gelenk gefunden!")

        # Antriebsgelenk bewegen (Rotation um das feste Gelenk)
        cos_theta = np.cos(np.radians(theta))
        sin_theta = np.sin(np.radians(theta))

        self.driving_joint.x = fixed_joint.x + (self.driving_joint.x - fixed_joint.x) * cos_theta - (self.driving_joint.y - fixed_joint.y) * sin_theta
        self.driving_joint.y = fixed_joint.y + (self.driving_joint.x - fixed_joint.x) * sin_theta + (self.driving_joint.y - fixed_joint.y) * cos_theta

        # Gelenke, die optimiert werden sollen
        variable_joints = [joint for joint in self.mechanism.joints if not joint.fixed]

        def error_function(vars):
            """ Fehlerfunktion: Minimiert die Abweichung von den Soll-Längen der Glieder """
            joint_map = {variable_joints[i]: (vars[2 * i], vars[2 * i + 1]) for i in range(len(variable_joints))}
            eqs = []
            
            for link in self.mechanism.links:
                x1, y1 = link.joint1.x, link.joint1.y
                x2, y2 = link.joint2.x, link.joint2.y

                if link.joint1 in joint_map:
                    x1, y1 = joint_map[link.joint1]
                if link.joint2 in joint_map:
                    x2, y2 = joint_map[link.joint2]

                length_error = ((x2 - x1)**2 + (y2 - y1)**2 - link.length**2)
                eqs.append(length_error)
            
            return eqs

        # Startwerte setzen
        initial_guesses = [coord for joint in variable_joints for coord in (joint.x, joint.y)]

        # Optimierung starten
        result = least_squares(error_function, initial_guesses, xtol=1e-6)

        # Ergebnisse speichern
        for i, joint in enumerate(variable_joints):
            joint.x, joint.y = result.x[2 * i], result.x[2 * i + 1]

        return self.mechanism.joints
    
    def calculate_trajectory(self, angle_range=(0, 360, 2)):
        angles = range(angle_range[0], angle_range[1] + 1, angle_range[2])
        trajectory = {joint: [] for joint in self.mechanism.joints}

        for angle in angles:
            joints = self.calculate_positions(angle)
            for joint in joints:
                trajectory[joint].append((joint.x, joint.y))

        return trajectory



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
    print(kin.calculate_positions(45))