# Module to plot a vector 

import matplotlib.pyplot as plt
import numpy as np

def plot(solu, delta, save_to_file=False, x_min=0.0, x_max=1.0):

        x = y = np.arange(x_min, x_max, delta)
        X, Y = np.meshgrid(x, y)

        fig = plt.figure(figsize=(20, 20))
        fig.suptitle("Simulation results")

        ax = fig.add_subplot(2, 2, 1, projection='3d')

        ax.plot_surface(X, Y, solu, cmap='viridis', edgecolor='none')
        ax.set_title('Surface plot u(x,y)')
        ax.set_ylabel('y coordinate')
        ax.set_xlabel('x coordinate')

        ax = fig.add_subplot(2, 2, 2)
        ax.set_title('2D projection of u(x,y)')
        ax.set_ylabel('j node number')
        ax.set_xlabel('i node number')
        plt.imshow(solu, cmap='hot')
        plt.colorbar()

        ax = fig.add_subplot(2, 2, 3)
        ax.set_title('Fake test vector plot of (u(x,y), u(x,y)')
        ax.set_ylabel('y coordinate')
        ax.set_xlabel('x coordinate')
        plt.quiver(X, Y, solu, solu)

        ax = fig.add_subplot(2, 2, 4)
        ax.set_title('Contour lines for u(x,y)')
        ax.set_ylabel('y coordinate')
        ax.set_xlabel('x coordinate')
        plt.contour(X, Y, solu)

        if (save_to_file):
            print ("Saving to file")
            plt.savefig('static/plot.png')
        else:        
            plt.show()
