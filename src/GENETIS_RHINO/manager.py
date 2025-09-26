"""Class for managing the evolution of a population of antennas."""
import pathlib
import random

from src.GENETIS_RHINO.analysis import Analysis
from src.GENETIS_RHINO.evolver import NSGA2
from src.GENETIS_RHINO.genotype import Genotype
from src.GENETIS_RHINO.parameters import ParametersObject
from src.GENETIS_RHINO.phenotype import Phenotype


class Manager:
    """Manager class."""

    def __init__(self, cfg: ParametersObject) -> None:
        """Constructor."""
        self.seed = cfg.random_num_seed
        self.rand = random.Random(self.seed)

        self.population = []

        # import selection scheme
        selection_scheme_convert_dict = {
            "NSGAII": NSGA2,
        }
        if cfg.selection_scheme in selection_scheme_convert_dict:
            self.selection_scheme = selection_scheme_convert_dict[cfg.selection_scheme]()
            return
        raise ValueError("Invalid selection scheme")

    def initialize_population(self, cfg: ParametersObject) -> None:
        """
        Generate a random population.

        Generates a new population of randomly generated Phenotypes.

        :param cfg: Configuration object.
        :type cfg: ParametersObject
        :rtype: None
        """
        pop_size = int(cfg.population_size)
        initial_generation_num = 0

        # calculate how many individuals with and without ridges to generate
        make_without_ridge = int(pop_size * float(
            cfg.percent_no_ridge_at_start))
        make_with_ridge = pop_size - make_without_ridge

        # generate starting individuals with ridges
        for individual in range(make_with_ridge):
            # create new random Genotype with 4 sides
            g = Genotype(cfg).generate_with_ridge(self.rand)

            # assign phenotype to genotype
            p = Phenotype(g, str(individual), "None", initial_generation_num)

            # append phenotype to population
            self.population.append(p)

        # generate starting individuals without ridges
        for individual in range(make_without_ridge):
            # create new random Genotype with 4 sides
            g = Genotype(cfg).generate_without_ridge(self.rand)

            # assign phenotype to genotype
            p = Phenotype(g, str(individual), "None", initial_generation_num)

            # append phenotype to population
            self.population.append(p)

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
        next_gen_pop = self.selection_scheme.evolve(self.population,
                                                    generation_num, self.rand)
        self.population = next_gen_pop

def main() -> None:
    """Main function."""
    # 0. Initialize manager
    cfg = ParametersObject(str(pathlib.Path(
        __file__).parent.parent/"GENETIS_RHINO/config.toml"))
    manager = Manager(cfg)

    num_generations = int(cfg.num_generations)

    # 1. Randomly generates initial population
    manager.initialize_population(cfg)

    for generation_num in range(1, num_generations):
        # 2. Selects individuals to replicate to the next generation,
        # does evo work on them (mutation, crossover, etc.) and updates
        # population to the next generation.
        manager.evolve_one_gen(generation_num)

        # 3. Analyzer collects data on current state of population (to process and write to file)
        Analysis(manager.population).update(generation_num)


if __name__ == "__main__":
    main()
