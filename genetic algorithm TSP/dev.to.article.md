# Genetic Algorithm
Genetic algorithm is a method of mimicking natural section and survival of fittest to find optimal solutions to problems, which otherwise would be too difficult to solve.

# Travelling Salesman Problem
Travelling Salesman Problem or TSP for short, is a infamous problem where a travelling sales person has to travel various cities with known distance and return to the origin city in the shortest time/path possible.

First lets try to brute force to solve the problem.
for starters lets take 5 cities, i.e., we have to calculate 5!, i.e., 120 routes to ensure we got the shortest path.

Now, if we are to do that for 20 cities,
-  5! = 120
- 10! = 3628800
- 15! = 1307674368000
- 20! = 2432902008176640000
- 50! = 30414093201713378043612608166064768844377641568960512000000000000

We can see how brute forcing our way is simply not going to be helpful here.

So, we will see how Genetic Algorithm can help us find a optimal shortest path here.

In simple, Genetic Algorithm works the following way,
- Choosing Random initial solutions/chromosomes (Called as Initial Population or Chromosomes)
- crossover (generating new solution or chromosome, by kind of mixing two parent chromosomes/solutions)
- mutate (making a minor change in the solution)
- fitness check (checking if the solution is useful or fullfills our requirement)

So.. for our problem, we will do the following:

## Create a map, with bunch of cities at random location

```julia
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
# calling generate_cities method to create cities
generate_cities(5,500)
```

We are storing the city as a Dictionary, so for 5 cities we get:
Each city has an id, and `(x,y)` location

```bash
 ("id" => 1,"x" => 480.0,"y" => 157.0)
 ("id" => 2,"x" => 4.0,"y" => 465.0)
 ("id" => 3,"x" => 57.0,"y" => 25.0)
 ("id" => 4,"x" => 411.0,"y" => 322.0)
 ("id" => 5,"x" => 44.0,"y" => 460.0)
```

## Representing the solution as chromosome.

the solution for our problem is route from one city to another city. We can write it as an array of integers, where each number represents a city id.

```julia
[1,2,5,4,3,1]
```

So, for above mentioned route or chromosome, we are starting from city1 -> city 2 and so on... finally coming back to city1.

## Crossover function

Here generate a new chromosome by taking values from two parent chromosomes.
For this problem we simply have to ensure the genes/city id is not getting repeated, while generating new chromosome.

There a many ways to do a crossover like, Unipoint crossover, multi-point crossover, etc.
We will do a unipoint crossover, where we choose a random point in gene and do a simple swap to create new chromosome.

```julia
function crossover(parent_one_chromosome, parent_two_chromosome, crossover_point)
	offspring_part_one = parent_one_chromosome[1:crossover_point]
	for gene in offspring_part_one
		if gene in parent_two_chromosome
			gene_loc = findfirst(el -> el == gene, parent_two_chromosome)
			splice!(parent_two_chromosome, gene_loc)
		end
	end
	return vcat(offspring_part_one, parent_two_chromosome)
end
```

## Mutation function

In simple terms mutation can be defined as making a random change in the chromosome.
Here we will simply swap two gene's positions.

```julia
function mutate(offspring)
	println("mutate: ", offspring)
	random_mutation_point1 = rand(1:length(offspring))
    random_mutation_point2 = rand(1:length(offspring))
	offspring[random_mutation_point1], offspring[random_mutation_point2] = offspring[random_mutation_point2], offspring[random_mutation_point1]
	return offspring
end
```

## Fitness function

Fitness function's responsibility is to calculate each chromosome's score, so that we can decide if we want to use this
chromosome in next generation or to discard.

For our problem, the score is the travel distance for a given route/chromosome. The lower the travel distance the better.

To calculate the travel distance, we simple start from 1st city, go to next and then to next, so..on and return to origin city, by adding the distance we travelled, we get the score of this particular route.

```julia
function calculate_distance_between_two_points(point1, point2)
    return sqrt((((point2[1] - point1[1]))^2) + (((point2[2] - point1[2]))^2))
end

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
```

## Generating intial population:
We will define a function that can generate initial populations.

```julia
function generate_initial_population(initial_population_size)
	chromosomes = []
    for population_counter in 1:initial_population_size
        chromosome = shuffle_chromosome(copy(initial_chromosome))
        push!(chromosomes, 
            Dict(
                "chromosome" => chromosome,
                "distance" => calculate_chromosome_travel_distance(chromosome)
            )
        )
    end
	return chromosomes
end
```

```bash
[3, 9, 4, 8, 10, 5, 1, 2, 7, 6]
[8, 1, 6, 9, 10, 5, 2, 4, 3, 7]
[2, 9, 10, 8, 5, 4, 6, 1, 3, 7]
[5, 6, 10, 7, 4, 3, 1, 2, 8, 9]
[2, 10, 9, 4, 6, 5, 1, 3, 8, 7]
```

## main part

This is where we run decide our number_of_generations, number_of_chromosomes per generation, initial_population_size etc.

So, we start by creating an initial population, few random solutions.

Then we randomly choose two parents and do a crossover by calling crossover function.
Then mutate the generated chromosome by calling mutate function
Then we calculate the travel distance by calling calculate_chromosome_travel_distance

We then sort the chromosomes based on it's travel distance in assending order. (remember the the lower the score is the better)

Then we keep five chromosomes with lowest travel distance and proceed again for as many generations we want.
For each generation the travel distance will get reduced i.e., the path gets optimized.

We stop once we are statisfied with the results or if there is not significant improvement.

```julia
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
			push!(chromosomes, Dict("chromosome" => offspring, "distance" => calculate_chromosome_travel_distance(offspring)))
		end
		sort!(chromosomes, by=x -> x["distance"], rev=false)
		splice!(chromosomes, 6:size(chromosomes)[1])
	end
end
```