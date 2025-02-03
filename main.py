import streamlit as st

# Titel der Anwendung
st.title("Kinematische Simulation Ebenen Mechanismen")

# Seitenleiste für Einstellungen
st.sidebar.header("Einstellungen")
st.sidebar.text("Hier können Parameter eingestellt werden.")

# Begrüßungstext
st.write("### Willkommen zur Kinematik-Simulation")
st.write("Diese Anwendung wird es ermöglichen, ebene Mechanismen zu simulieren.")

# Platzhalter für zukünftige Funktionen
st.write("🚀 Simulation folgt hier in zukünftigen Schritten.")

if __name__ == "__main__":
    st.write("App läuft... 🚀")
