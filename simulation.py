import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from guidance import Guidance
import numpy as np

class Simulation:
    system = Guidance()
    data = system.simulation()

    # the main plot
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, data["altitude"][0]+15)
    
    #adding a thrust over time graph
    f, a = plt.subplots()
    a.plot(data["time"][1:], data["thrust"][1:])
    a.set_ylim(24800, 26100)
    a.set_xlabel("Time (s)")
    a.set_ylabel("Thrust (N)")
    a.set_title("Thrust over Time")
    a.grid(True)

    #adding a velocity over time
    fa, an = plt.subplots()
    an.plot(data["time"][1:], data["velocity"][1:])
    an.set_xlabel("Time (s)")
    an.set_ylabel("Velocity (m/s)")
    an.set_title("Velocity over Time")
    an.grid(True)

    # drawing the landing module
    # square (45, 200), (45, 195), (55, 200), (55, 195) plus a parallelogram (45, 195), (40, 190), (55, 195), (60, 190)
    Polygon_verticies = np.array([[47, 0], [53, 0], [52, 5], [52, 10], [48, 10], [48, 5]])
    apollo_11 = patches.Polygon(Polygon_verticies, closed = True, facecolor = "blue", edgecolor = "black")
    ax.add_patch(apollo_11)

    #updating frame req for function animation call
    def update(frame, shape, verticies, data):
        shape.set_xy(verticies + np.array([0, data["altitude"][frame]]))
        return (shape,)

    #animating
    animate = FuncAnimation(fig, update, frames=list(range(0, len(data["altitude"]), 5)) + [len(data["altitude"])-1], fargs=(apollo_11, Polygon_verticies, data), interval=33, blit=True, repeat = False)
    animate.save("2dLander.gif", writer = "pillow", fps = 33)
    
    # thrust graph+ velocity graph
    fa.savefig("velocity.png")
    f.savefig("thrust.png")
    plt.show()

simulate = Simulation()
