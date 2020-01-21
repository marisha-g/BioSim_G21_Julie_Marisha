# -*- coding: utf-8 -*-

"""
This is a small demo script running a BioSim simulation
with all default values.
Also makes an mp4 movie of the simulation stored in the figs directory.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import matplotlib.pyplot as plt
import os

from biosim.rossumoya import Rossumoya
from biosim.simulation import BioSim

if __name__ == '__main__':
    image_base = os.path.join('.', r'figs\bio')
    sim = BioSim(ini_pop=Rossumoya.default_ini_herbs,
                 ymax_animals=10000,
                 cmax_animals={'Herbivore': 100, 'Carnivore': 50},
                 img_base=image_base,)
    sim.simulate(num_years=10, vis_years=1, img_years=1)
    sim.add_population(Rossumoya.default_ini_carns)
    sim.simulate(num_years=30, vis_years=1, img_years=1)
    plt.show()
    sim.make_movie()
