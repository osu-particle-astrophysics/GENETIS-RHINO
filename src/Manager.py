"""Class for managing the evolution of a population of antennas."""
import random

from src.Genotype import Genotype
from src.Phenotype import Phenotype


class Manager:
    """Manager class."""

    def __init__(self) -> None:
        """Constructor."""
        self.seed = 1  #TODO this should be read into the program not hard
        # coded
        self.rand = random.seed(self.seed)
        self.population = []

    def generate_random_population(self, pop_size: int) -> None:
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
            g = Genotype().generate(4, self.rand)

            # assign phenotype to genotype
            p = Phenotype(g, str(individual), "None", 0)

            # append phenotype to population
            self.population.append(p)

    # TODO method to return best individual in population

def main() -> None:
    """Main function."""
    # 0. Initialize manager
    manager = Manager()

    # 1. Randomly generates starting population
    manager.generate_random_population(5)

    # 2. Runs evaluation on population

    # 3. Analyzer collects data on current state of population (to process and write to file)

    # 4. Selects individuals to replicate to the next generation

    # 5. Triggers mutations on next generation

    # 6. Loop back to step 2


if __name__ == "__main__":
    main()
