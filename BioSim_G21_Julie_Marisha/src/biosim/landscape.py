# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import textwrap


class Landscape:
    def __init__(self, geogr):
        self.geography_map = None

    def make_geography_coordinates(self, geogr):
        geogr_list = geogr.split('\n')
        self.geography_map = {}
        for i_index, line in enumerate(geogr_list):
            for j_index, cell in enumerate(line):
                self.geography_map[(i_index+1, j_index+1)] = cell

        return self.geography_map



if __name__ == '__main__':
