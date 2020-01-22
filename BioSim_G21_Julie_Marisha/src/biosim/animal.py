# -*- coding: utf-8 -*-

"""
:mod: `biosim.animal` provides the user information about the fauna on
       Rossumøya.


The different species on Rossumøya have certain characteristics in common, 
but also some differences. This script has all the characteristics for the
Herbivores and Carnivores stored in superclasses and subclasses.

This file can be imported as a module and contains the following
classes:

    *   BaseAnimal - Superclass and the basic characteristics that all of the
        species in Rossumøya has in common.

    *   Herbivore(BaseAnimal) - Subclass of BaseAnimal and characteristics for
        the Herbivore species.

    *   Carnivore(BaseAnimal) - Subclass of BaseAnimal and characteristics for
        the Carnivore species.

.. note::
    *   This script requires that `numpy` and `numba` are installed
        within the Python environment you are running this script in.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import random
import math
from numba import jit



class BaseAnimal:
    """Superclass for animals in BioSim."""

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

        :param w_birth: Constant
        :type w_birth: float
        :param sigma_birth: Constant
        :type sigma_birth: float
        :param beta: Constant used to calculate weight gain
        :type beta: float
        :param eta: Constant used to calculate weight loss
        :type eta: float
        :param a_half: Constant
        :type a_half: float
        :param phi_age: Constant
        :type phi_age: float
        :param w_half: Constant
        :type w_half: float
        :param phi_weight: Constant
        :type phi_weight: float
        :param mu: Constant used to calculate probability to move
        :type mu: float
        :param lambda_: Constant
        :type lambda_: float
        :param gamma: Constant used to calculate the probability to give birth
                        to an offspring in a year
        :type gamma: float
        :param zeta: Constant
        :type zeta: float
        :param xi: Constant
        :type xi: float
        :param omega: Constant used to calculate the probability
                        of an animal dying
        :type omega: float
        :param F: Appetite of the species
        :type F: float
        :param args: Extra arguments
        :type args: *tuple
        :param kwargs: Extra keyword arguments
        :type kwargs: **dict
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
        Birth weight is drawn from a Gaussian distribution based on mean and
        standard deviation.

        :return: Birth weight
        :rtype: float
        """
        cls.birth_weight = 0
        while cls.birth_weight <= 0:
            cls.birth_weight = random.gauss(cls.w_birth, cls.sigma_birth)
        return cls.birth_weight

    def __init__(self, age=None, weight=None):
        """
        Constructor that initiates class BaseAnimal.

        :param age: Initial age
        :type age: float
        :param weight: Initial weight
        :type weight: float
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
        self.fitness_has_been_calculated = False
        self._prob_migration = None
        self._prob_death = None
        self.has_migrated = False

    def aging(self):
        """
        At birth, each animal has age 0. Age increments by one each year.
        """
        self.age += 1
        self.fitness_has_been_calculated = False

    def weight_gain(self, food):
        """
        When an animal eats an amount 'food' of fodder, its
        weight increases.

        :param food: Amount of food eaten.
        :type food: int
        """
        self.weight += (self.beta * food)
        self.fitness_has_been_calculated = False

    def weight_loss(self):
        """
        Every year, the weight of the animal decreases.
        """
        self.weight -= (self.eta * self.weight)
        self.fitness_has_been_calculated = False

    def weight_loss_birth(self, weight_offspring):
        """
        When an animal gives birth to an offspring, it loses weight.

        :param weight_offspring: Weight of the offspring
        :type weight_offspring: float
        """
        self.weight -= (self.xi * weight_offspring)
        self.fitness_has_been_calculated = False

    def prob_procreation(self, n):
        r"""
        Animals can mate if there are at least two animals of the same species
        in a cell. Probability to give birth is given by the variable p which
        is calculated with the following formula.

        .. math::

            min(1, \gamma \times \Phi \times (N - 1))

        .. math::
            \mbox { where } \gamma \mbox { is a constant, } \Phi \mbox
            { is fitness and } N \mbox { is the number of animals i a cell.}

        :param n: Number of animals of the same species in a cell
        :type n: int
        :return: Either 0 or 1
        :rtype: int
        """
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return 0
        else:
            p = min(1, self.gamma * self.fitness * (n - 1))
            choice = custom_binomial(p)
            return choice

    @property
    def fitness(self):
        """
        The overall condition of an animal is described by its fitness,
        which is calculated based on age and weight with a call to the
        `fitness_calculator` function.

            :setter: Sets the fitness value
            :type: float
        """
        if self.fitness_has_been_calculated:
            return self._fitness

        if self.weight > 0:
            self.fitness = fitness_calculator(
                self.phi_age, self.age, self.a_half,
                self.phi_weight, self.weight, self.w_half
            )
            self.fitness_has_been_calculated = True
        else:
            self._fitness = 0
            self.fitness_has_been_calculated = True

        return self._fitness

    @fitness.setter
    def fitness(self, value):
        """
        Sets the attribute self._fitness to a new value.
        """
        self._fitness = value

    @property
    def prob_migration(self):
        """
        Calculates the probability for an animal to migrate, based on fitness
        and availability of fodder in neighboring cells. Probability for
        moving is given by the variable p.

            :setter: Sets the probability value
            :type: int
        """
        p = self.mu * self.fitness
        self._prob_migration = custom_binomial(p)
        return self._prob_migration

    @prob_migration.setter
    def prob_migration(self, value):
        """
        Sets the probability for an animal to migrate to a new value.
        """
        self._prob_migration = value

    @property
    def prob_death(self):
        """
        An animal dies with probability p based on its fitness.

            :setter: Sets the probability value.
            :type: int
        """
        if self.fitness == 0:
            self._prob_death = 1
        else:
            p = self.omega * (1 - self.fitness)
            self._prob_death = custom_binomial(p)

        return self._prob_death

    @prob_death.setter
    def prob_death(self, value):
        """
        Sets the probability for an animal to die.
        """
        self._prob_death = value


class Herbivore(BaseAnimal):
    """Class for the herbivore species in Biosim.
    Subclass of class BaseAnimal."""

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
        Set default parameters for class instance of Herbivore.

        :param w_birth: Constant
        :type w_birth: float
        :param sigma_birth: Constant
        :type sigma_birth: float
        :param beta: Constant used to calculate weight gain
        :type beta: float
        :param eta: Constant used to calculate weight loss
        :type eta: float
        :param a_half: Constant
        :type a_half: float
        :param phi_age: Constant
        :type phi_age: float
        :param w_half: Constant
        :type w_half: float
        :param phi_weight: Constant
        :type phi_weight: float
        :param mu: Constant used to calculate probability to move
        :type mu: float
        :param lambda_: Constant
        :type lambda_: float
        :param gamma: Constant used to calculate the probability for an
                        animal to give birth.
        :type gamma: float
        :param zeta: Constant
        :type zeta: float
        :param xi: Constant
        :type xi: float
        :param omega: Constant used to calculate the probability of an
                        animal dying.
        :type omega: float
        :param F: Appetite of the species
        :type F: float
        :param args: Extra arguments
        :type args: *tuple
        :param kwargs: Extra keyword arguments
        :type kwargs: **dict
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
        Constructor that initiates class instances of Herbivore.

        :param age: Initial age for Herbivore
        :type age: float
        :param weight: Initial weight for Carnivore
        :type weight: float
        """
        super().__init__(age, weight)


class Carnivore(BaseAnimal):
    """Class for the carnivore species in Biosim.
    Subclass of class BaseAnimal."""
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
            DeltaPhiMax=None,
            *args,
            **kwargs
    ):
        """
        Set default parameters for class instance Carnivore.

        :param w_birth: Constant
        :type w_birth: float
        :param sigma_birth: Constant
        :type sigma_birth: float
        :param beta: Constant used to calculate weight gain
        :type beta: float
        :param eta: Constant used to calculate weight loss
        :type eta: float
        :param a_half: Constant
        :type a_half: float
        :param phi_age: Constant
        :type phi_age: float
        :param w_half: Constant
        :type w_half: float
        :param phi_weight: Constant
        :type phi_weight: float
        :param mu: Constant used to calculate probability to move
        :type mu: float
        :param lambda_: Constant
        :type lambda_: float
        :param gamma: Constant used to calculate the probability to give birth
                        to an offspring in a year
        :type gamma: float
        :param zeta: Constant
        :type zeta: float
        :param xi: Constant
        :type xi: float
        :param omega: Constant used to calculate the probability of an animal
                        dying
        :type omega: float
        :param F: Appetite of the species
        :type F: float
        :param DeltaPhiMax: Constant
        :type DeltaPhiMax: float
        :param args: Extra arguments
        :type args: *tuple
        :param kwargs: Extra keyword arguments
        :type kwargs: **dict
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

        :param age: Initial age for Carnivore species
        :type age: float
        :param weight: Initial weight for Carnivore species
        :type weight: float
        """
        super().__init__(age, weight)
        self._prob_carnivore_kill = None

    def prob_carnivore_kill(self, fitness_prey):
        r"""
        Calculates the probability for a Carnivore to kill a Herbivore,
        and decides accordingly. The formula for calculating this probability
        is given below.

        .. math::
            p =
            \begin{cases}
            0 & \mbox { if } \Phi_{carn} \leq \Phi_{herb} \\
            \frac{\Phi_{carn} - \Phi_{herb}}{\Delta \Phi_{max}} &
            \mbox { if } 0 < \Phi_{carn} - \Phi_{herb < \Delta \Phi_{max}} \\
            0 & \mbox { otherwise }
            \end{cases} \quad

        .. math::

            \mbox { where } \Phi_{carn} \mbox
            { is the fitness of the carnivore, } \Phi_{herb} \mbox
            { is the fitness of the herbivore and }
            \Delta\Phi_{max} \mbox { is a constant.}

        :param fitness_prey: The fitness of the prey (Herbivore)
        :type fitness_prey: float
        :return: Either 0 or 1
        :rtype: int
        """
        if self.fitness <= fitness_prey:
            return 0
        if 0 < self.fitness - fitness_prey < self.DeltaPhiMax:
            p = (self.fitness - fitness_prey) / self.DeltaPhiMax
            choice = custom_binomial(p)
            return choice
        return 1


@jit
def custom_binomial(p):
    """Function for drawing random numbers similar to
     numpy.random.binomial(n=1, p=p), but with built_in method
     `random.uniform` for faster code execution.
      Uses the numba.jit decorator.

     :param p: Probability
     :type p: float
     :return: Either 0 or 1
     :rtype: int
     """
    x = random.uniform(0, 1)
    if x < p:
        return 1
    else:
        return 0


@jit
def fitness_calculator(
        phi_age, age, a_half, phi_weight, weight, w_half
):
    r"""
    Uses the numba.jit decorator.
    Calculates fitness based on age and weight. The fitness is calculated by
    using the following formula.

    .. math::
        \Phi =
        \begin{cases}
        0 & w \leq 0 \\
        q^+(a, a_{\frac{1}{2}, \phi_{age}}) \times q^-(w, w_{\frac{1}{2},
        \phi_{weight}}) & else
        \end{cases}

    where

    .. math::
        q^\pm(x, x_{\frac{1}{2}}, \phi) =
        \frac{1}{1 + e^{\pm \phi(x - x_{\frac{1}{2}})}}

    Note that :math:`0 \leq \Phi \leq 1`.


        :param phi_age: Constant
        :type phi_age: float
        :param age: The age of the animal
        :type age: int
        :param a_half: Constant
        :type a_half: float
        :param phi_weight: Constant
        :type phi_weight: float
        :param weight: The weight of the animal
        :type weight: float
        :param w_half: Constant
        :type w_half: float
        :return: Calculated fitness
        :rtype: float
    """
    age_sigma = 1 / (1 + math.exp(phi_age * (age - a_half)))
    weight_sigma = 1 / (1 + math.exp(- phi_weight * (weight - w_half)))
    fitness = age_sigma * weight_sigma
    return fitness
