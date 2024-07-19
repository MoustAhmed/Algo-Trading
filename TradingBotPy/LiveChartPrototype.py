import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import mplcursors

# Function to generate random data
def generate_data():
    return np.random.rand()

# Set up the figure and axis
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'b-', animated=True)

# Initialize the plot
def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1)
    return ln,

# Update the plot
def update(frame):
    xdata.append(frame)
    ydata.append(generate_data())
    
    # Keep only the last 10 seconds of data
    if len(xdata) > 30:
        xdata.pop(0)
        ydata.pop(0)
        
    # Update the data in the plot
    ln.set_data(xdata, ydata)
    
    # Update the x-axis to show the most recent 10 seconds
    ax.set_xlim(xdata[0], xdata[-1])
    
    # Update the y-axis to fit the current data range
    ax.set_ylim(min(ydata) - 0.1, max(ydata) + 0.1)
    
    return ln,

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 1000, 0.1),
                              init_func=init, blit=True, interval=50)

# Enable zooming and panning
plt.connect('button_press_event', lambda event: plt.gca().set_autoscale_on(False))
plt.connect('scroll_event', lambda event: plt.gca().set_autoscale_on(False))

# Show the plot
plt.show()
