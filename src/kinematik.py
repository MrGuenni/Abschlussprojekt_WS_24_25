import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
            index = 0
            num_vars = len(vars)

            for link in links:
                if link.joint1 in joint_positions:
                    x1, y1 = joint_positions[link.joint1]
                else:
                    if index + 1 >= num_vars:
                        continue
                    x1, y1 = vars[index], vars[index + 1]
                    index += 2

                if link.joint2 in joint_positions:
                    x2, y2 = joint_positions[link.joint2]
                else:
                    if index + 1 >= num_vars:
                        continue
                    x2, y2 = vars[index], vars[index + 1]
                    index += 2

                eqs.append((x2 - x1) ** 2 + (y2 - y1) ** 2 - link.length ** 2)

            return eqs

        initial_guesses = []
        variable_joints = []

        for joint in self.mechanism.joints:
            if not joint.fixed and joint != self.driving_joint:
                initial_guesses.extend([joint.x, joint.y])
                variable_joints.append(joint)

        if not initial_guesses:
            raise ValueError("Initial Guesses für fsolve sind leer!")

        result = fsolve(equations, initial_guesses, args=(variable_joints, joint_positions, self.mechanism.links), xtol=1e-6)


        index = 0
        for joint in variable_joints:
            joint.x, joint.y = result[index], result[index + 1]
            index += 2

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