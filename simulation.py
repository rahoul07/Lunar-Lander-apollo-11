import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from guidance import Guidance

class Simulation:
    apollo = plt.Rectangle((3,3), width = 2, height = 1, facecolor = "blue", edgecolor = "black")
    ax = plt.gca()
    ax.add_patch(apollo)
    plt.show()

simulate = Simulation()
