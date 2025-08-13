class Phenotype:
    """
        A wrapper class for the genotype class representing an individual antenna's phenotype.

           Attributes:
               id (str): The individual's unique ID.
               parent1_id (str): The ID of parent1 of the individual.
               parent2_id (str): The ID of parent2 of the individual.
               generation_created (int): Which generation the individual was created.
               fitness_score (float): The fitness score of the individual.
           """

    def __init__(self, id, parent1_id, parent2_id, generation_created, fitness_score):
        """
            Initializes a Phenotype object.

                Parameters:
                    id (str): The individual's unique ID.
                    parent1_id (str): The ID of parent1 of the individual.
                    parent2_id (str): The ID of parent2 of the individual.
                    generation_created (int): Which generation the individual was created.
                    fitness_score (float): The fitness score of the individual.
                """

        self.id = id
        self.parent1_id = parent1_id
        self.parent2_id = parent2_id
        self.generation_created = generation_created
        self.fitness_score = fitness_score