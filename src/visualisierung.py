import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import os
import io
import imageio
import matplotlib.animation as animation
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.kinematik import Kinematics
from src.mechanismus import Mechanism, Joint, Link, create_strandbeest_leg, validate_mechanism
from src.fehleranalyse import compute_errors  # Fehleranalyse-Funktion importieren
from matplotlib.animation import FFMpegWriter
from src.schubkurbel import create_schubkurbel_mechanism, simulate_schubkurbel_gif


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

def animate_mechanism():
    fig, ax = plt.subplots()
    angles = range(0, 361, 10)
    frames = []
    
    for angle in angles:
        kin.calculate_positions(angle)
        ax.clear()
        for link in mech.links:
            x1, y1 = link.joint1.x, link.joint1.y
            x2, y2 = link.joint2.x, link.joint2.y
            ax.plot([x1, x2], [y1, y2], 'bo-')
        for joint in mech.joints:
            ax.plot(joint.x, joint.y, 'ro' if not joint.fixed else 'go')
        ax.set_xlim(-5, 7)
        ax.set_ylim(-5, 7)
        ax.set_aspect('equal')
        ax.set_title(f"Mechanismus-Simulation (Winkel: {angle}°)")
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        frames.append(imageio.imread(buf))
    
    imageio.mimsave("mechanismus.gif", frames, duration=0.1)
    return "mechanismus.gif"

def animate_mechanism_mp4():
    fig, ax = plt.subplots()
    angles = range(0, 361, 10)
    
    writer = FFMpegWriter(fps=10)
    video_path = "mechanismus.mp4"
    
    with writer.saving(fig, video_path, dpi=100):
        for angle in angles:
            kin.calculate_positions(angle)
            ax.clear()
            for link in mech.links:
                x1, y1 = link.joint1.x, link.joint1.y
                x2, y2 = link.joint2.x, link.joint2.y
                ax.plot([x1, x2], [y1, y2], 'bo-')
            for joint in mech.joints:
                ax.plot(joint.x, joint.y, 'ro' if not joint.fixed else 'go')
            ax.set_xlim(-5, 7)
            ax.set_ylim(-5, 7)
            ax.set_aspect('equal')
            ax.set_title(f"Mechanismus-Simulation (Winkel: {angle}°)")
            writer.grab_frame()
    
    return video_path

st.title("Kinematik-Simulation")

st.sidebar.header("Steuerung")
mechanism_options = {
    "Standard-Mechanismus": create_default_mechanism,
    "Strandbeest-Bein": create_strandbeest_leg
}

selected_mechanism = st.sidebar.selectbox("Wähle einen Mechanismus", list(mechanism_options.keys()))
if "mech" not in st.session_state:
    st.session_state["mech"] = mechanism_options[selected_mechanism]()
    st.session_state["kin"] = Kinematics(st.session_state["mech"], st.session_state["mech"].joints[1])

mech = st.session_state["mech"]
kin = st.session_state["kin"]
angle = st.sidebar.slider("Antriebswinkel", 0, 360, 0)

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
        if joint1 != joint2:
            j1 = joint_options[joint1]
            j2 = joint_options[joint2]
            mech.add_link(j1, j2)
            st.sidebar.success(f"Glied zwischen {j1} und {j2} erstellt!")
        else:
            st.sidebar.error("Ein Gelenk kann nicht mit sich selbst verbunden werden!")

# Mechanismus validieren
try:
    validate_mechanism(mech)
except ValueError as e:
    st.error(f"Mechanismus ungültig: {e}")
    st.stop()

updated_joints = kin.calculate_positions(angle)
trajectory = kin.calculate_trajectory()

# Mechanismus zeichnen mit Overlay-Informationen
def plot_mechanism_with_labels():
    fig, ax = plt.subplots()
    
    mech = st.session_state["mech"]  
    
    for link in mech.links:
        x1, y1 = link.joint1.x, link.joint1.y
        x2, y2 = link.joint2.x, link.joint2.y
        ax.plot([x1, x2], [y1, y2], 'bo-')
        ax.annotate(f"{link.length:.2f}", xy=((x1 + x2) / 2, (y1 + y2) / 2), fontsize=9, color="red", ha='left', va='bottom')
    
    for joint in mech.joints:
        ax.plot(joint.x, joint.y, 'ro' if not joint.fixed else 'go')
        ax.annotate(f"({joint.x:.1f}, {joint.y:.1f})", xy=(joint.x, joint.y), fontsize=9, color="blue", ha='right', va='top')
    
    ax.set_xlim(-5, 7)
    ax.set_ylim(-5, 7)
    ax.set_aspect('equal')
    ax.set_title(f"Mechanismus-Simulation (Winkel: {angle}°)")
    st.pyplot(fig)

plot_mechanism_with_labels()

def save_mechanism(mech, filename="mechanismus.json"):
    data = {
        "joints": [{"x": j.x, "y": j.y, "fixed": j.fixed} for j in mech.joints],
        "links": [{"joint1": mech.joints.index(l.joint1), "joint2": mech.joints.index(l.joint2)} for l in mech.links]
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    st.sidebar.success("Mechanismus gespeichert!")

def load_mechanism(filename="mechanismus.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        mech = Mechanism()
        joints = [mech.add_joint(j["x"], j["y"], fixed=j["fixed"]) for j in data["joints"]]

        for link in data["links"]:
            if 0 <= link["joint1"] < len(joints) and 0 <= link["joint2"] < len(joints):
                mech.add_link(joints[link["joint1"]], joints[link["joint2"]])
            else:
                st.sidebar.error(f"❌ Ungültiger Gelenkindex in JSON-Datei: {link}")

        st.sidebar.success("✅ Mechanismus geladen!")

        # 🎯 Mechanismus und Kinematik direkt in `st.session_state` speichern
        st.session_state["mech"] = mech
        st.session_state["kin"] = Kinematics(mech, mech.joints[1])

        # 🎯 Mechanismus mit den neuen Daten zeichnen
        plot_mechanism_with_labels()
        return mech

    except FileNotFoundError:
        st.sidebar.error("❌ Keine gespeicherte Mechanismus-Datei gefunden.")

if st.sidebar.button("Mechanismus speichern"):
    save_mechanism(mech)

if st.sidebar.button("Mechanismus laden"):
    load_mechanism()
    
# Stückliste (BOM) erstellen
st.subheader("Stückliste:")

# Gelenk-Liste erstellen
joint_data = []
for i, joint in enumerate(mech.joints):
    joint_data.append({
        "ID": f"Gelenk {i+1}",
        "X": joint.x,
        "Y": joint.y,
        "Fixiert": "Ja" if joint.fixed else "Nein"
    })

joint_df = pd.DataFrame(joint_data)
st.write("### Gelenke")
st.dataframe(joint_df)

# Glieder-Liste erstellen
link_data = []
for i, link in enumerate(mech.links):
    link_data.append({
        "ID": f"Glied {i+1}",
        "Von": f"Gelenk {mech.joints.index(link.joint1) + 1}",
        "Nach": f"Gelenk {mech.joints.index(link.joint2) + 1}",
        "Länge": round(link.length, 2)
    })

link_df = pd.DataFrame(link_data)
st.write("### Glieder")
st.dataframe(link_df)

# Fehleranalyse-Kontrolle
if st.sidebar.checkbox("Fehleranalyse aktivieren"):
    angles, errors = compute_errors(kin, (0, 360, 10))
    
    fig, ax = plt.subplots()
    ax.plot(angles, errors, marker='o')
    ax.set_xlabel("Winkel (°)")
    ax.set_ylabel("Längen-Fehler")
    ax.set_title(f"Längen-Fehler für {selected_mechanism}")
    st.pyplot(fig)

if st.sidebar.button("GIF erstellen"):
    gif_path = animate_mechanism()
    with open(gif_path, "rb") as f:
        st.download_button("Download Animation (GIF)", f, file_name="mechanismus.gif", mime="image/gif")

if st.sidebar.button("MP4 erstellen"):
    mp4_path = animate_mechanism_mp4()
    with open(mp4_path, "rb") as f:
        st.download_button("Download Animation (MP4)", f, file_name="mechanismus.mp4", mime="video/mp4")

if st.sidebar.button("Schubkurbel-Simulation starten", key="schubkurbel_simulation_viz"):
    gif_path = simulate_schubkurbel_gif()
    st.image(gif_path, caption="Schubkurbel-Simulation", use_container_width=True)

    with open(gif_path, "rb") as f:
        st.download_button("Download GIF", f, file_name="schubkurbel_simulation.gif", mime="image/gif")

