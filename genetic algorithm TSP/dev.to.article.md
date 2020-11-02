# Genetic Algorithm
Genetic algorithm is a method of mimicking natural section and survival of fittest to find optimal solutions to problems, that otherwise would be too difficult to solve.

# Travelling Salesman Problem
Travelling Salesman Problem or TSP for short is a infamous problem where a travelling sales person has to travel various cities with known distance and return to the origin city in the shortest time/path possible.

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

In simple, Genetic Algorithm works on the following way,
- Choosing Random initial solutions (Called as Initial Population or Chromosomes)
- crossover (generating new solution or chromosome, by kind of mixing two parents)
- mutate (making a minor change in the solution)
- fitness check (checking if the solution is useful or fullfills our requirement)

So.. for our problem, we will do the following:

- Create a map, with bunch of cities at random location

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

```bash
 ("id" => 1,"x" => 480.0,"y" => 157.0)
 ("id" => 2,"x" => 4.0,"y" => 465.0)
 ("id" => 3,"x" => 57.0,"y" => 25.0)
 ("id" => 4,"x" => 411.0,"y" => 322.0)
 ("id" => 5,"x" => 44.0,"y" => 460.0)
```

- Representing the solution as chromosome.
    - the solution for our problem is route from one city to another city. We can write it as an array of integers, where each number represents a city.

```julia
[2,5,4,3,1]
```
- Generating intial population:
    - We will define a function that can generate initial populations.