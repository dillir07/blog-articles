import random
import math
from random import randint

all_cities = []


def generate_cities(number_of_cities, map_limit):
    # print("######################################################")
    # print("Generate Cities Called")
    cities = []
    for city_counter in range(number_of_cities):
        cities.append(
            {"id": city_counter, "x": random.randint(
                map_limit), "y": random.randint(map_limit)
             }
        )

    print("Cities Generated:", len(cities))
    return cities


def shuffle_chromosome(chromosome):
    for i in range(len(chromosome)):
        random_point = random.randint(len(chromosome))
        chromosome[i], chromosome[random_point] = chromosome[random_point], chromosome[i]

        print("Created chromosome", chromosome)
    return chromosome


def calculate_distance_between_two_points(point1, point2):
    return math.sqrt((((point2[1] - point1[1]))**2) + (((point2[2] - point1[2]))**2))


def calculate_chromosome_travel_distance(chromosome):
    travel_distance = 0
    for geneId in len(chromosome):
        point1 = (all_cities[chromosome[geneId]]["x"],
                  all_cities[chromosome[geneId]]["y"])
        point2 = (all_cities[chromosome[geneId + 1]]["x"],
                  all_cities[chromosome[geneId + 1]]["y"])
        travel_distance += calculate_distance_between_two_points(
            point1, point2)

        print("travel distance:", chromosome, " : ", travel_distance)
    return travel_distance


def generate_initial_population(initial_population_size):
    """
    Generates Initial Population
    """
    chromosomes = []
    for population_counter in range(initial_population_size):
        chromosome = shuffle_chromosome(initial_chromosome)
    chromosomes.append(
        {
            "chromosome": chromosome,
            "distance": calculate_chromosome_travel_distance(chromosome)
        }
    )

    return chromosomes


def crossover(parent_one_chromosome, parent_two_chromosome, crossover_point):
    print("crossover: ", parent_one_chromosome, " ", parent_two_chromosome)
    offspring_part_one = parent_one_chromosome[1:crossover_point]
    for gene in offspring_part_one:
        if gene in parent_two_chromosome:
            gene_loc = parent_two_chromosome
            splice!(parent_two_chromosome, gene_loc)

    return offspring_part_one + parent_two_chromosome


def mutate(offspring):
    print("mutate: ", offspring)
    random_mutation_point1 = random.randint(offspring)
    random_mutation_point2 = random.randint(offspring)
    offspring[random_mutation_point1], offspring[random_mutation_point2] = offspring[random_mutation_point2], offspring[random_mutation_point1]
    return offspring


def evolve(generation_count, offsprings_count, crossover_point):
    for generation in range(generation_count):
        for offspring_count in range(offsprings_count):
            print("generation: ", generation, " offspring: ", offspring_count)
            random_parent_one_id = random.choice(chromosomes)
            random_parent_two_id = random.choice(chromosomes)
            random_parent_one = chromosomes[random_parent_one_id]["chromosome"].copy()
            random_parent_two = chromosomes[random_parent_two_id]["chromosome"].copy()
            offspring = crossover(random_parent_one, random_parent_two, crossover_point)
            offspring = mutate(offspring)
            chromosomes.append({
                "chromosome": offspring, "distance": calculate_chromosome_travel_distance(offspring)
            })
            sorted(chromosomes)
            print("BEST: ", chromosomes[1])
            chromosomes = chromosomes[:number_of_cities]


number_of_cities = 10
all_cities = generate_cities(10, number_of_cities)
initial_chromosome = [_ for _ in range(1, all_cities)]
print("initial_chromosome:", initial_chromosome)
print()
chromosomes = generate_initial_population(10)
evolve(5, 5, 2)
print("CHOOSEN: ", chromosomes[1])
