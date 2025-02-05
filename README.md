# 🚀 Kinematik-Simulation von Mechanismen

## 🏰 Projektbeschreibung
Diese Anwendung ermöglicht die Simulation von ebenen Mechanismen und deren Kinematik.
Die Berechnung erfolgt mit einer Optimierungsmethode (`scipy.optimize.least_squares`), während die Visualisierung über **Streamlit** bereitgestellt wird.

## 👅 Installation & Lokale Ausführung

### 1. Projekt klonen
bash
git clone https://github.com/MrGuenni/Abschlussprojekt_WS_24_25.git


### 2. Virtuelle Umgebung erstellen & Abhängigkeiten installieren
bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

pip install -r requirements.txt


### 3. Anwendung starten (lokal)
bash
streamlit run src/visualisierung.py


## 🌍 **Online-Demo**
👉 **[Hier klicken, um die App online zu testen](https://abschlussprojektws2425-v7ij3cuvrdqrpv2vmnyy6b.streamlit.app/)** 🚀  

## 🔬 **Funktionen**
✔ Mechanismen erstellen & speichern  
✔ Bahnkurven berechnen & visualisieren  
✔ Simulation mit Optimierungsmethoden  
✔ Export der Kinematik-Daten als CSV  
✔ Validierung der Mechanismen  
✔ Streamlit-Web-UI zur Interaktion  

## 🛠 **Verwendete Technologien**
- **Python** (Backend-Logik)
- **Streamlit** (Web-Interface)
- **Matplotlib** (Visualisierung)
- **SciPy & NumPy** (Optimierung)

## 👨‍💻 **Autoren**
- **Andre Muther** (@tt-st1)
- **Günter Steininger** (@MrGuenni)

## 📚 **Projektstruktur**
Die Projektstruktur entspricht dem Screenshot, den ihr mir gegeben habt. Die wichtigsten Dateien:

````ABSSCHLUSSPROJEKT_WS_24_25/
│── src/
│   │── csv_export.py
│   │── dateibearbeitung.py
│   │── kinematik.py
│   │── mechanismus.py
│   │── test_dateibearbeitung.py
│   │── test_mechanismus.py
│   │── ui_mechanismus.py
│   │── visualisierung.py
│── tests/
│   │── test_mechanismus.py
│── venv/
│── kinematics.csv
│── LICENSE
│── main.py
│── mechanismus.json
│── README.md
│── requirements.txt
│── testfile.txt
````


## 📝 **Lizenz**
MIT License

