# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'


class Cell:
    """
    Cell class description.
    """
    @classmethod
    def set_parameters(cls, f_max):

        if f_max < 0:
            raise ValueError('f_max must be a positive number')
        cls.f_max = f_max

    def __init__(self):
        self.fodder_in_cell = None
        self.population = None
        self.animals = None

    def fodder_first_year(self, f_max):
        """
        Sets max fodder in Savannah and Jungle cells.
        """
        self.fodder_in_cell = f_max

    def abundance_of_fodder(self):
        rel_abundance_of_fodder =  self.fodder_in_cell /
    def propensity_migration(self, ):




class Savannah(Cell):
    @classmethod
    def set_parameters(cls, f_max=300.0, alpha=0.3):

        super(Savannah, cls).set_parameters(f_max)
        if alpha is None:
            alpha = 0.3
        if alpha < 0:
            raise ValueError('alpha can not be negative.')

        cls.alpha = alpha

    def __init__(self):
        super().__init__()

    def regrow_fodder(self):
        self.fodder_in_cell = self.fodder_in_cell + self.alpha * (self.f_max - self.fodder_in_cell)


class Jungle(Cell):

    @classmethod
    def set_parameters(cls, f_max=800.0):

        super(Jungle, cls).set_parameters(f_max)

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
