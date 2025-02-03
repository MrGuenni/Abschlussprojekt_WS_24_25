class Joint:
    def __init__(self, x: float, y: float, fixed: bool = False):
        self.x = x
        self.y = y
        self.fixed = fixed

    def __repr__(self):
        return f"Joint(x={self.x}, y={self.y}, fixed={self.fixed})"


class Link:
    def __init__(self, joint1: Joint, joint2: Joint):
        self.joint1 = joint1
        self.joint2 = joint2
        self.length = self.calculate_length()

    def calculate_length(self):
        return ((self.joint2.x - self.joint1.x) ** 2 + (self.joint2.y - self.joint1.y) ** 2) ** 0.5

    def __repr__(self):
        return f"Link({self.joint1} <-> {self.joint2}, Length={self.length:.2f})"


class Mechanism:
    def __init__(self):
        self.joints = []
        self.links = []

    def add_joint(self, x: float, y: float, fixed=False):
        joint = Joint(x, y, fixed)
        self.joints.append(joint)
        return joint

    def add_link(self, joint1: Joint, joint2: Joint):
        link = Link(joint1, joint2)
        self.links.append(link)

    def __repr__(self):
        return f"Mechanism(Joints={len(self.joints)}, Links={len(self.links)})"


def create_strandbeest_leg() -> Mechanism:
    mech = Mechanism()
    
    j1 = mech.add_joint(0, 0, fixed=True)
    j2 = mech.add_joint(5, 0)
    j3 = mech.add_joint(4, 3)
    j4 = mech.add_joint(1, 3, fixed=True)
    j5 = mech.add_joint(3, 1.5)
    j6 = mech.add_joint(2, 2)

    mech.add_link(j1, j2)
    mech.add_link(j2, j3)
    mech.add_link(j3, j4)
    mech.add_link(j4, j1)
    mech.add_link(j2, j5)
    mech.add_link(j5, j6)
    mech.add_link(j6, j3)

    return mech
