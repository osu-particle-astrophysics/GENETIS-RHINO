"""Record the best individuals and fitness score statistics for each generation of Phenotypes."""
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from src.GENETIS_RHINO.phenotype import Phenotype


# noinspection SpellCheckingInspection
class Analysis:
    """Collect data about the progress of generations and fitness."""

    def __init__(self, population: list) -> None:
        """Track the population as it is updated."""
        self.population = population
        self.generation_counter = 0

    def update(self, generation_num: int) -> None:
        """Increment the generation counter; write to the fitness and the best individual CSV files."""
        self.generation_counter = generation_num
        print(f"Generation: {self.generation_counter}")
        self.update_fitness_scores()
        self.update_best_individuals()

    def update_best_individuals(self) -> list[Phenotype]:
        """Read the nsgaii rank from each individual and find the individuals on the pareto front (lowest rank)."""
        min_rank = min(indiv.nsgaii_rank for indiv in self.population)
        best_indivs = [indiv for indiv in self.population if indiv.nsgaii_rank==min_rank]
        self.to_csv_best_individuals(best_indivs)
        return best_indivs

    @staticmethod
    def to_csv_best_individuals(best_indivs: list[Phenotype],
                                csv_path: str="best_individuals.csv") -> (
            DataFrame):
        """Write the attributes of the best phenotypes to a CSV file."""

        def make_row(indiv: Phenotype) -> pd.DataFrame:
            """Get the attributes of a phenotype and turn its attributes into a table row."""
            row = {}
            row["Indiv_ID"]             = [indiv.indiv_id]
            row["Parent1_ID"]           = [indiv.parent1_id]
            row["Generation_Created"]   = [indiv.generation_created]
            row["Flare_Length"]         = [indiv.genotype.flare_length]
            row["Waveguide_Height"]     = [indiv.genotype.waveguide_height]
            row["Waveguide_Length"]     = [indiv.genotype.waveguide_length]
            row["Waveguide_Width"]      = [indiv.genotype.waveguide_width]

            counter = 1
            for wp in indiv.genotype.walls:
                attribute = "WP" + str(counter) + "_Has_Ridge"
                row[attribute] = [wp.has_ridge]

                attribute = "WP" + str(counter) + "_Angle"
                row[attribute] = [wp.angle]

                attribute = "WP" + str(counter) + "_Ridge_Height"
                row[attribute] = [wp.ridge_height]

                attribute = "WP" + str(counter) + "_Ridge_Width_Top"
                row[attribute] = [wp.ridge_width_top]

                attribute = "WP" + str(counter) + "_Ridge_Width_Bottom"
                row[attribute] = [wp.ridge_width_bottom]

                attribute = "WP" + str(counter) + "_Ridge_Thickness_Top"
                row[attribute] = [wp.ridge_thickness_top]

                attribute = "WP" + str(counter) + "_Ridge_Thickness_Bottom"
                row[attribute] = [wp.ridge_thickness_bottom]

                counter += 1

            for metric, score in indiv.fitness_scores.items():
                row[metric] = [score]
            return pd.DataFrame(row)

        indiv_df = pd.concat([make_row(indiv) for indiv in best_indivs])
        indiv_df.to_csv(csv_path, mode="w", header=True, index=False)
        return indiv_df

    def update_fitness_scores(self) -> dict[str, int]:
        """Read the fitness from each individual and calculate the maximum and average."""
        # Create dictionary containing fitness scores from every phenotype in the population.
        all_scores = {}
        for indiv in self.population:
            scores = indiv.fitness_scores
            # Append the fitness scores for each individual to the all_score dictionary.
            if len(all_scores) > 0:
                for metric, score in scores.items():
                    all_scores[metric].append(score)
            # On the first phenotype of the population, initiate the all_score dictionary.
            else:
                all_scores = {metric: [score] for metric, score in scores.items()}
        # Create the fitness statistics log.
        fitness_stats_dict = {"Generation": self.generation_counter}
        for metric, scores in all_scores.items():
            fitness_stats_dict[metric+"_Average"] = [sum(scores) / len(scores)]
            fitness_stats_dict[metric+"_Maximum"] = [max(scores)]
        self.to_csv_fitness(fitness_stats_dict)
        return fitness_stats_dict

    @staticmethod
    def to_csv_fitness(fitness: dict, csv_path: str= "fitness.csv") -> pd.DataFrame:
        """Write generation fitness statistics to a CSV file."""
        # Format data for CSV using pandas.
        fitness_row = pd.DataFrame(fitness)
        fitness_row.to_csv(csv_path, mode="a", header=not Path(csv_path).exists(), index=False)
        return fitness_row
