# -*- coding: utf-8 -*-

"""
This is a small demo script running a BioSim simulation and generating a movie.
"""
__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import os

from biosim.simulation import BioSim

DEFAULT_IMAGE_BASE = r'C:\Users\be15069901\Documents\NMBU Data 2019-2020\INF200\biosim_project\BioSim_G21_Julie_MarishaBioSim_G21_Julie_Marisha\src\figs\bio'


sim = BioSim(ymax_animals=300,
             cmax_animals={'Herbivore': 20, 'Carnivore': 20},
             img_base=DEFAULT_IMAGE_BASE)
sim.simulate(10, 1, 1)
sim.make_movie('mp4')
