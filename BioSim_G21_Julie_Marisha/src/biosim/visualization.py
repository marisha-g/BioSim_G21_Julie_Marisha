# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import matplotlib.pyplot as plt
import numpy as np
import os

from biosim.simulation import BioSim

_DEFAULT_MOVIE_FORMAT = 'mp4'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'figs')
_DEFAULT_IMAGE_BASE = 'bio'
_DEFAULT_IMAGE_FORMAT = "png"
_DEFAULT_MOVIE_FORMAT = 'mp4'  # alternatives: mp4, gif


class BioVis:
    """Provides user interface for simulation, including visualization."""

    def __init__(self,
                 island_map=None,
                 ini_pop=None,
                 seed=None,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=None,
                 img_fmt=None):
        """
        """
        if img_base is None:
            img_base = _DEFAULT_IMAGE_BASE

        if img_fmt is None:
            img_fmt = _DEFAULT_IMAGE_FORMAT

        self.sim = BioSim(island_map=island_map,
                          ini_pop=ini_pop,
                          seed=seed,
                          ymax_animals=ymax_animals,
                          cmax_animals=cmax_animals,
                          img_base=img_base,
                          img_fmt=img_fmt)


