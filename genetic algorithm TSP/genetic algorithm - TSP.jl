"""
Travelling Salesman problem (TSP):
    The travelling salesman problem (TSP) asks the following question:
    "Given a list of cities and the distances between each pair of cities,
    what is the shortest possible route that visits each city exactly once
    and returns to the origin city?".

Genetic Algorithm:
    genetic algorithm (GA) is a metaheuristic inspired by the process
    of natural selection that belongs to the larger class
    of evolutionary algorithms (EA).
    Genetic algorithms are commonly used to generate high-quality solutions
    to optimization and search problems by relying on
    biologically inspired operators such as mutation, crossover and selection. 
"""


"""
# Generate cities:
Generates given `number_of_cities randomly`, with in given `map_limit`
# Arguments:
- `number_of_cities::Integer`: number of cities to generate
- `map_limit::Integer=1`: map size limit for cities
"""
function generate_cities(number_of_cities, map_limit)

	cities = []
    for city_counter in 1:number_of_cities
        push!(cities, 
            Dict(
                "id" => city_counter, 
                "x" => round(rand() * map_limit), 
                "y" => round(rand() * map_limit)
            )
        )
    end
	println("Cities Generated:", size(cities)[1])
	return cities
end

"""
# Shuffle chromosome:
Takes an array of integers and returns in shuffed order

# Arguments:
- `chromosome` - Array of integers
```julia
[1,2,3,4,5]
```

# Returns:
- `chromosome` - Shuffled integers
```julia
[2,1,4,3,5]
```

"""
function shuffle_chromosome(chromosome)
    for i in 1:size(chromosome)[1]
        random_point = rand(1:5, 1)[1]
        chromosome[i], chromosome[random_point] = chromosome[random_point], chromosome[i]
    end
    
	println("Created chromosome", chromosome)
    return chromosome
end

"""
# Calculate distance between two points
Calculates distance between two points in 2d plane

uses formula 
"""
function calculate_distance_between_two_points(point1, point2)
    return sqrt((((point2[1] - point1[1]))^2) + (((point2[2] - point1[2]))^2))
end

"""
# calculate chromosome travel distance
calculates total travel distance for given chromosome

Returns:
- `travel_distance::Float`
"""
function calculate_chromosome_travel_distance(chromosome)
    travel_distance = 0
    chromosome = vcat(1, chromosome, 1)
    for geneId in 1:length(chromosome) - 1
        point1 = (cities[chromosome[geneId]]["x"], cities[chromosome[geneId]]["y"])
        point2 = (cities[chromosome[geneId + 1]]["x"], cities[chromosome[geneId + 1]]["y"])
        travel_distance += calculate_distance_between_two_points(point1, point2)
	end
	println("travel distance:", chromosome, " : ", travel_distance)
    return travel_distance
end

"""
# generate_initial_population
Generates initial population, by creating give number of size
"""
function generate_initial_population(initial_population_size)
	chromosomes = []
    for population_counter in 1:initial_population_size
        chromosome = shuffle_chromosome(copy(initial_chromosome))
        push!(chromosomes, Dict("chromosome" => chromosome, "distance" => calculate_chromosome_travel_distance(chromosome)))
    end
	return chromosomes
end

"""
# crossover
Here we take two chromosomes and generate new chromosome off of it
"""
function crossover(parent_one_chromosome, parent_two_chromosome, crossover_point)
	# println("crossover: ", parent_one_chromosome, " ", parent_two_chromosome)
	offspring_part_one = parent_one_chromosome[1:crossover_point]
	for gene in offspring_part_one
		if gene in parent_two_chromosome
			gene_loc = findfirst(el -> el == gene, parent_two_chromosome)
			splice!(parent_two_chromosome, gene_loc)
		end
	end
	return vcat(offspring_part_one, parent_two_chromosome)
end

"""
# mutate
Here we mutate the generated chromosome by swapping two elements
"""
function mutate(offspring)
	# println("mutate: ", offspring)
	random_mutation_point1 = rand(1:length(offspring))
    random_mutation_point2 = rand(1:length(offspring))
	offspring[random_mutation_point1], offspring[random_mutation_point2] = offspring[random_mutation_point2], offspring[random_mutation_point1]
	return offspring
end

function evolve(generation_count, offsprings_count, crossover_point)
	for generation in 1:generation_count
		
		for offspring_count in 1:offsprings_count
			println("generation: ", generation, " offspring: ", offspring_count)
			random_parent_one_id = rand(1:size(chromosomes)[1])
			random_parent_two_id = rand(1:size(chromosomes)[1])
			random_parent_one = copy(chromosomes[random_parent_one_id]["chromosome"])
			random_parent_two = copy(chromosomes[random_parent_two_id]["chromosome"])
			offspring = crossover(random_parent_one, random_parent_two, crossover_point)
			offspring = mutate(offspring)
            push!(chromosomes, 
                Dict(
                    "chromosome" => offspring,
                    "distance" => calculate_chromosome_travel_distance(offspring)
                    )
            )
		end
		sort!(chromosomes, by=x -> x["distance"], rev=false)
		splice!(chromosomes, 6:size(chromosomes)[1])
	end
end

cities = generate_cities(10, 500)
display(cities)
println()
println()

# here we are creating initial chromosome from 2 because, we will always start from 1
# and we don't want gene 1 to be shuffled, while randomizing

initial_chromosome = [2:length(cities);]
println("initial_chromosome:", initial_chromosome)
println()

chromosomes = generate_initial_population(10)
evolve(5, 5, 2)
println("--------------------------------------------------------")
println("Optimal route:", vcat(1, chromosomes[1]["chromosome"], 1))
println("travel_distance:", chromosomes[1]["distance"])