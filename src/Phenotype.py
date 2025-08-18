from src.Genotype import Genotype

#TODO is there anything else I need to do to make this formally a wrapper class?
class Phenotype:
    """
    A wrapper for the genotype class representing an individual antenna's phenotype.

    Attributes:
        id (str): The individual's unique ID.
        parent1_id (str): The ID of parent1 of the individual. Use id "None1" if no parent1.
        parent2_id (str): The ID of parent2 of the individual. Use id "None2" if no parent2.
        generation_created (int): Which generation the individual was created.
        fitness_score (float): The fitness score of the individual.
    """

    def __init__(self, genotype, id, parent1_id, parent2_id, generation_created, fitness_score):
        """
        Initializes a Phenotype object.

        Parameters:
            genotype (Genotype): The genotype of the individual. Must be a Genotype object.
            id (str): The individual's unique ID.
            parent1_id (str): The ID of parent1 of the individual. Use id "None1" if no parent1.
            parent2_id (str): The ID of parent2 of the individual. Use id "None2" if no parent2.
            generation_created (int): Which generation the individual was created.
            fitness_score (float): The fitness score of the individual.
        """
        # Make sure the genotype provided to the constructor is valid. Exit program if invalid.
        if not isinstance(genotype, Genotype):
            raise TypeError("The genotype provided to Phenotype constructor is not a valid Genotype object.")

        # Make sure either has no parents or both parents.
        if parent1_id.startswith("None") != parent2_id.startswith("None"):
            raise ValueError('A phenotype can only have no parents or both parents.')

        self.genotype = genotype
        self.id = str(id)
        self.parent1_id = str(parent1_id)
        self.parent2_id = str(parent2_id)
        self.generation_created = int(generation_created)
        self.fitness_score = float(fitness_score)

        #TODO check id and parent ids are valid

        #TODO check generation created is valid

        #TODO check fitness score is valid
