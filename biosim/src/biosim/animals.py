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
        cls.w_birth = w_birth
        cls.sigma_birth = sigma_birth
        cls.beta = beta
        cls.eta = eta
        cls.a_half = a_half
        cls.phi_age = phi_age
        cls.w_half = w_half
        cls.phi_weight = phi_weight
        cls.mu = mu
        cls.lambda_ = lambda_
        cls.gamma = gamma
        cls.zeta = zeta
        cls.xi = xi
        cls.omega = omega
        cls.f = f


    def __init__(self, name, age=0, weight=None, fitness):
        """constructor"""
        self.name = name
        self.age = age
        self.weight = weight
        self.fitness = fitness

    def aging(self):
        """
        At birth,each animal has age a=0. Age increases by one year for
        each year that passes.
        :return:
        """
        self.age += 1

    def weight_birth(self):
        """
        Birth weight is drawn from a Gaussian distribution with mean and
        standard deviation.
        :return:
        """
        self.weight += np.random.normal(self.w_birth, self.sigma_birth)

    def weight_gain(self):
        """
        When an animal eats an amount F of fodder, its
        weight increases.
        :return:
        """
        self.weight += self.beta * self.F

    def weight_loss(self):
        """
        Every year, the weight of the animal decreases.
        :return:
        """
        self.weight -= self.eta * self.weight

    def fitness(self):
        """
        The overall condition of the animal is described by its fitness,
        which is calculated based on age and weight using a formula (4)
        :return:
        """

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


    def __init__(self):
        super().__init__()
        pass


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
            f)

    def __init__(self):
        super().__init__(age=0, weight=None)
        pass