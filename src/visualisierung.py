import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.kinematik import Kinematics
from src.mechanismus import Mechanism, Joint, Link, create_strandbeest_leg, validate_mechanism

def create_default_mechanism():
    mech = Mechanism()
    j1 = mech.add_joint(0, 0, fixed=True)
    j2 = mech.add_joint(2, 0)
    j3 = mech.add_joint(2, 2)
    j4 = mech.add_joint(0, 2, fixed=True)

    mech.add_link(j1, j2)
    mech.add_link(j2, j3)
    mech.add_link(j3, j4)
    mech.add_link(j4, j1)

    return mech

st.title("Kinematik-Simulation")

mechanism_options = {
    "Standard-Mechanismus": create_default_mechanism,
    "Strandbeest-Bein": create_strandbeest_leg
}

selected_mechanism = st.selectbox("Wähle einen Mechanismus", list(mechanism_options.keys()))

mech = mechanism_options[selected_mechanism]()

kin = Kinematics(mech, mech.joints[1])

angle = st.slider("Antriebswinkel", 0, 360, 0)

try:
    validate_mechanism(mech)
    updated_joints = kin.calculate_positions(angle)
except ValueError as e:
    st.error(f"Fehler: {e}")
    st.stop()

updated_joints = kin.calculate_positions(angle)
trajectory = kin.calculate_trajectory()

fig, ax = plt.subplots()

for i, (joint, positions) in enumerate(trajectory.items()):
    x_vals, y_vals = zip(*positions)
    ax.plot(x_vals, y_vals, linestyle="dashed", alpha=0.6, label=f"Gelenk {i+1}")

for link in mech.links:
    x1, y1 = link.joint1.x, link.joint1.y
    x2, y2 = link.joint2.x, link.joint2.y
    ax.plot([x1, x2], [y1, y2], 'bo-')
    ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{link.length:.2f}", fontsize=8, color="red")

for joint in mech.joints:
    ax.plot(joint.x, joint.y, 'ro' if not joint.fixed else 'go')
    ax.text(joint.x, joint.y, f"({joint.x:.1f}, {joint.y:.1f})", fontsize=8, color="blue")

ax.set_xlim(-5, 7)
ax.set_ylim(-5, 7)
ax.set_aspect('equal')
ax.set_title(f"Mechanismus-Simulation (Winkel: {angle}°)")
ax.legend()
st.pyplot(fig)

angles = np.arange(0, 361, 10)
errors = []
for theta in angles:
    kin.calculate_positions(theta)
    error = sum(abs(((link.joint2.x - link.joint1.x)**2 + (link.joint2.y - link.joint1.y)**2)**0.5 - link.length) for link in mech.links)
    errors.append(error)

fig2, ax2 = plt.subplots()
ax2.plot(angles, errors, marker='o')
ax2.set_xlabel("Winkel (°)")
ax2.set_ylabel("Längen-Fehler")
ax2.set_title("Längen-Fehler über den Drehwinkel")
st.pyplot(fig2)