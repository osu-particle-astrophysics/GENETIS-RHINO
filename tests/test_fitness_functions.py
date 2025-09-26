from src.GENETIS_RHINO.fitness_functions import calculate_fitnesses


def test_fitness_function():
    results = calculate_fitnesses("tests/assets/uan_example/0")