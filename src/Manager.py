"""Class for managing the evolution of a population of antennas."""
import random

from src.Evolver import NSGA2
from src.Genotype import Genotype
from src.Phenotype import Phenotype


class Manager:
    """Manager class."""

    def __init__(self) -> None:
        """Constructor."""
        self.seed = 1  #TODO read in from config
        # coded
        self.rand = random.Random(self.seed)

        self.population = []

        self.per_site_mut_rate = 0.5 #TODO read in from config
        self.mut_effect_size = 0.5 #TODO read in from config

        self.selection_scheme = NSGA2()

    def generate_random_population(self, pop_size: int, generation_num: int) -> None:
        """
        Generate a random population.

        Generates a new population of size 'pop_size' of randomly generated
        Phenotypes.

        :param pop_size: population size.
        :type pop_size: int
        :rtype: None
        """
        for individual in range(pop_size):
            # create new random Genotype with 4 sides
            g = Genotype().generate(2, self.rand)

            # assign phenotype to genotype
            p = Phenotype(g, str(individual), "None", generation_num)

            # append phenotype to population
            self.population.append(p)

    # TODO method to return best individual in population

    def evolve_one_gen(self, generation_num: int) -> None:
        """
        Evolve population for one generation.

        Takes the Manager's population and evolves it for one generation.
        Set's Manager's population to the new generation's population.

        :param generation_num: The generation number of the new generation
        being created.
        :type generation_num: int
        :rtype: None
        """

        new_pop = self.selection_scheme.evolve(self.population)
        self.population = new_pop


def main() -> None:
    """Main function."""
    pop_size = 10 #TODO read in from config
    num_generations = 10  #TODO read in from config

    # 0. Initialize manager
    manager = Manager()

    # 1. Randomly generates starting population
    manager.generate_random_population(pop_size, 0)

    for generation_num in range(1, num_generations):
        print(generation_num)
        # 2. Runs evaluation on population
             # GROUP 2

        # 3. Analyzer collects data on current state of population (to process and write to file)
             # GROUP 3

        # 4. Selects individuals to replicate to the next generation, does evo
        # work on them (mutation, crossover, etc.) and updates population to the
        # next generation.
        manager.evolve_one_gen(generation_num) # need to feed it generation
        # because gen created is a variable you need to make a child Phenotype


if __name__ == "__main__":
    main()
