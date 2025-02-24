import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import imageio
import io
import os
from src.mechanismus import Mechanism

def create_schubkurbel_mechanism():
    mech = Mechanism()

    j1 = mech.add_joint(0, 0, fixed=True)
    j2 = mech.add_joint(3, 0)
    j3 = mech.add_joint(6, 0)
    j4 = mech.add_joint(9, 0, fixed=True)

    mech.add_link(j1, j2)
    mech.add_link(j2, j3)
    mech.add_link(j3, j4)

    return mech

def simulate_schubkurbel_gif():
    mech = create_schubkurbel_mechanism()
    angles = np.linspace(0, 360, 36)

    frames = []
    fig, ax = plt.subplots()
    ax.set_xlim(-2, 10)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')

    for theta in angles:
        j1, j2, j3, j4 = mech.joints

        j2.x = j1.x + 3 * np.cos(np.radians(theta))
        j2.y = j1.y + 3 * np.sin(np.radians(theta))
        
        j3.x = j2.x + np.sqrt(max(9 - j2.y**2, 0))
        j3.y = 0

        ax.clear()
        ax.set_xlim(-2, 10)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal')

        for link in mech.links:
            x1, y1 = link.joint1.x, link.joint1.y
            x2, y2 = link.joint2.x, link.joint2.y
            ax.plot([x1, x2], [y1, y2], 'bo-')

        for joint in mech.joints:
            ax.plot(joint.x, joint.y, 'ro' if not joint.fixed else 'go')

        ax.set_title(f"Schubkurbel-Simulation (Winkel: {theta:.1f}°)")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        frames.append(imageio.imread(buf))

    gif_path = os.path.join(os.getcwd(), "schubkurbel_simulation.gif")
    imageio.mimsave(gif_path, frames, duration=0.1)

    return gif_path

if st.sidebar.button("Schubkurbel-Simulation starten", key="schubkurbel_simulation_script"):
    gif_path = simulate_schubkurbel_gif()
    st.image(gif_path, caption="Schubkurbel-Simulation", use_container_width=True)

    with open(gif_path, "rb") as f:
        st.download_button("Download GIF", f, file_name="schubkurbel_simulation.gif", mime="image/gif")
