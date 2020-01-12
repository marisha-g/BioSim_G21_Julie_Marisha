# -*- coding: utf-8 -*-

"""
"""
from BioSim_G21_Julie_Marisha.src.biosim.animal import Carnivore, Herbivore
import math

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

    def __init__(self, animals=None):
        self.fodder_in_cell = None
        self.animal_can_enter = True

        if animals is None:
            self.animals = []

    def fodder_first_year(self, f_max):
        """
        Sets max fodder in Savannah and Jungle cells.
        """
        self.fodder_in_cell = f_max

    @property
    def abundance_of_fodder_herbivores(self):
        rel_abundance_of_fodder = self.fodder_in_cell /\
                                  (self.total_herbivores + 1) * Herbivore.F
        return rel_abundance_of_fodder

    @property
    def abundance_of_fodder_carnivores(self):
        weight_of_herbs = 0
        for animal in self.animals:
            if type(animal).__name__ == 'Herbivore':
                weight_of_herbs += animal.weight

        rel_abundance_of_fodder = weight_of_herbs /\
                                  (self.total_carnivores + 1) * Carnivore.F
        return rel_abundance_of_fodder

    @property
    def propensity_migration_herb(self):
        return math.exp(Herbivore.lambda_ * self.abundance_of_fodder_herbivores)

    @property
    def propensity_migration_carn(self):
        return math.exp(Carnivore.lambda_ * self.abundance_of_fodder_carnivores)

    @property
    def total_population(self):
        return len(self.animals)


    @property
    def total_herbivores(self):
        return self.animals.count(Herbivore)

    @property
    def total_carnivores(self):
        return self.animals.count(Carnivore)


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

    def propensity_migration(self):
        return 0
