# Initialisation
#    Tu generes aleatoirement une population de 50 individus, par exemple.
# Evaluation (Fitness)
#    Chaque individu correspond a une IA. Tu mesures ses performances en faisant jouer plusieurs parties.
# Selection
#    Tu selectionnes les individus les plus performant pour devenir les parents de la generation suivante.
# Croisement (Crossover)
#    Tu combines les poids de deux parents pour creer un nouvel individu.
# Mutation
#    Tu modifies aleatoirement quelques poids pour introduire de nouvelles possibilites.
from src.ai.weights import generate_weights
from src.genetic.evaluation import fitness
from src.genetic.initialisation import generate_population
from src.genetic.selection import select_bests


POPULATION_SIZE = 50


def train():

    individuals = generate_population(POPULATION_SIZE)
    reference = generate_weights()
    opponents = generate_population(2) + [reference]

    strenghts: list[float] = []
    for individual in individuals:
        strenghts.append(fitness(individual, opponents))

    bests = select_bests(individuals, strenghts)
    