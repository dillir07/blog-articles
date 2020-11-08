# Genetic Algorithm
Genetic algorithm (GA) is a type of algorithm inspired by the process of natural selection to generate high-quality solutions to problems, which otherwise would be too difficult to solve.

# Travelling Salesman Problem
Travelling Salesman Problem or TSP for short, is a infamous problem where a travelling sales person has to travel various cities with known distance and return to the origin city in the shortest time/path possible.

Like below, each circle is a city and blue line is a route, visiting them.

![TSP City map](https://dev-to-uploads.s3.amazonaws.com/i/84o5cwq9on4o4z15ostt.png)

## Why not brute-force ??

Okay, lets try to brute force to solve the problem.
for starters lets take 5 cities, i.e., we have to calculate `5!`, i.e., 120 routes to ensure we got the shortest path.

Now, if we are to do that for `50` cities,
-  `5!` = 120
- `10!` = 3628800
- `15!` = 1307674368000
- `20!` = 2432902008176640000
- `50!` = 30414093201713378043612608166064768844377641568960512000000000000

We can see how brute forcing our way is simply not going to be helpful here.

## Let's try GA

So, we will see how `Genetic Algorithm` can help us find a optimal shortest path here.

In simple, Genetic Algorithm works the following way,
- Choosing Random initial solutions/chromosomes (Called as `Initial Population` or Chromosomes)
- `crossover` (generating new solution or chromosome, by kind of mixing two parent chromosomes/solutions)
- `mutate` (making a minor change in the solution)
- `fitness` (checking if the solution is useful or fullfills our requirement), if yes, we use them to create new offsprings (parents in next generation) and the cycle continues for an many generations we want.

So.. for our `TSP` problem, we will do the following:

## Generate Cities

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

We are storing the city as a Dictionary.

Each city has an `id`, and `(x,y)` location

```julia
 ("id" => 1,"x" => 480.0,"y" => 157.0)
 ("id" => 2,"x" => 4.0,"y" => 465.0)
 ("id" => 3,"x" => 57.0,"y" => 25.0)
 ("id" => 4,"x" => 411.0,"y" => 322.0)
 ("id" => 5,"x" => 44.0,"y" => 460.0)
```

## Representing the solution as chromosome.

The solution for our problem is a route from one city to another city. We can write it as an array of integers, where each number represents a city id.

```julia
[1,2,5,4,3,1]
```

So, for above mentioned route or chromosome, we are starting from city1 -> city 2 and so on... finally coming back to city1.

## Crossover function

Here, we generate a new chromosome by taking values from two parent chromosomes.
For this problem we simply have to ensure the genes/city id is not getting repeated, while generating new chromosome.

There are many ways to do a crossover like, Unipoint crossover, multi-point crossover, etc.
We will do a unipoint crossover, simply by choosing a random point in chromosome and doing a simple swap to create new chromosome.

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
        point1 = (
            cities[chromosome[geneId]]["x"],
            cities[chromosome[geneId]]["y"]
            )
        point2 = (
            cities[chromosome[geneId + 1]]["x"],
            cities[chromosome[geneId + 1]]["y"]
            )
        travel_distance += calculate_distance_between_two_points(point1, point2)
	end
	println("travel distance:", chromosome, " : ", travel_distance)
    return travel_distance
end
```

## Generating intial population:
We will define a function that can generate initial populations.

```julia
# We shuffle the chromosome here
function shuffle_chromosome(chromosome)
    for i in 1:size(chromosome)[1]
        random_point = rand(1:5, 1)[1]
        chromosome[i], chromosome[random_point] = chromosome[random_point], chromosome[i]
    end
    
	println("Created chromosome", chromosome)
    return chromosome
end


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

```julia
[3, 9, 4, 8, 10, 5, 1, 2, 7, 6]
[8, 1, 6, 9, 10, 5, 2, 4, 3, 7]
[2, 9, 10, 8, 5, 4, 6, 1, 3, 7]
[5, 6, 10, 7, 4, 3, 1, 2, 8, 9]
[2, 10, 9, 4, 6, 5, 1, 3, 8, 7]
```

## main part

Here, we have defined a function, which run GA for given number of generations, and creates given number of offsprings for each generation, then checks it's fitness and the cycle continues for each generation.

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
```

Now, lets execute the GA

```julia
# creating 10 cities randomly
cities = generate_cities(10, 500)
initial_chromosome = [2:length(cities);]
# generating 10 initial chromosomes
chromosomes = generate_initial_population(10)

# we are running GA for
# 5 generations
# 5 offsprings per generation
# random crossover point as 2
evolve(5, 5, 2)
println("--------------------------------------------------------")
println("Optimal route:", vcat(1, chromosomes[1]["chromosome"], 1))
println("travel_distance:", chromosomes[1]["distance"])
```

If we execute, we get the following output.

# output:

```julia
generation: 1 offspring: 1
travel distance:[1, 3, 9, 10, 7, 5, 4, 6, 8, 2, 1] : 2780.551726305925
generation: 1 offspring: 2
travel distance:[1, 5, 10, 6, 9, 3, 2, 4, 7, 8, 1] : 2236.035984494435
generation: 1 offspring: 3
travel distance:[1, 10, 7, 3, 9, 5, 4, 6, 8, 2, 1] : 2627.3533869849102
generation: 1 offspring: 4
travel distance:[1, 7, 6, 4, 10, 3, 5, 2, 8, 9, 1] : 3078.2871083508203
generation: 1 offspring: 5
travel distance:[1, 3, 9, 10, 7, 2, 4, 5, 8, 6, 1] : 3074.581278954089
generation: 2 offspring: 1
travel distance:[1, 9, 8, 5, 10, 4, 3, 2, 6, 7, 1] : 2882.8847896850843
generation: 2 offspring: 2
travel distance:[1, 5, 10, 6, 2, 3, 9, 4, 7, 8, 1] : 1864.9566066991729
generation: 2 offspring: 3
travel distance:[1, 9, 8, 5, 10, 2, 3, 4, 6, 7, 1] : 2889.200659672017
generation: 2 offspring: 4
travel distance:[1, 4, 10, 6, 9, 3, 2, 5, 7, 8, 1] : 2520.4527035595024
generation: 2 offspring: 5
travel distance:[1, 9, 10, 6, 3, 5, 2, 4, 7, 8, 1] : 2443.441192706744
generation: 3 offspring: 1
travel distance:[1, 2, 10, 6, 9, 8, 5, 7, 4, 3, 1] : 2177.1886229349225
generation: 3 offspring: 2
travel distance:[1, 2, 10, 5, 6, 9, 8, 7, 4, 3, 1] : 1745.6328718972204
generation: 3 offspring: 3
travel distance:[1, 5, 4, 2, 6, 9, 8, 7, 10, 3, 1] : 2491.210252809206
generation: 3 offspring: 4
travel distance:[1, 7, 5, 6, 9, 3, 2, 4, 10, 8, 1] : 2867.790574182069
generation: 3 offspring: 5
travel distance:[1, 10, 6, 5, 9, 3, 2, 7, 4, 8, 1] : 2158.331962819929
generation: 4 offspring: 1
travel distance:[1, 4, 10, 6, 2, 3, 9, 5, 7, 8, 1] : 2375.395804596975
generation: 4 offspring: 2
travel distance:[1, 4, 10, 2, 6, 9, 8, 5, 7, 3, 1] : 2696.2819714580255
generation: 4 offspring: 3
travel distance:[1, 5, 3, 6, 9, 10, 2, 7, 4, 8, 1] : 2585.1841206421177
generation: 4 offspring: 4
travel distance:[1, 4, 6, 2, 9, 8, 5, 7, 10, 3, 1] : 2927.589295286965
generation: 4 offspring: 5
travel distance:[1, 5, 3, 10, 6, 9, 7, 2, 4, 8, 1] : 2610.376635133937
generation: 5 offspring: 1
travel distance:[1, 3, 10, 5, 6, 9, 8, 7, 4, 2, 1] : 1919.461172591361
generation: 5 offspring: 2
travel distance:[1, 10, 6, 8, 9, 3, 2, 7, 4, 5, 1] : 2488.399757690674
generation: 5 offspring: 3
travel distance:[1, 6, 10, 3, 5, 9, 8, 7, 4, 2, 1] : 1962.725547491429
generation: 5 offspring: 4
travel distance:[1, 10, 6, 8, 9, 4, 2, 7, 3, 5, 1] : 2626.455096698985
generation: 5 offspring: 5
travel distance:[1, 2, 6, 5, 10, 3, 9, 4, 7, 8, 1] : 1631.463753062698
--------------------------------------------------------
Optimal route:[1, 2, 6, 5, 10, 3, 9, 4, 7, 8, 1]
travel_distance:1631.463753062698
```

I have created a TSP-GA playground using Typescript, checkout if you want to playaround: [GA TSP using typescript](https://dillir07.github.io/Genetic-Algorithm-TSP/)

![dillir07 - GA TSP](https://dev-to-uploads.s3.amazonaws.com/i/qyenxsc0uix1db747psc.png)

Thank for reading :)... Comments are welcome.