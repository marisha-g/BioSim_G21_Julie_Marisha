# -*- coding: utf-8 -*-

"""
Tests for classes in animal.py using pytest.
"""

__author__ = 'Julie Forrisdal', 'Marisha Gnanaseelan'
__email__ = 'juforris@nmbu.no', 'magn@nmbu.no'

import pytest

from biosim.animal import BaseAnimal, Herbivore, Carnivore


class TestAnimal:
    """Tests for class Animal."""
    @pytest.fixture(autouse=True)
    def create_base_animal(self):
        self.base_animal = BaseAnimal()
        self.carnivore = Carnivore()
        self.herbivore = Herbivore()
        Herbivore.set_parameters()
        Carnivore.set_parameters()

    def test_value_error_for_negative_values(self):
        """Negative values raises ValueError."""
        with pytest.raises(ValueError):
            self.base_animal.set_parameters(
                -8.0, -1.5, -0.9,  -0.05, -40.0, -0.2, -10.0, -0.1,
                -0.25, -1.0, -0.2, -3.5, -1.2, -0.4, -10.0
            )

    def test_draw_birth_weight(self):
        """ Test that birth_weight method returns positive number."""
        assert self.herbivore.draw_birth_weight() >= 0
        assert self.carnivore.draw_birth_weight() >= 0

    def test_reset_migration(self):
        """Test that reset migration is False."""
        assert self.base_animal.reset_migration() is False

    def test_value_error_for_age_and_weight(self):
        """Check if ValueError is raised for negative inputs. """
        with pytest.raises(ValueError):
            Herbivore(age=-4, weight=-5)
        with pytest.raises(ValueError):
            Carnivore(age=-60, weight=-2.2)

    def test_aging(self):
        """Test if aging method increments an animal's age by 1."""
        self.herbivore.age = 0
        self.carnivore.age = 0

        self.herbivore.aging()
        self.carnivore.aging()

        assert self.herbivore.age == 1
        assert self.carnivore.age == 1

    def test_weight_gain(self):
        """Weight increases when weight gain method is called. """
        herb_weight_1 = self.herbivore.weight
        carn_weight_1 = self.carnivore.weight

        self.herbivore.weight_gain(5)
        self.carnivore.weight_gain(5)

        assert herb_weight_1 < self.herbivore.weight
        assert carn_weight_1 < self.carnivore.weight

    def test_weight_loss(self):
        """Weight decreases when weight loss method is called."""
        herb_weight_1 = self.herbivore.weight
        carn_weight_1 = self.carnivore.weight

        self.herbivore.weight_loss()
        self.carnivore.weight_loss()

        assert herb_weight_1 > self.herbivore.weight
        assert carn_weight_1 > self.carnivore.weight

    def test_prob_procreation(self):
        """Probability for procreation is 0 when weight is 0."""
        self.herbivore.weight = 0
        self.carnivore.weight = 0

        assert self.herbivore.prob_procreation(10) == 0
        assert self.carnivore.prob_procreation(13) == 0

    def test_fitness(self):
        """Tests if the formula for evaluating fitness works."""
        self.base_animal = Herbivore()
        self.base_animal.set_parameters()
        self.base_animal.weight = 10
        self.base_animal.age = 2
        assert self.base_animal.fitness == pytest.approx(0.49975)

    def test_prob_death_is_callable(self):
        """Property prob_death is callable."""
        self.herbivore.prob_death
        self.carnivore.prob_death


class TestHerbivore:
    """Tests for subclass Herbivore."""
    @pytest.fixture(autouse=True)
    def create_herbivore(self):
        self.herbivore = Herbivore()
        Herbivore.set_parameters()

    def test_constructor_default(self):
        """Default constructor callable."""
        assert isinstance(self.herbivore, Herbivore)

    def test_default_parameters(self):
        """Test if default parameters are given."""
        assert self.herbivore.age == 0
        assert self.herbivore.weight == 10
        assert self.herbivore._fitness is None

        assert self.herbivore.w_birth == 8.0
        assert self.herbivore.sigma_birth == 1.5
        assert self.herbivore.beta == 0.9
        assert self.herbivore.eta == 0.05
        assert self.herbivore.a_half == 40.0
        assert self.herbivore.phi_age == 0.2
        assert self.herbivore.w_half == 10.0
        assert self.herbivore.phi_weight == 0.1
        assert self.herbivore.mu == 0.25
        assert self.herbivore.lambda_ == 1.0
        assert self.herbivore.gamma == 0.2
        assert self.herbivore.zeta == 3.5
        assert self.herbivore.xi == 1.2
        assert self.herbivore.omega == 0.4
        assert self.herbivore.F == 10.0

    def test_zero_weight_gives_zero_fitness(self):
        """Fitness is zero if weight is zero. """
        self.herbivore.weight = 0
        assert self.herbivore.fitness == 0.0


class TestCarnivore:
    """Tests for subclass Carnivore"""
    @pytest.fixture(autouse=True)
    def create_carnivore(self):
        self.carnivore = Carnivore()
        Carnivore.set_parameters()

    def test_constructor_default(self):
        """Default constructor callable."""
        assert isinstance(self.carnivore, Carnivore)

    def test_default_parameters(self):
        """Tests if default parameters are given."""
        self.carnivore = Carnivore()
        assert self.carnivore.age == 0
        assert self.carnivore.weight == 10

        assert self.carnivore.w_birth == 6.0
        assert self.carnivore.sigma_birth == 1.0
        assert self.carnivore.beta == 0.75
        assert self.carnivore.eta == 0.125
        assert self.carnivore.a_half == 60.0
        assert self.carnivore.phi_age == 0.4
        assert self.carnivore.w_half == 4.0
        assert self.carnivore.phi_weight == 0.4
        assert self.carnivore.mu == 0.4
        assert self.carnivore.lambda_ == 1.0
        assert self.carnivore.gamma == 0.8
        assert self.carnivore.zeta == 3.5
        assert self.carnivore.xi == 1.1
        assert self.carnivore.omega == 0.9
        assert self.carnivore.F == 50.0
        assert self.carnivore.DeltaPhiMax == 10.0

    def test_delta_phi_max_value_error(self):
        """Test that delta phi max must be strictly positive."""
        with pytest.raises(ValueError):
            Carnivore().set_parameters(DeltaPhiMax=0)
        with pytest.raises(ValueError):
            Carnivore().set_parameters(DeltaPhiMax=-2)

    def test_value_error_for_mu(self):
        """Test that mu can not be greater than 1."""
        with pytest.raises(ValueError):
            Carnivore().set_parameters(mu=2)
