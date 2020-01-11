# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import numpy as np


class Animal:
    """
    Superclass for animal in Biosim.
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

    def __init__(self, age=None, weight=None):
        """ Constructor initiate animal.
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

    def aging(self):
        """
        At birth, each animal has age a=0. Age increases by one year for
        each year that passes.
        """
        self.age += 1

    @property
    def draw_birth_weight(self):
        """
        Birth weight is drawn from a Gaussian distribution with mean and
        standard deviation.
        :return: float
        """
        birth_weight = 0
        while birth_weight <= 0:
            birth_weight = np.random.normal(self.w_birth, self.sigma_birth)
        return birth_weight

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

    @property
    def fitness(self):
        """
        The overall condition of the animal is described by its fitness,
        which is calculated based on age and weight using a formula (4)
        """
        if self.weight > 0:
            self._fitness = (1 / (1 + np.exp(self.phi_age *
                                             (self.age - self.a_half)
                                             )
                                  )
                             ) * \
                            (
                                    1 / (1 + np.exp(-self.phi_weight *
                                                    (self.weight - self.w_half)
                                                    )
                                         )
                            )
        else:
            self._fitness = 0.0
        return self._fitness

    def prob_procreation(self, n):
        """
        Animals can mate if there are at least two animals of the same species
        in a cell. Probability to give birth is given by fomula (8)
        :return: float
        """
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return 0.0
        else:
            p = min(1, self.gamma * self.fitness * (n - 1))
            probability_procreation = np.random.choice(2, p=[p, 1 - p])
            return probability_procreation

    def prob_death(self):
        """
        An animal dies with probability following formula (9)
        :return: float
        """
        if self.fitness == 0:
            return 0.0
        else:
            p = self.omega * (1 - self.fitness)
            probability_death = np.random.choice(2, p=[p, 1 - p])
            return probability_death

    def prob_migration(self):
        """
        Depends on fitness and availability of fodder in neighboring cells.
        Cannot move to ocean or mountain cells. Probability for moving is given
        by formula (5 - 7).
        :param:
        :return: float
        """
        p = self.mu * self.fitness
        probability_migration = np.random.choice(2, p=[p, 1 - p])
        return probability_migration


class Herbivore(Animal):

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
        super().__init__(age, weight)


class Carnivore(Animal):
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
        super().__init__(age, weight)
