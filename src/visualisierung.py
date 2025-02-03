import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.kinematik import Kinematics
from src.mechanismus import Mechanism

st.title("Kinematik-Simulation")

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

angle = st.slider("Antriebswinkel", 0, 360, 0)

updated_joints = kin.calculate_positions(angle)

fig, ax = plt.subplots()

for link in mech.links:
    x1, y1 = link.joint1.x, link.joint1.y
    x2, y2 = link.joint2.x, link.joint2.y
    ax.plot([x1, x2], [y1, y2], 'bo-')

ax.set_xlim(-3, 5)
ax.set_ylim(-3, 5)
ax.set_aspect('equal')
ax.set_title("Mechanismus-Simulation")

st.pyplot(fig)