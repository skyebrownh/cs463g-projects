from copy import deepcopy
from MasterPyraminxModel.Pyraminx import Pyraminx

pyraminx1 = Pyraminx()
pyraminx1.randomize(3)

pyraminx2 = Pyraminx(data=deepcopy(pyraminx1.faces))
pyraminx2.single_move(100, 1.5, 'counterclockwise')

print(pyraminx1 == pyraminx2)
print(pyraminx1)
print(pyraminx2)
