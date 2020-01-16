# -*- coding: utf-8 -*-

"""
This is a small demo script running a BioSim simulation.
"""

__author__ = "Hans E Plesser / NMBU"

import matplotlib.pyplot as plt
from biosim.simulation import BioSim

if __name__ == '__main__':

    sim = BioSim(seed=12345)
    sim.simulate(50, 1, 5)

    input('Press ENTER to simulate some more!')

    sim.simulate(100, 1, 5)

    print('Close the figure to end the program!')

    plt.show()