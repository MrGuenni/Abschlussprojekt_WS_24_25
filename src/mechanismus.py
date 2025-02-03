class Joint:
    #Gelenk ebener Mechanismus
    def __init__(self, x: float, y: float, fixed: bool = False):
        self.x = x  # x-Koordinate des Gelenks
        self.y = y  # y-Koordinate des Gelenks
        self.fixed = fixed  # Ist das Gelenk fest oder beweglich?

    def __repr__(self):
        return f"Joint(x={self.x}, y={self.y}, fixed={self.fixed})"


class Link:
    #starre Verbindung zwischen zwei Gelenken
    def __init__(self, joint1: Joint, joint2: Joint):
        self.joint1 = joint1
        self.joint2 = joint2
        self.length = self.calculate_length()

    def calculate_length(self):
        #Distanz
        return ((self.joint2.x - self.joint1.x) ** 2 + (self.joint2.y - self.joint1.y) ** 2) ** 0.5

    def __repr__(self):
        return f"Link({self.joint1} <-> {self.joint2}, Length={self.length:.2f})"


class Mechanism:
    #Hauptklasse
    def __init__(self):
        self.joints = []
        self.links = []

    def add_joint(self, x: float, y: float, fixed=False):
        joint = Joint(x, y, fixed)
        self.joints.append(joint)
        return joint

    def add_link(self, joint1: Joint, joint2: Joint):
        #Verbindung zwei Gelenke mit festen Glied
        link = Link(joint1, joint2)
        self.links.append(link)

    def __repr__(self):
        return f"Mechanism(Joints={len(self.joints)}, Links={len(self.links)})"
