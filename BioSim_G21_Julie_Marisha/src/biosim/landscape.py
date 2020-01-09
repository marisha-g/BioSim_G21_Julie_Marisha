# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import textwrap


class Landscape:
    """
    Landscape class description.
    """

    default_geogr = """\
                  OOOOOOOOOOOOOOOOOOOOO
                  OOOOOOOOSMMMMJJJJJJJO
                  OSSSSSJJJJMMJJJJJJJOO
                  OSSSSSSSSSMMJJJJJJOOO
                  OSSSSSJJJJJJJJJJJJOOO
                  OSSSSSJJJDDJJJSJJJOOO
                  OSSJJJJJDDDJJJSSSSOOO
                  OOSSSSJJJDDJJJSOOOOOO
                  OSSSJJJJJDDJJJJJJJOOO
                  OSSSSJJJJDDJJJJOOOOOO
                  OOSSSSJJJJJJJJOOOOOOO
                  OOOSSSSJJJJJJJOOOOOOO
                  OOOOOOOOOOOOOOOOOOOOO"""
    default_geogr = textwrap.dedent(default_geogr)

    def __init__(self, geogr=None):
        self.fodder_in_cell = None

        if geogr is None:
            self.geogr = Landscape.default_geogr

        self.geography_map = self.make_geography_coordinates()

    def make_geography_coordinates(self):
        """
        Making a dictionary with coordinates as keys and lists with cell
        types "O, M, S, J, D" and fodder in cell as values.

        :return: dict
        """
        geogr_list = self.geogr.split('\n')
        geography_map = {}
        for i_index, line in enumerate(geogr_list):
            for j_index, cell in enumerate(line):
                geography_map[(i_index+1, j_index+1)] = cell

        return geography_map

    def fodder_first_year(self, f_max):
        """
        Sets max fodder in Savannah and Jungle cells.
        """
        self.fodder_in_cell = f_max


class Savannah(Landscape):
    def __init__(self, f_sav_max=None, alpha=None):
        super().__init__(f_sav_max)
        if f_sav_max is None:
            self.f_sav_max = 300.0
        if alpha is None:
            self.alpha = 0.3

    def set_initial_fodder(self):
        super().fodder_first_year(self.f_sav_max)
    
    def regrow_fodder(self):
        self.fodder_in_cell = self.fodder_in_cell + self.alpha*(self.f_sav_max - self.fodder_in_cell)


class Jungle(Landscape):
    def __init__(self, f_jungle_max=None):
        super().__init__(f_jungle_max)
        if f_jungle_max is None:
            self.f_jungle_max = 800.0

    def set_initial_fodder(self):
        super().fodder_first_year(self.f_jungle_max)

    def regrow_fodder(self):
        self.fodder_in_cell = self.f_jungle_max


class Desert(Landscape):
    def __init__(self):
        super().__init__()
        self.fodder_in_cell = 0


class MountainAndOcean:
    def __init__(self):
        super().__init__()
        self.fodder_in_cell = 0



