import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.mechanismus import Mechanism

mech = Mechanism()
st.title("Mechanismus-Erstellung")

st.sidebar.header("Gelenke hinzufügen")
x = st.sidebar.number_input("X-Koordinate", value=0.0)
y = st.sidebar.number_input("Y-Koordinate", value=0.0)
fixed = st.sidebar.checkbox("Fixiertes Gelenk")

if st.sidebar.button("Gelenk hinzufügen"):
    joint = mech.add_joint(x, y, fixed)
    st.sidebar.success(f"Gelenk {joint} hinzugefügt!")

st.sidebar.header("Glieder hinzufügen")
if len(mech.joints) >= 2:
    joint_options = {f"Joint {i}": j for i, j in enumerate(mech.joints)}
    joint1 = st.sidebar.selectbox("Erstes Gelenk", list(joint_options.keys()))
    joint2 = st.sidebar.selectbox("Zweites Gelenk", list(joint_options.keys()))

    if st.sidebar.button("Glied hinzufügen"):
        j1 = joint_options[joint1]
        j2 = joint_options[joint2]
        mech.add_link(j1, j2)
        st.sidebar.success(f"Glied zwischen {j1} und {j2} erstellt!")

st.write("### Aktuelle Gelenke:")
for i, joint in enumerate(mech.joints):
    st.write(f"Gelenk {i+1}: x={joint.x}, y={joint.y}, {'fixiert' if joint.fixed else 'beweglich'}")

st.write("### Aktuelle Glieder:")
for i, link in enumerate(mech.links):
    st.write(f"Glied {i+1}: {link.joint1} ↔ {link.joint2}, Länge: {link.length:.2f}")