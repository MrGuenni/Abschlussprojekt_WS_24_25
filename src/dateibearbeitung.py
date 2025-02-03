import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from src.mechanismus import Mechanism, Joint, Link

def save_mechanism(mechanism: Mechanism, filename="mechanism.json"):
    data = {
        "joints": [{"x": j.x, "y": j.y, "fixed": j.fixed} for j in mechanism.joints],
        "links": [{"joint1": mechanism.joints.index(l.joint1), "joint2": mechanism.joints.index(l.joint2)} for l in mechanism.links]
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Mechanismus gespeichert als {filename}")

def load_mechanism(filename="mechanism.json"):
    #Mechanismus aus JSON Datei laden
    with open(filename, "r") as f:
        data = json.load(f)

    mechanism = Mechanism()
    joints = [mechanism.add_joint(j["x"], j["y"], j["fixed"]) for j in data["joints"]]

    for l in data["links"]:
        mechanism.add_link(joints[l["joint1"]], joints[l["joint2"]])

    return mechanism
