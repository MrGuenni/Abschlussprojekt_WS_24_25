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
        fixed_joint = None
        for joint in self.mechanism.joints:
            if joint.fixed:
                fixed_joint = joint
                break

        if fixed_joint is None:
            raise ValueError("Kein festes Gelenk gefunden!")

        cos_theta = np.cos(np.radians(theta))
        sin_theta = np.sin(np.radians(theta))

        self.driving_joint.x = fixed_joint.x + (self.driving_joint.x - fixed_joint.x) * cos_theta - (self.driving_joint.y - fixed_joint.y) * sin_theta
        self.driving_joint.y = fixed_joint.y + (self.driving_joint.x - fixed_joint.x) * sin_theta + (self.driving_joint.y - fixed_joint.y) * cos_theta

        joint_positions = {joint: (joint.x, joint.y) for joint in self.mechanism.joints if joint.fixed}

        def equations(vars, variable_joints, joint_positions, links):
            eqs = []
            joint_map = {variable_joints[i]: (vars[2 * i], vars[2 * i + 1]) for i in range(len(variable_joints))}

            for link in links:
                x1, y1 = joint_positions.get(link.joint1, joint_map.get(link.joint1, (None, None)))
                x2, y2 = joint_positions.get(link.joint2, joint_map.get(link.joint2, (None, None)))

                if x1 is None or y1 is None or x2 is None or y2 is None:
                    continue

                eqs.append((x2 - x1) ** 2 + (y2 - y1) ** 2 - link.length ** 2)

            return eqs

        initial_guesses = []
        variable_joints = []

        for joint in self.mechanism.joints:
            if not joint.fixed:
                if joint.x is None or joint.y is None:
                    raise ValueError(f"Gelenk {joint} hat ungültige Koordinaten!")
                initial_guesses.extend([max(abs(joint.x), 1e-3) * np.sign(joint.x),
                                        max(abs(joint.y), 1e-3) * np.sign(joint.y)])
                variable_joints.append(joint)

        if not initial_guesses:
            raise ValueError("Fehler: Keine beweglichen Gelenke gefunden!")

        
        for link in self.mechanism.links:
            length = np.sqrt((link.joint1.x - link.joint2.x) ** 2 + (link.joint1.y - link.joint2.y) ** 2)
            correction_factor = link.length / length if length != 0 else 1  

            link.joint2.x = link.joint1.x + (link.joint2.x - link.joint1.x) * correction_factor
            link.joint2.y = link.joint1.y + (link.joint2.y - link.joint1.y) * correction_factor


        res = fsolve(equations, initial_guesses, args=(variable_joints, joint_positions, self.mechanism.links), xtol=1e-6)

        for i, joint in enumerate(variable_joints):
            joint.x, joint.y = res[2 * i], res[2 * i + 1]

        return self.mechanism.joints

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