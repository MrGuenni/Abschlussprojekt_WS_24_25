import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mechanismus import Mechanism
from src.mechanismus import create_strandbeest_leg

mech = Mechanism()
j1 = mech.add_joint(0, 0, fixed=True)
j2 = mech.add_joint(2, 0)
j3 = mech.add_joint(2, 2)
mech.add_link(j1, j2)
mech.add_link(j2, j3)
mech.add_link(j1, j3)

print(mech)
for link in mech.links:
    print(link)

mech = create_strandbeest_leg()
print(mech)