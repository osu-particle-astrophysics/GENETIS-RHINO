"""Abstract Evolver class defines the interface for all evolvers (e.g. NSGA-II, Lexicase, etc.)."""

import random
from abc import ABC, abstractmethod

from src.Phenotype import Phenotype
from src.Selectors import NSGATournament


class AbstractEvolver(ABC):
    """Evolvers perform everything needed to select and manage populations of individuals."""

    @abstractmethod
    def evolve(self, population: list[Phenotype], generation_num: int, rand: random.Random) -> list[Phenotype]:
        """Take in a population and return a new population that has undergone selection and mutation."""


class NSGA2(AbstractEvolver):
    """Implemented evolver for the Non-dominated Sorting Genetic Algorithm."""

    def evolve(self, population: list[Phenotype], generation_num: int, rand: random.Random) -> list[Phenotype]:
        """
        Do one generation of NSGA-II.

        Steps:
        1. Assign ranks and distances to all individuals.
        2. Generate offspring equal to the size of the pop using binary tournament.
        3. Merge the offspring and old population.
        4. Truncate the lower half (according to rank and crowding distance).
        """
        pop_size = len(population)

        # Assign ranks and distances
        fronts = fast_non_dominated_sort(population)
        for front in fronts:
            crowding_distance_assignment(front)

        # Generate offspring
        offspring = []
        for i in range(pop_size):
            parent1 = NSGATournament.select_one(population, rand)
            # uncomment these lines for crossover
            #parent2 = NSGATournament.select_one(population, rand)
            new_child_id = generation_num*pop_size + i
            #child = parent1.make_offspring(new_child_id, parent2)
            child = parent1.make_offspring(new_child_id, rand)
            child.generation_created = generation_num

            offspring.append(child)

        # Combine parents + offspring
        combined = population + offspring

        # Re-sort and truncate to pop_size for elitism
        fronts = fast_non_dominated_sort(combined)
        new_pop = []
        for front in fronts:
            crowding_distance_assignment(front)
            if len(new_pop) + len(front) <= pop_size:
                new_pop.extend(front)
            else:
                front.sort(key=lambda ind: ind.nsgaii_distance, reverse=True)
                new_pop.extend(front[: pop_size - len(new_pop)])
                break

        return (new_pop)

### Helper functions for NSGAII
def fast_non_dominated_sort(population: list) -> list[list]:
    """Assigns NSGA-II Pareto rank to each individual in the population. Lower rank = better front."""
    fronts: list[list] = [[]]

    # For every individual get who it dominates, and how many it is dominated by
    for indiv in population:
        indiv.dominated_set = []
        indiv.domination_count = 0

        for q in population:
            if indiv is q:
                continue

            if dominates(indiv, q):
                indiv.dominated_set.append(q)
            elif dominates(q, indiv):
                indiv.domination_count += 1

        # If you're not dominated by anyone, you go in the first front
        if indiv.domination_count == 0:
            indiv.nsgaii_rank = 0
            fronts[0].append(indiv)

    i = 0
    while fronts[i]:
        next_front = []
        # For each individual in the current front
        for indiv in fronts[i]:
            # If this individual dominates a solution, reduce that solution's domination count by one
            for q in indiv.dominated_set:
                q.domination_count -= 1
                # If the solution has nobody left dominating it, it belongs in the next front
                if q.domination_count == 0:
                    q.nsgaii_rank = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    return fronts[:-1]

def dominates(p: Phenotype, q: Phenotype) -> bool:
    """
    Returns True if individual p dominates q (minimization).

    Args:
    p (Phenotype): First individual to compare
    q (Phenotype): Second individual to compare

    """
    p_better_or_equal = all(p.fitness[obj] <= q.fitness[obj] for obj in p.fitness)
    p_strictly_better = any(p.fitness[obj] < q.fitness[obj] for obj in p.fitness)
    return p_better_or_equal and p_strictly_better

def crowding_distance_assignment(front: list) -> None:
    """
    Assigns NSGA-II crowding distance to individuals in a front. Larger distance = more diversity.

    Args: front: A collection of individuals on the same front
    """
    if len(front) == 0:
        return
    if len(front) == 1:
        front[0].nsgaii_distance = float("inf")
        return
    num_for_double_front = 2
    if len(front) == num_for_double_front:
        front[0].nsgaii_distance = float("inf")
        front[1].nsgaii_distance = float("inf")
        return

    for indiv in front:
        indiv.nsgaii_distance = 0.0

    # For every objective
    for obj in front[0].fitness:
        # Sort the front for this objective
        front.sort(key=lambda indiv: indiv.fitness[obj])
        # Get the max and min for normalization
        f_min = front[0].fitness[obj]
        f_max = front[-1].fitness[obj]

        # If equal we will get division by zero, so skip
        if f_max == f_min:
            continue

        # Boundary points get infinite distance
        front[0].nsgaii_distance = float("inf")
        front[-1].nsgaii_distance = float("inf")

        # For every point in the front
        for i in range(1, len(front) - 1):
            if front[i].nsgaii_distance != float("inf"):
                # Get the two closest points
                prev_f = front[i - 1].fitness[obj]
                next_f = front[i + 1].fitness[obj]
                # Assign normalized crowding distance
                front[i].nsgaii_distance += (next_f - prev_f) / (f_max - f_min)
