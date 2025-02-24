import streamlit as st

st.title("Kinematische Simulation Ebenen Mechanismen")

st.sidebar.header("Einstellungen")
st.sidebar.text("Hier können Parameter eingestellt werden.")

st.write("### Das ist unsere Kinematik-Simulation")
st.write("Diese Anwendung soll es ermöglichen, ebene Mechanismen zu simulieren.")


if __name__ == "__main__":
    st.write("App läuft...")
