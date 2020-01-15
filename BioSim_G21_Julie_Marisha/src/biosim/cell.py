# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from biosim.animal import Carnivore, Herbivore
import numpy as np


class BaseCell:
    """
    Superclass for cell in BioSim.
    """

    @classmethod
    def set_parameters(cls, f_max=None):
        """
        Set default parameters for class Cell.
        :param f_max: maximum fodder available in a cell type
        :type: float
        """
        if f_max is None:
            f_max = 0

        if f_max < 0:
            raise ValueError('f_max must be a positive number')
        cls.f_max = f_max

    def __init__(self, animals=None):
        """
        Constructor that initiate class Cell.
        :param animals: list of all the animals in a cell
        :type: list
        """
        self._fodder_in_cell = None
        self.animal_can_enter = True

        if animals is None:
            animals = []
        self.animals = animals

        self.set_parameters()
        self.fodder_first_year(self.f_max)

    def fodder_first_year(self, f_max):
        """
        Sets max fodder in Savannah and Jungle cells.
        :param f_max: maximum fodder available in a cell type
        :type: float
        """
        self.fodder_in_cell = f_max

    def regrow_fodder(self):
        """
        Grow back initial fodder amount.
        """
        self.fodder_in_cell = self.f_max

    def add_population(self, pop_list):
        for pop_dict in pop_list:
            species = pop_dict['species']
            age = pop_dict['age']
            weight = pop_dict['weight']
            if species == 'Herbivore':
                self.animals.append(
                    Herbivore(age, weight)
                )
            if species == 'Carnivore':
                self.animals.append(
                    Carnivore(age, weight)
                )

    def herbivores_eat(self):
        """
        Herbivore with the highest fitness eat first. The Herbivore's weight
        increases with the amount of fodder it has eaten.
        """
        if self.fodder_in_cell != 0:
            for herbivore in self.list_of_sorted_herbivores:
                if self.fodder_in_cell >= herbivore.F:
                    food = Herbivore.F
                    self.fodder_in_cell -= food
                    herbivore.weight_gain(food)
                else:
                    herbivore.weight_gain(self.fodder_in_cell)
                    self.fodder_in_cell = 0

    def carnivores_eat(self):
        """
        Carnivore with the highest fitness eat first. The Carnivore tries to
        kill the Herbivore with lowest fitness first. The increase in weight
        of the Carnivore is proportional to the weight of the Herbivore killed.
        """
        for carnivore in self.list_of_sorted_carnivores:
            killed_herbivores = []
            for herbivore in reversed(self.list_of_sorted_herbivores):
                if carnivore.prob_carnivore_kill(herbivore.fitness):
                    killed_herbivores.append(herbivore)
                    weight_prey = herbivore.weight
                    carnivore.weight_gain(weight_prey)
            self.remove_dead_animals(killed_herbivores)

    def remove_migrated_animal(self, gone_animals):
        """
        Removes animal that has migrated.
        :param gone_animal: list of animals that has migrated
        :type: list
        """
        for gone_animal in gone_animals:
            self.animals.remove(gone_animal)

    def remove_dead_animals(self, dead_animals):
        """
        Removes animal that has died.
        :param dead_animals: list of animals that has died
        :type: list
        """
        for dead_animal in dead_animals:
            self.animals.remove(dead_animal)

    @property
    def list_of_sorted_herbivores(self):
        """
        List of sorted Herbivores. Herbivore with highest fitness is first.
        :return: sorted_herbivores
        :type: list
        """
        list_of_herbivores = [animal for animal in self.animals
                              if isinstance(animal, Herbivore)]
        sorted_herbivores = sorted(list_of_herbivores,
                                   key=lambda x: x.fitness)
        return sorted_herbivores

    @property
    def list_of_sorted_carnivores(self):
        """
        List of sorted Carnivores. Carnivore with highest fitness is first.
        :return: sorted_carnivores
        :type: list
        """
        list_of_carnivores = [animal for animal in self.animals
                              if isinstance(animal, Carnivore)]
        sorted_carnivores = sorted(list_of_carnivores,
                                   key=lambda x: x.fitness)
        return sorted_carnivores

    @property
    def fodder_in_cell(self):
        """
        Fodder available in cell.
        :return: self._fodder_in_cell
        :type: float
        """
        return self._fodder_in_cell

    @fodder_in_cell.setter
    def fodder_in_cell(self, value):
        """
        Set the amount of fodder in cell. Setting this to a
        new value will reconfigure the cell automatically.
        :param value: new value
        :type: float
        """
        self._fodder_in_cell = value

    @property
    def abundance_of_fodder_herbivores(self):
        """
        Calculates the relative abundance of fodder for Herbivores.
        :return: rel_abundance_of_fodder
        :type: float
        """
        rel_abundance_of_fodder = self.fodder_in_cell / ((
                self.total_herbivores + 1
        ) * Herbivore.F)

        return rel_abundance_of_fodder

    @property
    def abundance_of_fodder_carnivores(self):
        """
        Calculates the relative abundance of fodder for Carnivores.
        :return: rel_abundance_of_fodder
        :type: float
        """
        weight_of_herbs = 0
        for animal in self.animals:
            if type(animal).__name__ == 'Herbivore':
                weight_of_herbs += animal.weight

        rel_abundance_of_fodder = weight_of_herbs / ((
                self.total_carnivores + 1
        ) * Carnivore.F)

        return rel_abundance_of_fodder

    @property
    def propensity_migration_herb(self):
        """
        Calculates the propensity for a Herbivore to move from one cell
        to another.
        :return: formula for calculating propensity
        :type: float
        """
        return np.exp(Herbivore.lambda_ * self.abundance_of_fodder_herbivores)

    @property
    def propensity_migration_carn(self):
        """
        Calculates the propensity for a Carnivore to move from one cell
        to another.
        :return: formula for calculating propensity
        :type: float
        """
        return np.exp(Carnivore.lambda_ * self.abundance_of_fodder_carnivores)

    @property
    def total_population(self):
        """
        Returns the total amount of animals on Rossumøya.
        :return: length of the Animal list
        :type: int
        """
        return len(self.animals)

    @property
    def total_herbivores(self):
        """
        :returns: the total amount of Herbivores on Rossumøya.
        :type: int
        """
        return len([animal for animal in self.animals if isinstance(animal, Herbivore)])

    @property
    def total_carnivores(self):
        """
        :returns: the total amount of Carnivores on Rossumøya.
        :type: int
        """
        return len([animal for animal in self.animals if isinstance(animal, Carnivore)])


class Savannah(BaseCell):
    """
    Class instance of class Cell for the cell type Savannah.
    """

    @classmethod
    def set_parameters(cls, f_max=300.0, alpha=0.3):
        """
        Set default parameters for class instance Savannah.
        :param f_max: maximum fodder available in cell type Savannah
        :type: float
        :param alpha: constant
        :type: float
        """
        super(Savannah, cls).set_parameters(f_max)
        if alpha is None:
            alpha = 0.3
        if alpha < 0:
            raise ValueError('alpha can not be negative.')

        cls.alpha = alpha

    def __init__(self):
        """
        Constructor that initiate class instance Savannah.
        """
        super().__init__()

    def regrow_fodder(self):
        """
        Calculates regrowth of fodder in cell type Savannah.
        """
        self.fodder_in_cell = self.fodder_in_cell + self.alpha * (
                self.f_max - self.fodder_in_cell
        )


class Jungle(BaseCell):
    """
    Class instance of class Cell for the cell type Jungle.
    """

    @classmethod
    def set_parameters(cls, f_max=800.0):
        """
        Set default parameters for class instance Jungle.
        :param f_max: maximum fodder available in cell type Jungle
        :type: float
        """
        super(Jungle, cls).set_parameters(f_max)

    def __init__(self):
        """
        Constructor that initiate class instance Jungle.
        """
        super().__init__()


class Desert(BaseCell):
    """
    Class instance of class Cell for the cell type Desert.
    """
    @classmethod
    def set_parameters(cls, f_max=None):
        """
        Set default parameters for class instance Desert.
        :param f_max: maximum fodder available in cell type Desert
        :type: float
        """
        super(Desert, cls).set_parameters(f_max)

    def __init__(self):
        """
        Constructor that initiate class instance Desert.
        """
        super().__init__()
        self.fodder_in_cell = 0


class Mountain(BaseCell):
    """
    Class instance of class Cell for the cell types Mountain.
    """
    @classmethod
    def set_parameters(cls, f_max=0):
        """
        Set default parameters for class instance Mountain.
        :param f_max: maximum fodder available in cell type Mountain
        :type: float
        """
        super(Mountain, cls).set_parameters(f_max)

    def __init__(self):
        """
        Constructor that initiate class instance Mountain.
        """
        super().__init__()
        self.fodder_in_cell = 0
        self.animal_can_enter = False

    @property
    def propensity_migration_herb(self):
        """
        Sets the propensity for a Herbivore to migrate to zero,
        because Mountain cells are impassable.
        :return: 0
        :type: int
        """
        return 0

    @property
    def propensity_migration_carn(self):
        """
        Sets the propensity for a Carnivore to migrate to zero,
        because Mountain cells are impassable.
        :return: 0
        :type: int
        """
        return 0


class Ocean(BaseCell):
    """
    Class instance of class Cell for the cell type Ocean.
    """
    @classmethod
    def set_parameters(cls, f_max=0):
        """
        Set default parameters for class instance Ocean.
        :param f_max: maximum fodder available in cell type Ocean
        :type: float
        """
        super(Ocean, cls).set_parameters(f_max)

    def __init__(self):
        """
        Constructor that initiate class instance Ocean.
        """
        super().__init__()
        self.fodder_in_cell = 0
        self.animal_can_enter = False

    @property
    def propensity_migration_herb(self):
        """
        Sets the propensity for a Herbivore to migrate to zero,
        because Ocean cells are impassable.
        :return: 0
        :type: int
        """
        return 0

    @property
    def propensity_migration_carn(self):
        """
        Sets the propensity for a Carnivore to migrate to zero,
        because Ocean cells are impassable.
        :return: 0
        :type: int
        """
        return 0