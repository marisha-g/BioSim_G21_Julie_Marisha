# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import numpy as np
from scipy.special import expit


class Animal:
    """
    Superclass for animal in BioSim.
    """
    @classmethod
    def set_parameters(
            cls,
            w_birth,
            sigma_birth,
            beta,
            eta,
            a_half,
            phi_age,
            w_half,
            phi_weight,
            mu,
            lambda_,
            gamma,
            zeta,
            xi,
            omega,
            F,
            *args,
            **kwargs
    ):
        """
        Set default parameters for class Animal.
        :param w_birth: birth weight
        :type: float
        :param sigma_birth: constant
        :type: float
        :param beta: Constant used to calculate weight gain
        :type: float
        :param eta: Constant used to calculate weight loss
        :type: float
        :param a_half: constant
        :type: float
        :param phi_age: constant
        :type: float
        :param w_half: constant
        :type: float
        :param phi_weight: constant
        :type: float
        :param mu: Constant used to calculate probability to move
        :type: float
        :param lambda_: constant
        :type: float
        :param gamma: Constant used to calculate the probability to give birth
                      to an offspring in a year
        :type: float
        :param zeta: constant
        :type: float
        :param xi: constant
        :type: float
        :param omega: Constant used to calculate the probability of an animal
                      dying
        :type: float
        :param F: Appetite of the species
        :type: float
        :param args: Extra arguments
        :type: *tuple
        :param kwargs: Extra keyword arguments
        :type: **dict
        """

        if w_birth >= 0:
            cls.w_birth = w_birth
        else:
            raise ValueError('w_birth can not be a negative value.')
        if sigma_birth >= 0:
            cls.sigma_birth = sigma_birth
        else:
            raise ValueError('sigma_birth can not be a negative value.')
        if beta >= 0:
            cls.beta = beta
        else:
            raise ValueError('beta can not be a negative value.')
        if eta >= 0:
            cls.eta = eta
        else:
            raise ValueError('eta can not be a negative value.')
        if a_half >= 0:
            cls.a_half = a_half
        else:
            raise ValueError('a_half can not be a negative value.')
        if phi_age >= 0:
            cls.phi_age = phi_age
        else:
            raise ValueError('phi_age can not be a negative value.')
        if w_half >= 0:
            cls.w_half = w_half
        else:
            raise ValueError('w_half can not be a negative value.')
        if phi_weight >= 0:
            cls.phi_weight = phi_weight
        else:
            raise ValueError('phi_weight can not be a negative value.')
        if 0 <= mu <= 1:
            cls.mu = mu
        else:
            raise ValueError('mu can not be a negative value.')
        if lambda_ >= 0:
            cls.lambda_ = lambda_
        else:
            raise ValueError('lambda_ can not be a negative value.')
        if gamma >= 0:
            cls.gamma = gamma
        else:
            raise ValueError('gamma can not be a negative value.')
        if zeta >= 0:
            cls.zeta = zeta
        else:
            raise ValueError('zeta can not be a negative value.')
        if xi >= 0:
            cls.xi = xi
        else:
            raise ValueError('xi can not be a negative value.')
        if omega >= 0:
            cls.omega = omega
        else:
            raise ValueError('omega can not be a negative value.')
        if F >= 0:
            cls.F = F
        else:
            raise ValueError('f can not be a negative value.')

    @classmethod
    def draw_birth_weight(cls):
        """
        Birth weight is drawn from a Gaussian distribution with mean and
        standard deviation.
        :return: birth_weight
        :rtype: float
        """
        cls.birth_weight = 0
        while cls.birth_weight <= 0:
            cls.birth_weight = np.random.normal(cls.w_birth, cls.sigma_birth)
        return cls.birth_weight

    @classmethod
    def reset_migration(cls):
        cls.has_migrated = False

    def __init__(self, age=None, weight=None):
        """
        Constructor that initiate class Animal.
        :param age: initial age
        :type: float
        :param weight: initial weight
        :type: float
        """
        if age is None:
            age = 0
        if age < 0:
            raise ValueError("Age can not have negative value.")
        self.age = age

        if weight is None:
            weight = 10
        if weight < 0:
            raise ValueError("Weight can not have negative value")

        self.weight = weight
        self._fitness = None
        self._prob_migration = None
        self._prob_death = None

    def aging(self):
        """
        At birth, each animal has age a=0. Age increases by one year for
        each year that passes.
        """
        self.age += 1

    def weight_gain(self, food):
        """
        When an animal eats an amount 'food' of fodder, its
        weight increases.
        """
        self.weight += self.beta * food

    def weight_loss(self):
        """
        Every year, the weight of the animal decreases.
        """
        self.weight -= self.eta * self.weight

    def weight_loss_birth(self, weight_offspring):
        """
        Calculates weight loss when an animal gives birth.
        :param weight_offspring: weight of the offspring
        :type: float
        """
        self.weight -= self.xi * weight_offspring

    def prob_procreation(self, n):
        """
        Animals can mate if there are at least two animals of the same species
        in a cell. Probability to give birth is given by the attribute p.
        :param n: number of animals of the same species in a cell
        :return: choice
        :type: int
        """
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return 0
        else:
            p = min(1, self.gamma * self.fitness * (n - 1))
            choice = np.random.choice(2, p=[p, 1 - p])
            return choice

    @property
    def fitness(self):
        """
        The overall condition of the animal is described by its fitness,
        which is calculated based on age and weight.
        :return: self._fitness: calculated fitness
        :type: float
        """
        if self.weight > 0:
            age_sigma = expit(-self.phi_age * (self.age - self.a_half))
            weight_sigma = expit(self.phi_weight * (self.weight - self.w_half))
            self._fitness = age_sigma * weight_sigma
        else:
            self._fitness = 0
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        """
        Set the current fitness. Setting the fitness to a new value
        will reconfigure the animal automatically.
        :param value: new value
        :type: float
        """
        self.fitness = value

    @property
    def prob_migration(self):
        """
        Depends on fitness and availability of fodder in neighboring cells.
        Cannot move to ocean or mountain cells. Probability for moving is given
        by the attribute p.
        :return: self._prob_migration: chooses if animal will migrate
        :type: int
        """
        p = self.mu * self.fitness
        self._prob_migration = np.random.choice(2, p=[p, 1 - p])
        self.has_migrated = True
        return self._prob_migration

    @prob_migration.setter
    def prob_migration(self, value):
        """
        Set the choice for probability to migrate. Setting the choice to a
        new value will reconfigure the animal automatically.
        :param value: new value
        :type: float
        """
        self._prob_migration = value

    @property
    def prob_death(self):
        """
        An animal dies with probability given by the attribute p.
        :return: self._prob_death: chooses if animal will die or not
        :type: int
        """
        if self.fitness == 0:
            self._prob_death = 0
        else:
            p = self.omega * (1 - self.fitness)
            self._prob_death = np.random.choice(2, p=[p, 1 - p])

        return self._prob_death

    @prob_death.setter
    def prob_death(self, value):
        """
        Set the choice for probability to die. Setting the choice to a
        new value will reconfigure the animal automatically.
        :param value: new value
        :type: float
        """
        self._prob_death = value


class Herbivore(Animal):
    """
    Class instance of class Animal for the Herbivore species.
    """

    @classmethod
    def set_parameters(
            cls,
            w_birth=8.0,
            sigma_birth=1.5,
            beta=0.9,
            eta=0.05,
            a_half=40.0,
            phi_age=0.2,
            w_half=10.0,
            phi_weight=0.1,
            mu=0.25,
            lambda_=1.0,
            gamma=0.2,
            zeta=3.5,
            xi=1.2,
            omega=0.4,
            F=10.0,
            *args,
            **kwargs
    ):
        """
        Set default parameters for class instance Herbivore.
        :param w_birth: birth weight
        :type: float
        :param sigma_birth: constant
        :type: float
        :param beta: Constant used to calculate weight gain
        :type: float
        :param eta: Constant used to calculate weight loss
        :type: float
        :param a_half: constant
        :type: float
        :param phi_age: constant
        :type: float
        :param w_half: constant
        :type: float
        :param phi_weight: constant
        :type: float
        :param mu: Constant used to calculate probability to move
        :type: float
        :param lambda_: constant
        :type: float
        :param gamma: Constant used to calculate the probability to give birth
                      to an offspring in a year
        :type: float
        :param zeta: constant
        :type: float
        :param xi: constant
        :type: float
        :param omega: Constant used to calculate the probability of an animal
                      dying
        :type: float
        :param F: Appetite of the species
        :type: float
        :param args: Extra arguments
        :type: *tuple
        :param kwargs: Extra keyword arguments
        :type: **dict
        """
        super(Herbivore, cls).set_parameters(
            w_birth,
            sigma_birth,
            beta,
            eta,
            a_half,
            phi_age,
            w_half,
            phi_weight,
            mu,
            lambda_,
            gamma,
            zeta,
            xi,
            omega,
            F)

    def __init__(self, age=None, weight=None):
        """
        Constructor that initiate class instance Herbivore.
        :param age: initial age for Herbivore
        :type: float
        :param weight: initial weight for Carnivore
        :type: float
        """
        super().__init__(age, weight)


class Carnivore(Animal):
    """
    Class instance of class Animal for the Carnivore species.
    """

    @classmethod
    def set_parameters(
            cls,
            w_birth=6.0,
            sigma_birth=1.0,
            beta=0.75,
            eta=0.125,
            a_half=60.0,
            phi_age=0.4,
            w_half=4.0,
            phi_weight=0.4,
            mu=0.4,
            lambda_=1.0,
            gamma=0.8,
            zeta=3.5,
            xi=1.1,
            omega=0.9,
            F=50.0,
            DeltaPhiMax=10.0,
            *args,
            **kwargs
    ):
        """
        Set default parameters for class instance Carnivore.
        :param w_birth: birth weight
        :type: float
        :param sigma_birth: constant
        :type: float
        :param beta: Constant used to calculate weight gain
        :type: float
        :param eta: Constant used to calculate weight loss
        :type: float
        :param a_half: constant
        :type: float
        :param phi_age: constant
        :type: float
        :param w_half: constant
        :type: float
        :param phi_weight: constant
        :type: float
        :param mu: Constant used to calculate probability to move
        :type: float
        :param lambda_: constant
        :type: float
        :param gamma: Constant used to calculate the probability to give birth
                      to an offspring in a year
        :type: float
        :param zeta: constant
        :type: float
        :param xi: constant
        :type: float
        :param omega: Constant used to calculate the probability of an animal
                      dying
        :type: float
        :param F: Appetite of the species
        :type: float
        :param DeltaPhiMax: constant
        :type: float
        :param args: Extra arguments
        :type: *tuple
        :param kwargs: Extra keyword arguments
        :type: **dict
        """
        super(Carnivore, cls).set_parameters(
            w_birth,
            sigma_birth,
            beta,
            eta,
            a_half,
            phi_age,
            w_half,
            phi_weight,
            mu,
            lambda_,
            gamma,
            zeta,
            xi,
            omega,
            F
        )
        if DeltaPhiMax is None:
            DeltaPhiMax = 10.0

        if DeltaPhiMax <= 0:
            raise ValueError('delta_phi_max must be strictly positive.')
        cls.DeltaPhiMax = DeltaPhiMax

    def __init__(self, age=None, weight=None):
        """
        Constructor that initiate class instance Carnivore.
        :param age: initial age for Herbivore species
        :type: float
        :param weight: initial weight for Carnivore species
        :type: float
        """
        super().__init__(age, weight)
        self._prob_carnivore_kill = None

    def prob_carnivore_kill(self, fitness_prey):
        """
        Probability for a Carnivore to kill a Herbivore.
        :param fitness_prey: the fitness of the prey (Herbivore)
        :type: float
        :return: self._prob_carnivore_kill: chooses if the Carnivore will
                 kill or not.
        :type: int
        """
        if self.fitness <= fitness_prey:
            self._prob_carnivore_kill = 0
            return self._prob_carnivore_kill
        elif 0 < self.fitness - fitness_prey < self.DeltaPhiMax:
            p = (self.fitness - fitness_prey) / self.DeltaPhiMax
            choice = np.random.choice(2, p=[1 - p, p])
            self._prob_carnivore_kill = choice
            return self._prob_carnivore_kill
        else:
            self._prob_carnivore_kill = 1
            return self._prob_carnivore_kill

    # @prob_carnivore_kill.setter
    # def prob_carnivore_kill(self, value):
    #        """
    #       Set the choice for probability for a Carnivore to kill a Herbivore.
    #      Setting the choice to a new value will reconfigure the animal
    #     automatically.
    #   :type: float
    #  """
    # self._prob_carnivore_kill = value
