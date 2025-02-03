import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from scipy.optimize import fsolve
from src.mechanismus import Mechanism, Joint, Link

class Kinematics:
    """Klasse zur Berechnung der Kinematik eines Mechanismus."""

    def __init__(self, mechanism: Mechanism, driving_joint: Joint):
        self.mechanism = mechanism
        self.driving_joint = driving_joint

    def calculate_positions(self, theta):
        """
        Berechnet die Positionen der beweglichen Gelenke für einen gegebenen Drehwinkel theta.
        """
        def equations(vars, joint_positions, links):
            """Gleichungssystem für die Kinematik."""
            eqs = []
            index = 0

            for link in links:
                # Korrekte Nutzung des Dictionarys für feste Gelenke
                x1, y1 = joint_positions[link.joint1]  # ✅ Jetzt wird das Dictionary genutzt
                
                # Falls das zweite Gelenk beweglich ist, hole Werte aus `vars`, sonst aus `joint_positions`
                if link.joint2 in joint_positions:
                    x2, y2 = joint_positions[link.joint2]
                else:
                    x2, y2 = vars[index], vars[index + 1]
                    index += 2

                # Füge die Gleichung für die Längenbeschränkung des Glieds hinzu
                eqs.append((x2 - x1) ** 2 + (y2 - y1) ** 2 - link.length ** 2)

            return eqs


        # Gelenkpositionen als Dictionary vorbereiten
        joint_positions = {joint: (joint.x, joint.y) for joint in self.mechanism.joints if joint.fixed}

        # Startwerte für bewegliche Gelenke sammeln
        initial_guesses = []
        variable_joints = []
        for joint in self.mechanism.joints:
            if not joint.fixed:
                initial_guesses.extend([joint.x, joint.y])
                variable_joints.append(joint)

        # Optimierung mit scipy.fsolve
        # Dictionary mit Gelenkpositionen erstellen
        joint_positions = {joint: (joint.x, joint.y) for joint in self.mechanism.joints}

        # fsolve mit Dictionary-Aufruf
        result = fsolve(equations, initial_guesses, args=(joint_positions, self.mechanism.links))

        # Aktualisiere die Gelenkpositionen mit den berechneten Werten
        index = 0
        for joint in variable_joints:
            joint.x, joint.y = result[index], result[index + 1]
            joint_positions[joint] = (joint.x, joint.y)  # Speichere neue Werte im Dictionary
            index += 2

        return self.mechanism.joints

# Testlauf mit einem Viergelenkgetriebe
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