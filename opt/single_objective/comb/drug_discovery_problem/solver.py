import random
import re
import sys
import os
import contextlib
from typing import Generator, List, Optional
from rdkit import Chem
from opt.single_objective.comb.drug_discovery_problem.mutation_info import MutationInfo
from .individual import Individual

from PyQt5.QtWidgets import QLabel, QProgressBar

def genetic_algorithm(
    population: List[Individual],
    only_one_generation: bool,
    number_of_generations: int,
    roulette_selection: bool,
    tournament_size: int,
    elitism_size: int,
    mutation_probability: float,
    mi: MutationInfo,
    individual_label: QLabel,
    individual_progress: QProgressBar
) -> List[Individual]:
    """
    Genetic algorithm for molecule evolution.

    :param population: Initial population of individuals
    :param only_one_generation: If True, run only one generation regardless of number_of_generations
    :param number_of_generations: Total number of generations to evolve
    :param roulette_selection: Whether to use roulette wheel selection or tournament selection
    :param tournament_size: Size of the tournament if tournament selection is used
    :param elitism_size: Number of elite individuals preserved between generations
    :param mutation_probability: Probability of mutation
    :param mi: Mutation information structure
    :param individual_label: Label object for GUI update
    :param individual_progress: Progress bar object for GUI update
    :return: Evolved population after all generations
    :rtype: List[`Individual`]
    """
    population_size = len(population)
    new_population = population.copy()

    if only_one_generation:
        number_of_generations = 1

    if elitism_size % 2 != population_size % 2:
        elitism_size += 1

    for _ in range(number_of_generations):
        new_population[:elitism_size] = population[:elitism_size]
        tmp = 0
        for j in range(elitism_size, population_size, 2):
            parent1 = selection(population, roulette_selection, tournament_size)
            parent2 = selection(population, roulette_selection, tournament_size)

            crossover(parent1, parent2, child1 = new_population[j], child2 = new_population[j + 1])

            mutation(new_population[j], mutation_probability, mi)
            mutation(new_population[j + 1], mutation_probability, mi)

            new_population[j].set_description("")
            new_population[j]._calculate_fitness()
            new_population[j + 1].set_description("")
            new_population[j + 1]._calculate_fitness()

            individual_label.setText(f"Individual: {j+1}/{population_size}")
            individual_progress.setValue(j + 1)
            tmp = j

        population = new_population.copy()
        individual_label.setText(f"Individual: {tmp + 2}/{population_size}")
        individual_progress.setValue(tmp + 2)

    return population

def selection(
    population: List[Individual], roulette_selection: bool, tournament_size: int
) -> Individual:
    """
    Select an individual from the population.

    :param population: Current population
    :param roulette_selection: Whether to use roulette selection
    :param tournament_size: Tournament size if using tournament selection
    :return: Selected individual
    :rtype: `Individual`
    """
    if roulette_selection:
        return roulette_wheel_selection(population)
    return tournament_selection(population, tournament_size)

def roulette_wheel_selection(population: List[Individual]) -> Individual:
    """
    Roulette wheel selection based on QED.

    :param population: Population to select from
    :return: Selected individual
    :rtype: `Individual`
    """
    total_fitness = sum(ind.get_qed() for ind in population)
    probabilities = []
    acc = 0
    for ind in population:
        acc += ind.get_qed() / total_fitness
        probabilities.append(acc)

    rnd = random.random()
    for i, p in enumerate(probabilities):
        if rnd <= p:
            return population[i]
    return population[-1]

def tournament_selection(population: List[Individual], tournament_size: int) -> Individual:
    """
    Tournament selection based on QED.

    :param population: Population to select from
    :param tournament_size: Number of individuals in tournament
    :return: Best individual from tournament
    :rtype: `Individual`
    """
    sample = random.sample(population, tournament_size)
    return max(sample, key=lambda ind: ind.get_qed())

@contextlib.contextmanager
def suppress_rdkit_warnings() -> Generator[None, None, None]:
    """
    Context manager to suppress RDKit warnings/errors.
    """
    original_stdout, original_stderr = sys.stdout, sys.stderr
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    try:
        yield
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr

def is_valid_smiles(smiles: str) -> bool:
    """
    Validate SMILES string.

    :param smiles: SMILES string
    :return: True if valid, False otherwise
    :rtype: `bool`
    """
    with suppress_rdkit_warnings():
        mol = Chem.MolFromSmiles(smiles)
    return mol is not None

def crossover(parent1: Individual, parent2: Individual, child1: Individual, child2: Individual) -> None:
    """
    Perform crossover on two parent individuals to generate two child individuals.

    :param parent1: First parent individual
    :param parent2: Second parent individual
    :param child1: First child individual (result)
    :param child2: Second child individual (result)
    :rtype: None
    """

    # Assuming smiles strings have more than 1 character (in order to be eligible for crossover)
    smiles1: str = parent1.get_smiles()
    smiles2: str = parent2.get_smiles()
    n1: int = len(smiles1)
    n2: int = len(smiles2)
    MAXITERS: int = 2000
    i: int = 0
    while i < MAXITERS:
        i += 1
        cp1: int = random.randrange(1, n1)
        cp2: int = random.randrange(1, n2)

        child_smiles1: str = smiles1[:cp1] + smiles2[cp2:]
        child_smiles2: str = smiles1[cp1:] + smiles2[:cp2]

        if is_valid_smiles(child_smiles1) and is_valid_smiles(child_smiles2):
            child1.set_smiles(child_smiles1)
            child2.set_smiles(child_smiles2)
            break
    
    if i == MAXITERS:
        print('Maximum number of iterations for crossover of following molecules exceeded:\n')
        print(f'{smiles1}\n{smiles2}\n')
        print('Attempting two point crossover...')

    i = 0
    while i < MAXITERS:
        i += 1
        first1: int = random.randrange(1, n1)
        if first1 < n1 - 1:
            first2: int = random.randrange(first1 + 1, n1)
        else:
            first2: int = random.randrange(1, first1)
            # first2 < first1, so swap them
            first1, first2 = first2, first1

        second1: int = random.randrange(1, n2)
        if second1 < n2 - 1:
            second2: int = random.randrange(second1 + 1, n2)
        else:
            second2: int = random.randrange(1, second1)
            # second2 < second1, so swap them
            second1, second2 = second2, second1

        child_smiles1 = smiles1[:first1] + smiles2[second1:second2] + smiles1[first2:]
        child_smiles2 = smiles2[:second1] + smiles1[first1:first2] + smiles2[second2:]

        if is_valid_smiles(child_smiles1) and is_valid_smiles(child_smiles2):
            child1.set_smiles(child_smiles1)
            child2.set_smiles(child_smiles2)
            break

    if i == MAXITERS:
        print('Maximum number of iterations for two point crossover of following molecules exceeded:\n')
        print(f'{smiles1}\n{smiles2}\n')
        print('Passing them to the new generation.\n')
        child1.set_smiles(smiles1)
        child2.set_smiles(smiles2)

def mutation(individual: Individual, mutation_probability: float, mi: MutationInfo) -> None:
    """
    Mutate an individual with a given mutation probability.

    :param individual: The individual to mutate
    :param mutation_probability: Probability of mutation
    :param mi: MutationInfo object with mutation rules
    :rtype: None
    """
    if random.random() > mutation_probability:
        return

    # Mutation will take place
    mutation_type: int = random.randrange(0, 4)
    # 0 - atom switch
    # 1 - group switch
    # 2 - insertion of an atom or a group
    # 3 - deletion of an atom or a group

    if mutation_type == 0:
        atom_switch_mutation(individual, mi)
    elif mutation_type == 1:
        group_switch_mutation(individual, mi)
    elif mutation_type == 2:
        insertion_mutation(individual, mi)
    else:
        deletion_mutation(individual, mi)

def atom_switch_mutation(individual: Individual, mi: MutationInfo) -> None:
    """
    Perform atom switch mutation.

    :param individual: The individual to mutate
    :param mi: MutationInfo with atom switch map
    :rtype: None
    """
    smiles: str = individual.get_smiles()
    hetero_atoms: List[str] = ['O', 'S', 'N', 'P']
    indices_of_hetero_atoms: List[int] = []
    for i, ch in enumerate(smiles):
        if ch in hetero_atoms:
            indices_of_hetero_atoms.append(i)

    if len(indices_of_hetero_atoms) == 0:
        # Can't perform hetero atom switching
        group_switch_mutation(individual, mi)
        return
    random_hetero_index: int = random.randrange(len(indices_of_hetero_atoms))
    hetero_atom: str = smiles[indices_of_hetero_atoms[random_hetero_index]]

    rnd: float = random.random()
    cum_prob: float = 0 # cumulative probability, similar to roulette selection
    change_with: str = hetero_atom
    for (second, prob) in mi.atom_switch_map[hetero_atom]:
        cum_prob += prob
        if rnd <= cum_prob:
            change_with = second
            break
    smiles = smiles[:indices_of_hetero_atoms[random_hetero_index]] + change_with + smiles[indices_of_hetero_atoms[random_hetero_index] + 1:]
    individual.set_smiles(smiles)

def group_switch_mutation(individual: Individual, mi: MutationInfo) -> None:
    """
    Perform group switch mutation.

    :param individual: The individual to mutate
    :param mi: MutationInfo with group switch map
    :rtype: None
    """
    smiles: str = individual.get_smiles()
    modified_smiles: List[str] = []

    # try with all known group mutations, and pick a random one
    for replace_from, options in mi.group_switch_map.items():
        for replace_with in options:
            # Find all the start positions of replaceFrom in smiles
            matches: List[int] = [match.start() for match in re.finditer(re.escape(replace_from), smiles)]
            if not matches:
                continue
            
            # Generate all replacements by replacing each occurrence of smilesFrom
            for match in matches:
                # Replace only the specific occurrence at the current position
                mod_smiles = smiles[:match] + replace_with + smiles[match + len(replace_from):]
                modified_smiles.append(mod_smiles)

    new_smiles: str = smiles
    if len(modified_smiles) > 0:
        new_smiles = random.choice(modified_smiles)
    individual.set_smiles(new_smiles)
    
def insertion_mutation(individual: Individual, mi: MutationInfo) -> None:
    """
    Perform insertion mutation.

    :param individual: The individual to mutate
    :param mi: MutationInfo with list of insertions
    :rtype: None
    """
    smiles: str = individual.get_smiles()
    n: int = len(smiles)
    MAX_INSERTION_ATTEMPTS: int = 200
    random_insertion: str = random.choice(mi.insertions)
    i: int = 0
    while i < MAX_INSERTION_ATTEMPTS:
        i += 1
        random_insertion_position: int = random.randrange(n)
        new_smiles: str = smiles[:random_insertion_position] + random_insertion + smiles[random_insertion_position:]
        if is_valid_smiles(new_smiles):
            individual.set_smiles(new_smiles)
            return

    # Insertion failed, in order to perform any other mutation, call deletionMutation (for example)
    deletion_mutation(individual, mi)

def deletion_mutation(individual: Individual, mi: MutationInfo) -> None:
    """
    Perform deletion mutation.

    :param individual: The individual to mutate
    :param mi: MutationInfo (not used but included for consistency)
    :rtype: None
    """
    smiles: str = individual.get_smiles()
    n: int = len(smiles)
    MAX_BRANCH_DELETION_ATTEMPTS: int = 20
    MAX_ITERS: int = 500
    open_brackets_positions: List[int] = []
    for i, ch in enumerate(smiles):
        if ch == '(':
            open_brackets_positions.append(i)

    # Branches in the molecule exist
    if len(open_brackets_positions) > 0:
        # Attempt deleting random branches of a molecule
        for _ in range(MAX_BRANCH_DELETION_ATTEMPTS):
            start_index: int = random.choice(open_brackets_positions)
            open_brackets: int = 1
            end_index: int = None
            # Finding the corresponding closed bracket
            for i in range(start_index + 1, n):
                if smiles[i] == '(':
                    open_brackets += 1
                if smiles[i] == ')':
                    open_brackets -= 1
                    if open_brackets == 0:
                        end_index = i
                        break

            new_smiles: str = smiles[:start_index] + smiles[end_index + 1:]
            if is_valid_smiles(new_smiles):
                individual.set_smiles(new_smiles)
                return

    # Else: zero branches in the molecule, or branches can not be deleted
    i: int = 0
    while i < MAX_ITERS:
        i += 1
        random_index: int = random.randrange(n)
        # We only want to delete atoms
        if smiles[random_index].isalpha():
            new_smiles = smiles[:random_index] + smiles[random_index + 1:]
            if is_valid_smiles(new_smiles):
                individual.set_smiles(new_smiles)
                break
    # Single atom deletion didn't succeed neither, hence, in order not to leave the molecule unchanged, we call
    # atom switch mutation. In case it also fails, that method will call group mutation, which will not fail,
    # since there are certain mutations that will always succeed.
    if i == MAX_ITERS:
        atom_switch_mutation(individual, mi)