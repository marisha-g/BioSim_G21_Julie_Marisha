# -*- coding: utf-8 -*-

"""
:mod: `biosim.cell` provides the user with the information stored
        in the different landscape cells at Rossumøya.

Rossumøya is divided into squares (or cells), where each square has its own
location and is of one of the following five geography types:
ocean, jungle, savannah, desert or mountain. The superclass and subclasses
in this script holds all the information that
are stored in all the landscape cells.

This file can be imported as a module and contains the following
classes:

    *   BaseCell - Superclass with the basic characteristics that all of
        the cell types in Rossumøya has in common.

    *   Savannah(BaseCell) - Subclass of BaseCell with characteristics for
        the cell type Savannah.

    *   Jungle(BaseCell) - Subclass of BaseCell with characteristics for
        the cell type Jungle.

    *   Desert(BaseCell) - Subclass of BaseCell with characteristics for
        the cell type Desert.

    *   Mountain(BaseCell) - Subclass of BaseCell with characteristics for
        the cell type Mountain.

    *   Ocean(BaseCell) - Subclass of BaseCell with characteristics for
        the cell type Ocean.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

from .animal import Carnivore, Herbivore
import math


class BaseCell:
    """Superclass for cell in BioSim."""

    @classmethod
    def set_parameters(cls, f_max=None):
        """
        Set default parameters for class Cell.

        :param f_max: Maximum fodder available in a cell
        :type f_max: float
        """
        if f_max is None:
            f_max = 0

        if f_max < 0:
            raise ValueError('f_max must be a positive number')
        cls.f_max = f_max

    def __init__(self):
        """
        Constructor that initiates class Cell.
        """
        self._fodder_in_cell = None
        self.animal_can_enter = True
        self._propensity_migration_carn = None
        self._propensity_migration_herb = None

        self.propensity_carn_calculated = False
        self.propensity_herb_calculated = False

        self.animals = []

        self.set_parameters()
        self.fodder_first_year(self.f_max)

    def add_population(self, pop_list):
        """
        Adds new animals in cell.

        :param pop_list: list of dictionaries indicating population.
        :type pop_list: list
        """
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

    @property
    def total_population(self):
        """
        Total number of animals in the cell.

        :type: int
        """
        return len(self.animals)

    @property
    def total_herbivores(self):
        """
        The total number of Herbivores in the cell.

        :type: int
        """
        total_herbivores = 0
        for animal in self.animals:
            if type(animal).__name__ == 'Herbivore':
                total_herbivores += 1

        return total_herbivores

    @property
    def total_carnivores(self):
        """
        The total number of Carnivores in the cell.

        :type: int
        """
        total_carnivores = 0
        for animal in self.animals:
            if type(animal).__name__ == 'Carnivore':
                total_carnivores += 1

        return total_carnivores

    @property
    def fodder_in_cell(self):
        """
        Fodder available in cell.

            :setter: Sets the amount of fodder.
            :type: float
        """
        return self._fodder_in_cell

    @fodder_in_cell.setter
    def fodder_in_cell(self, value):
        """
        Set the amount of fodder in cell. Setting this to a
        new value will reconfigure the cell automatically.
        """
        self._fodder_in_cell = value

    @property
    def abundance_of_fodder_herbivores(self):
        r"""
        Calculates the relative abundance of fodder for Herbivores according
        to the formula below.

        .. math::
            \begin{equation}
            \epsilon_k = \frac{f_k}{(n_k + 1)F'}
            \end{equation}

        .. math::
            \begin{equation}
            \mbox { where } F_k \mbox
            { is the amount of relevant fodder available in cell } k, \\ n_k
            \mbox { is the number of animals of the same species in cell } \\
            k \mbox { and } F' \mbox { is the "appetite" of the species.}
            \end{equation}


        :type: float
        """
        rel_abundance_of_fodder = self.fodder_in_cell / (
                (self.total_herbivores + 1) * Herbivore.F
        )

        return rel_abundance_of_fodder

    @property
    def abundance_of_fodder_carnivores(self):
        r"""
        Calculates the relative abundance of fodder for Carnivores according
        to the formula below.

        .. math::
            \begin{equation}
            \epsilon_k = \frac{f_k}{(n_k + 1)F'}
            \end{equation}

        .. math::
            \begin{equation}
            \mbox { where } F_k \mbox
            { is the amount of relevant fodder available in cell } k, \\ n_k
            \mbox { is the number of animals of the same species in cell } \\
            k \mbox { and } F' \mbox { is the "appetite" of the species.}
            \end{equation}

        :type: float
        """
        weight_of_herbs = 0
        for animal in self.animals:
            if type(animal).__name__ == 'Herbivore':
                weight_of_herbs += animal.weight

        rel_abundance_of_fodder = weight_of_herbs / (
                (self.total_carnivores + 1) * Carnivore.F
        )

        return rel_abundance_of_fodder

    def fodder_first_year(self, f_max):
        """
        Sets maximum fodder for Savannah and Jungle cells.

        :param f_max: maximum fodder available in a cell type
        :type f_max: float
        """
        self.fodder_in_cell = f_max

    def regrow_fodder(self):
        """
        Grow back initial fodder amount.
        """
        self.fodder_in_cell = self.f_max
        self.propensity_herb_calculated = False

    def animals_age_and_lose_weight(self):
        """
        Once a year all animals age and lose weight.
        """
        for animal in self.animals:
            animal.aging()
            animal.weight_loss()

    @property
    def list_of_sorted_herbivores_by_fitness(self):
        """
        Sorts all Herbivores by fitness in descending order if there
        are more than one Herbivore in the cell.

            :type: list
        """
        list_of_herbivores = []
        for animal in self.animals:
            if type(animal).__name__ == 'Herbivore':
                list_of_herbivores.append(animal)

        if len(list_of_herbivores) > 1:
            sorted_herbivores = sorted(list_of_herbivores,
                                       key=lambda x: x.fitness,
                                       reverse=True)
            return sorted_herbivores
        else:
            return list_of_herbivores

    @property
    def list_of_sorted_carnivores_by_fitness(self):
        """
        Sorts all Carnivores by fitness in descending order if there
        are more than one Carnivore in the cell.

            :type: list
        """
        list_of_carnivores = []
        for animal in self.animals:
            if type(animal).__name__ == 'Carnivore':
                list_of_carnivores.append(animal)

        if len(list_of_carnivores) > 1:
            sorted_carnivores = sorted(list_of_carnivores,
                                       key=lambda x: x.fitness,
                                       reverse=True)
            return sorted_carnivores
        else:
            return list_of_carnivores

    def herbivores_eat(self):
        """
        Herbivores eat in order of highest fitness. The Herbivore's weight
        increases.
        """
        if self.fodder_in_cell != 0:
            for herbivore in self.list_of_sorted_herbivores_by_fitness:
                if self.fodder_in_cell >= herbivore.F:
                    food = Herbivore.F
                    self.fodder_in_cell -= food
                    herbivore.weight_gain(food)
                else:
                    herbivore.weight_gain(self.fodder_in_cell)
                    self.fodder_in_cell = 0

    def carnivores_eat(self):
        """
        Carnivores eat in order of highest fitness. The Carnivore tries to
        kill the Herbivore with lowest fitness first. The Carnivore's weight
        increases.
        """
        for carnivore in self.list_of_sorted_carnivores_by_fitness:
            food_eaten = 0
            killed_herbivores = []
            for herbivore in list(
                    reversed(self.list_of_sorted_herbivores_by_fitness)
            ):
                if food_eaten < carnivore.F:
                    if carnivore.prob_carnivore_kill(herbivore.fitness):
                        killed_herbivores.append(herbivore)
                        weight_prey = herbivore.weight
                        if food_eaten + weight_prey > carnivore.F:
                            food_eaten = carnivore.F
                        else:
                            food_eaten += weight_prey
            carnivore.weight_gain(food_eaten)
            self.remove_animals(killed_herbivores)

    def herb_procreation(self):
        """
        Herbivores at the start of the breeding season procreate if the
        `prob_procreation` method returns 1.
        """
        total_herbs_at_start_of_breeding_season = self.total_herbivores
        for animal in self.animals:
            species = type(animal).__name__

            if species == 'Herbivore':
                animal_gives_birth = animal.prob_procreation(
                    total_herbs_at_start_of_breeding_season
                )
                if animal_gives_birth:
                    self.add_offspring(animal)

    def carn_procreation(self):
        """
        Carnivores at the start of the breeding season procreate if the
        `prob_procreation` method returns 1.
        """
        total_carns_at_start_of_breeding_season = self.total_carnivores
        for animal in self.animals:
            species = type(animal).__name__

            if species == 'Carnivore':
                animal_gives_birth = animal.prob_procreation(
                    total_carns_at_start_of_breeding_season
                )
                if animal_gives_birth:
                    self.add_offspring(animal)

    def add_offspring(self, animal):
        """
        Adds offspring to the cell, and decrease weight of the
        mother.

        :param animal: Mother who gives birth
        :type animal: type
        """
        weight = animal.draw_birth_weight()
        if weight * animal.xi < animal.weight:
            offspring = [
                {'species': type(animal).__name__,
                 'age': 0,
                 'weight': weight}
            ]
            self.add_population(offspring)
            animal.weight_loss_birth(weight)

    def find_migrating_animals(self):
        """
        Makes a list of the animals who wants to migrate out of the cell.

        :return: migrating_animals
        :rtype: list
        """
        migrating_animals = []
        for animal in self.animals:
            if animal.prob_migration and not animal.has_migrated:
                migrating_animals.append(animal)
                animal.has_migrated = True
        return migrating_animals

    def reset_migration(self):
        """
        Resets the `has_migrated` attribute to False
        for all animals in the cell.
        """
        for animal in self.animals:
            animal.has_migrated = False

    @property
    def propensity_migration_herb(self):
        r"""
        Calculates the propensity for a Herbivore to move from
        :math:`i \mbox { to } j \in C^{(i)}` according to the formula
        given below.

        .. math::
            \begin{equation}
            \pi_{i \rightarrow j} =
            \begin{cases}
            0 & \mbox { if j is Mountain or Ocean} \\
           e^{\lambda \epsilon_j} & \mbox { otherwise }
            \end{cases} \quad
            \end{equation}

        :type: float
        """
        if self.propensity_herb_calculated:
            return self._propensity_migration_herb
        else:
            self._propensity_migration_herb = math.exp(
                Herbivore.lambda_ * self.abundance_of_fodder_herbivores
            )
            self.propensity_herb_calculated = True
            return self._propensity_migration_herb

    @property
    def propensity_migration_carn(self):
        r"""
        Calculates the propensity for a Carnivore to move from
        :math:`i \mbox { to } j \in C^{(i)}` according to the formula
        given below.

        .. math::
            \begin{equation}
            \pi_{i \rightarrow j} =
            \begin{cases}
            0 & \mbox { if j is Mountain or Ocean} \\
            e^{\lambda \epsilon_j} & \mbox { otherwise }
            \end{cases} \quad
            \end{equation}

        :type: float
        """
        if self.propensity_carn_calculated:
            return self._propensity_migration_carn
        else:
            self._propensity_migration_carn = math.exp(
                Carnivore.lambda_ * self.abundance_of_fodder_carnivores
            )
            self.propensity_carn_calculated = True

            return self._propensity_migration_carn

    def remove_animals(self, gone_animals):
        """
        Removes animal that has migrated.

        :param gone_animals: list of animals that has migrated
        :type gone_animals: list
        """
        for gone_animal in gone_animals:
            self.animals.remove(gone_animal)

    def add_animals(self, new_animals):
        """
        Adds new animals to the animals list.

        :param new_animals: List of new animals
        :type new_animals: list
        """
        for new_animal in new_animals:
            self.animals.append(new_animal)


class Savannah(BaseCell):
    """Class instance of class Cell for the cell type Savannah."""

    @classmethod
    def set_parameters(cls, f_max=None, alpha=None):
        """
        Set default parameters for class instance Savannah.

        :param f_max: Maximum fodder available in cell type Savannah
        :type f_max: float
        :param alpha: Constant
        :type alpha: float
        """
        if f_max is None:
            f_max = 300.0

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
        r"""
        Calculates regrowth of fodder in cell type Savannah by using the
        formula below.

        .. math::
            f_{ij} \leftarrow f_{ij} + \alpha \times (f^{Sav}_{max} - f_{ij})

        """
        self._fodder_in_cell = self.fodder_in_cell + self.alpha * (
                self.f_max - self.fodder_in_cell
        )


class Jungle(BaseCell):
    """Class instance of class Cell for the cell type Jungle."""

    @classmethod
    def set_parameters(cls, f_max=800.0):
        """
        Set default parameters for class instance Jungle.

        :param f_max: Maximum fodder available in cell type Jungle
        :type f_max: float
        """
        super(Jungle, cls).set_parameters(f_max)

    def __init__(self):
        """
        Constructor that initiate class instance Jungle.
        """
        super().__init__()


class Desert(BaseCell):
    """Class instance of class Cell for the cell type Desert."""

    @classmethod
    def set_parameters(cls, f_max=None):
        """
        Set default parameters for class instance Desert.

        :param f_max: Maximum fodder available in cell type Desert
        :type f_max: float
        """
        super(Desert, cls).set_parameters(f_max)

    def __init__(self):
        """
        Constructor that initiate class instance Desert.
        """
        super().__init__()
        self.fodder_in_cell = 0


class Mountain(BaseCell):
    """Class instance of class Cell for the cell types Mountain."""

    @classmethod
    def set_parameters(cls, f_max=0):
        """
        Sets default parameters for class instance Mountain.

        :param f_max: Maximum fodder available in cell type Mountain
        :type f_max: float
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
        """
        return 0

    @property
    def propensity_migration_carn(self):
        """
        Sets the propensity for a Carnivore to migrate to zero,
        because Mountain cells are impassable.
        """
        return 0


class Ocean(BaseCell):
    """Class instance of class Cell for the cell type Ocean."""

    @classmethod
    def set_parameters(cls, f_max=0):
        """
        Set default parameters for class instance Ocean.

        :param f_max: Maximum fodder available in cell type Ocean
        :type f_max: float
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
        """
        return 0

    @property
    def propensity_migration_carn(self):
        """
        Sets the propensity for a Carnivore to migrate to zero,
        because Ocean cells are impassable.
        """
        return 0
