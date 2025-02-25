# Kinematik-Simulation von Mechanismen

## Beschreibung
Diese Anwendung ermöglicht die Simulation von ebenen Mechanismen und deren Kinematik.
Die Berechnung erfolgt mit einer Optimierungsmethode (`scipy.optimize.least_squares`), während die Visualisierung über **Streamlit** bereitgestellt wird.

## Installation & Lokale Ausführung

### 1. Projekt klonen
`bash
git clone` https://github.com/MrGuenni/Abschlussprojekt_WS_24_25.git


### 2. Virtuelle Umgebung erstellen & Abhängigkeiten installieren
bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt


### 3. Anwendung starten (lokal)
bash
streamlit run src/visualisierung.py


## **Online-Demo**
Um die Online-App zu testen, bitte [hier](https://abschlussprojektws2425-v7ij3cuvrdqrpv2vmnyy6b.streamlit.app/) klicken.

## **Funktionen**
- Mechanismen erstellen & speichern  
- Bahnkurven berechnen & visualisieren  
- Simulation mit Optimierungsmethoden  
- Export der Kinematik-Daten als CSV  
- Validierung der Mechanismen  
- Streamlit-Web-UI zur Interaktion  

## **Verwendete Technologien**
- **Python** (Backend-Logik)
- **Streamlit** (Web-Interface)
- **Matplotlib** (Visualisierung)
- **SciPy & NumPy** (Optimierung)

## **Autoren**
- **Andre Muther** (@tt-st1)
- **Günter Steininger** (@MrGuenni)

## **Projektstruktur**
Die Projektstruktur entspricht in etwa wie folgt.

````ABSSCHLUSSPROJEKT_WS_24_25/
│── src/
│   │── __init__.py
│   │── csv_export.py
│   │── dateibearbeitung.py
│   │── fehleranalyse.py
│   │── kinematik.py
│   │── mechanismus.py
│   │── schubkurbel.py
│   │── test_dateibearbeitung.py
|   |── ui_mechanismus.py
|   |── visualisierung.py
│── tests/
│   │── test_mechanismus.py
│── venv/
│── kinematics.csv
│── LICENSE
│── main.py
|── mechanismus.gif
│── mechanismus.json
│── README.md
│── requirements.txt
│── schubkurbel_simulation.gif
│── src__init__.py
│── testfile.txt
````


## **Lizenz**
MIT License

##
genauere Details, siehe [Bericht](Muther_Steininger_Bericht.pdf)
