# -*- coding: utf-8 -*-

import numpy as np
import random

"""
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

class Animals:
    """
    Description for the Animals class
    """
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
            if probability_death == 0:
                return probability_death
