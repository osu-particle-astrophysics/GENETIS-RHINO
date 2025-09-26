"""Dummy fittness func for alpha version of software."""
from src.GENETIS_RHINO.genotype import Genotype


class DummyFitnessFunc:
    """Turns genotype parameters into dictionary of fitness scores."""

    def __init__(self, genotype: Genotype) -> None:
        """Constructor."""
        self.fitness_scores = { "flare_length": genotype.flare_length,
                                "waveguide_height": genotype.waveguide_height,
                                "waveguide_length": genotype.waveguide_length,
                                "waveguide_width": genotype.waveguide_width,
                                }
        i = 0
        for wp in genotype.walls:
            key = "wp" + str(i) + "_angle"
            self.fitness_scores[key] = wp.angle

            key = "wp" +str(i) + "_ridge_height"
            self.fitness_scores[key] = wp.ridge_height

            key = "wp" + str(i) + "_ridge_width_top"
            self.fitness_scores[key] = wp.ridge_width_top

            key = "wp" + str(i) + "_ridge_width_bottom"
            self.fitness_scores[key] = wp.ridge_width_bottom

            key = "wp" + str(i) + "_ridge_thickness_top"
            self.fitness_scores[key] = wp.ridge_thickness_top

            key = "wp" + str(i) + "_ridge_thickness_bottom"
            self.fitness_scores[key] = wp.ridge_thickness_bottom

            i = i + 1

    def get_fitness_scores(self) -> dict:
        """Returns dict of dummy fitness scores."""
        return self.fitness_scores
