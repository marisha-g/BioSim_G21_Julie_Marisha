# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'


class Cell:
    """
    Cell class description.
    """

    def __init__(self):
        self.fodder_in_cell = None
        self.f_max = None
        self.location = None
        self.population = None

    def fodder_first_year(self, f_max):
        """
        Sets max fodder in Savannah and Jungle cells.
        """
        self.fodder_in_cell = f_max


class Savannah(Cell):
    @classmethod
    def set_parameters(cls, f_max=None, alpha=None):
        if f_max is None:
            f_max = 300.0
        if alpha is None:
            alpha = 0.3

        if f_max < 0:
            raise ValueError('f_max can not be negative.')
        if alpha < 0:
            raise ValueError('alpha can not be negative.')

        cls.f_max = f_max
        cls.alpha = alpha

    def __init__(self):
        super().__init__()

    def regrow_fodder(self):
        self.fodder_in_cell = self.fodder_in_cell + self.alpha * (self.f_max - self.fodder_in_cell)


class Jungle(Cell):

    @classmethod
    def set_parameters(cls, f_max=None):
        if f_max is None:
            f_max = 800.0
        if f_max <= 0:
            raise ValueError('f_max must be a positive number')
        cls.f_max = f_max

    def __init__(self):
        super().__init__()

    def regrow_fodder(self):
        self.fodder_in_cell = self.f_max


class Desert(Cell):
    def __init__(self):
        super().__init__()
        self.fodder_in_cell = 0


class MountainAndOcean(Cell):
    def __init__(self):
        super().__init__()
        self.fodder_in_cell = 0
