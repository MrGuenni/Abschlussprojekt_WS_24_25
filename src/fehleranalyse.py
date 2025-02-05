import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from src.kinematik import Kinematics
from src.mechanismus import Mechanism

def compute_errors(kinematics, angle_range):
    errors = []
    angles = np.arange(angle_range[0], angle_range[1] + 1, angle_range[2])
    
    for angle in angles:
        kinematics.calculate_positions(angle)
        error = sum(abs(((link.joint2.x - link.joint1.x)**2 + (link.joint2.y - link.joint1.y)**2)**0.5 - link.length) for link in kinematics.mechanism.links)
        errors.append(error)
    
    return angles, errors

st.title("Längen-Fehler-Analyse")

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
angles, errors = compute_errors(kin, (0, 360, 10))

fig, ax = plt.subplots()
ax.plot(angles, errors, marker='o')
ax.set_xlabel("Winkel (°)")
ax.set_ylabel("Längen-Fehler")
ax.set_title("Längen-Fehler über den Drehwinkel")

st.pyplot(fig)
