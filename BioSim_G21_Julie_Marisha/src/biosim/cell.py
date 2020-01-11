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

    def __init__(self, herbivores=None, carnivores=None):
        self.fodder_in_cell = None
        self.animal_can_enter = True

        if herbivores is None:
            self.herbivores = []
        if carnivores is None:
            self.carnivores = []

    def fodder_first_year(self, f_max):
        """
        Sets max fodder in Savannah and Jungle cells.
        """
        self.fodder_in_cell = f_max

    def abundance_of_fodder(self):
        rel_abundance_of_fodder = self.fodder_in_cell
        pass

    def propensity_migration(self):
        pass

    @property
    def total_population(self):
        tot_pop = len(self.herbivores) + len(self.carnivores)
        return tot_pop

    @property
    def total_herbivores(self):
        tot_herb = len(self.herbivores)
        return tot_herb

    @property
    def total_carnivores(self):
        tot_carn = len(self.carnivores)
        return tot_carn


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
        self.fodder_in_cell = self.fodder_in_cell + \
                              self.alpha * (self.f_max - self.fodder_in_cell)


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
        self.f_max = 0


class MountainAndOcean(Cell):
    def __init__(self):
        super().__init__()
        self.fodder_in_cell = 0
        self.f_max = 0
        self.animal_can_enter = False
