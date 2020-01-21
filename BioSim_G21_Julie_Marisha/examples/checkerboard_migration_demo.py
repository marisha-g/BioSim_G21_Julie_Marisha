# -*- coding: utf-8 -*-

"""
:mod: `BioSim_G21_Julie_Marisha.checkerboard_migration_demo` is a small demo
       script running a BioSim simulation that demonstrates the behaviour of
       the animals when the probability to migrate is set to 1.

The user can define:
    *   Rossumøya's geography
    *   The number of each species that are put on every defined coordinate
    *   The coordinates that the animals in that species should occupy
    *   Number of years to simulate

"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import matplotlib.pyplot as plt
from biosim.animal import Herbivore, Carnivore
from biosim.simulation import BioSim


if __name__ == '__main__':
    island_map = \
        "OOOOOOO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOJJJJJO\nOOOOOOO"

    ini_herbs = [
        {
            "loc": (3, 3),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (3, 3),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(70)
            ],
        }
    ]
    Herbivore.prob_migration = 1
    Carnivore.prob_migration = 1
    sim = BioSim(island_map=island_map,
                 ini_pop=ini_herbs,
                 ymax_animals=1000,
                 cmax_animals={'Herbivore': 20, 'Carnivore': 20})
    sim.add_population(ini_carns)
    sim.simulate(num_years=25)
    plt.show()
