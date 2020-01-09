# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import textwrap


class Landscape:

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

    def __init__(self, geogr=None, f_sav_max=None, f_jungle_max=None, alpha=None):
        if geogr is None:
            self.geogr = Landscape.default_geogr

        if f_sav_max is None:
            self.f_sav_max = 300.0

        if f_jungle_max is None:
            self.f_jungle_max = 800.0

        if alpha is None:
            self.alpha = 0.3

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
                geography_map[(i_index+1, j_index+1)] = [cell, None]

        return geography_map

    def fodder_first_year(self):
        """
        Sets max fodder in Savannah and Jungle cells.
        """
        for cell in self.geography_map:
            if self.geography_map[cell][0] == "S":
                self.geography_map[cell][1] = self.f_sav_max
            if self.geography_map[cell][0] == "J":
                self.geography_map[cell][1] = self.f_jungle_max

    def regrowth_fodder(self):
        """
        Updating fodder in Savannah and Jungle cells at the beginning
        of a new cycle.
        """
        for cell in self.geography_map:
            if self.geography_map[cell][0] == "S":
                current_fodder = self.geography_map[cell][1]
                self.geography_map[cell][1] = current_fodder + self.alpha * (self.f_sav_max - current_fodder)

            if self.geography_map[cell][0] == "J":
                self.geography_map[cell][1] = self.f_jungle_max
