import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.kinematik import Kinematics
from src.mechanismus import Mechanism, create_strandbeest_leg

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

updated_joints = kin.calculate_positions(angle)

for i, joint in enumerate(mech.joints):
    if not joint.fixed:  
        joint.x, joint.y = updated_joints[i]

print("Updated Joints:", updated_joints)
for joint in mech.joints:
    print(f"Joint {joint}: ({joint.x}, {joint.y})")


trajectory = kin.calculate_trajectory()

fig, ax = plt.subplots()

for joint, positions in trajectory.items():
    x_vals, y_vals = zip(*positions)  
    ax.plot(x_vals, y_vals, linestyle="dashed", alpha=0.6, label=f"Bahnkurve {joint}")

for link in mech.links:
    x1, y1 = link.joint1.x, link.joint1.y
    x2, y2 = link.joint2.x, link.joint2.y
    ax.plot([x1, x2], [y1, y2], 'bo-')

for joint in mech.joints:
    ax.plot(joint.x, joint.y, 'ro', markersize=6)

ax.set_xlim(-5, 7)
ax.set_ylim(-5, 7)
ax.set_aspect('equal')
ax.set_title("Mechanismus-Simulation mit Bahnkurven")
ax.legend()

st.pyplot(fig)
fig, ax = plt.subplots()

for link in mech.links:
    x1, y1 = link.joint1.x, link.joint1.y
    x2, y2 = link.joint2.x, link.joint2.y
    ax.plot([x1, x2], [y1, y2], 'bo-')

ax.set_xlim(-3, 6)
ax.set_ylim(-3, 6)
ax.set_aspect('equal')
ax.set_title("Mechanismus-Simulation")

st.pyplot(fig)