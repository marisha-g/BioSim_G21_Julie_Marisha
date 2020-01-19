# -*- coding: utf-8 -*-

"""
This is a small demo script running a BioSim simulation and generating a movie.
"""

__author__ = ""

import os

from biosim.simulation import BioSim
DEFAULT_GRAPHICS_DIR = os.path.join('..', 'figs')
DEFAULT_IMAGE_NAME = 'bio'
img_base = os.path.join(DEFAULT_GRAPHICS_DIR, DEFAULT_IMAGE_NAME)

sim = BioSim(img_base=img_base)
sim.simulate(10, 1, 5)
sim.make_movie('mp4')
