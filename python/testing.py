import matplotlib.pylab as plt
import numpy as np

#x = np.linspace(-np.pi, np.pi, 10)
#plt.plot(x, np.sin(x))
#plt.xlabel('Angle [rad]')
#plt.ylabel('sin(x)')
#plt.axis('tight')
#plt.show()

def sin_static():
    # raw
    x = np.linspace(-np.pi, np.pi, 252)
    y = np.sin(x) * 4
    # discretize y axis
    y_disc = y.astype(int)   
    return y_disc

y = sin_static()
x = np.linspace(-np.pi, np.pi, 252)
plt.plot(x, y)
plt.xlabel('Angle [rad]')
plt.ylabel('sin(x)')
plt.axis('tight')
plt.show()

