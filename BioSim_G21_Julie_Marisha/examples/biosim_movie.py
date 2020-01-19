# -*- coding: utf-8 -*-

"""
This is a small demo script running a BioSim simulation and generating a movie.
"""
__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import os

from biosim.simulation import BioSim

img_base = os.path.join('../figs', 'bio')

sim = BioSim(img_base=img_base)
sim.simulate(10, 1, 5)
sim.make_movie('mp4')
