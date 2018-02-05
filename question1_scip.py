from pyscipopt import Model, quicksum, multidict


GRID_HEIGHT = 600
GRID_WIDTH = 600


model = Model("try")


x = model.addVar("n1")
y = model.addVar("n2")


model.addCons(2 * x + y <= 10, "bound costs")
model.addCons(2 * x + 5 * y <= 30, "bound costs")

model.setObjective(x + y, "maximize")  # autre possibilité "minimize"
model.optimize()

print("Optimal value: %f" % model.getObjVal())
print("x: = %f" % model.getVal(x))
print("y: = %f" % model.getVal(y))