# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import numpy as np


class Animals:
    """
    Description for the Animals class
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
            f
    ):
        if w_birth >=0:
            cls.w_birth = w_birth
        else:
            raise ValueError('w_birth can not be a negative value.')
        if sigma_birth >=0:
            cls.sigma_birth = sigma_birth
        else:
            raise ValueError('sigma_birth can not be a negative value.')
        if beta >=0:
            cls.beta = beta
        else:
            raise ValueError('beta can not be a negative value.')
        if eta >=0:
            cls.eta = eta
        else:
            raise ValueError('eta can not be a negative value.')
        if a_half >=0:
            cls.a_half = a_half
        else:
            raise ValueError('a_half can not be a negative value.')
        if phi_age >=0:
            cls.phi_age = phi_age
        else:
            raise ValueError('phi_age can not be a negative value.')
        if w_half >=0:
            cls.w_half = w_half
        else:
            raise ValueError('w_half can not be a negative value.')
        if phi_weight >=0:
            cls.phi_weight = phi_weight
        else:
            raise ValueError('phi_weight can not be a negative value.')
        if 0 <= mu <= 1:
            cls.mu = mu
        else:
            raise ValueError('mu can not be a negative value.')
        if lambda_ >=0:
            cls.lambda_ = lambda_
        else:
            raise ValueError('lambda_ can not be a negative value.')
        if gamma >=0:
            cls.gamma = gamma
        else:
            raise ValueError('gamma can not be a negative value.')
        if zeta >=0:
            cls.zeta = zeta
        else:
            raise ValueError('zeta can not be a negative value.')
        if xi >=0:
            cls.xi = xi
        else:
            raise ValueError('xi can not be a negative value.')
        if omega >=0:
            cls.omega = omega
        else:
            raise ValueError('omega can not be a negative value.')
        if f >=0:
            cls.f = f
        else:
            raise ValueError('f can not be a negative value.')

    def __init__(self, age=0, weight=None):
        """constructor"""
        self.age = age
        self.weight = weight
        self.fitness = None

    def aging(self):
        """
        At birth,each animal has age a=0. Age increases by one year for
        each year that passes.
        :return:
        """
        self.age += 1

    def birth_weight(self):
        """
        Birth weight is drawn from a Gaussian distribution with mean and
        standard deviation.
        :return:
        """
        birth_weight = 0
        while birth_weight <= 0:
            birth_weight = np.random.normal(self.w_birth, self.sigma_birth)
        return birth_weight

    def weight_gain(self, food):
        """
        When an animal eats an amount F of fodder, its
        weight increases.
        :return:
        """
        self.weight += self.beta * food

    def weight_loss(self):
        """
        Every year, the weight of the animal decreases.
        :return:
        """
        self.weight -= self.eta * self.weight

    def evaluate_fitness(self):
        """
        The overall condition of the animal is described by its fitness,
        which is calculated based on age and weight using a formula (4)
        :return:
        """
        if self.weight > 0:
            self.fitness = (1 / (1 + np.exp(self.phi_age *
                                            (self.age - self.a_half)))) * (
                        1 / (1 + np.exp(-self.phi_weight *
                                        (self.weight - self.w_half))))
        else:
            self.fitness = 0  # aka død

    def migration(self):
        """
        Depends on fitness and availability of fodder in neighboring cells.
        Cannot move to ocean or mountain cells. Probability for moving is given
        by formula (5 - 7).
        :return:
        """

    def procreation(self, n):
        """
        Animals can mate if there are at least two animals of the same species
        in a cell. Probability to give birth is given by fomula (8)
        :return:
        """
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return 0
        else:
            p = min(1, self.gamma * self.fitness * (n - 1))
            probability_procreation = np.random.choice(2, p=[p, 1-p])
            return probability_procreation

    def death(self):
        """
        An animal dies following formula (9)
        Får vi 0 så dør dyret, får vi 1 overlever den.
        :return:
        """
        if self.fitness == 0:
            return 0
        else:
            p = self.omega * (1 - self.fitness)
            probability_death = np.random.choice(2, p=[p, 1-p])
            return probability_death


class Herbivore(Animals):

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
            f=10.0
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
            f)

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)


class Carnivore(Animals):
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
            f=50.0,
            delta_phi_max=10.0
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
            f
        )
        if delta_phi_max > 0:
            cls.delta_phi_max = 10.0
        else:
            raise ValueError('delta_phi_max must be strictly positive.')

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)
