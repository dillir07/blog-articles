# Genetic Algorithm
Genetic algorithm is a method of mimicking natural section and survival of fittest to find optimal solutions to problems, that otherwise would be too difficult to solve.

# Travelling Salesman Problem
Travelling Salesman Problem or TSP for short is a infamous problem where a travelling sales person has to travel various cities with known distance and return to the origin city in the shortest time/path possible.

First lets try to brute force to solve the problem.
for starters lets take 5 cities, i.e., we have to calculate 5! routes to ensure we got the shortest path.

Now, if we are to do that for 20 cities,
- 5! = 120
- 10! = 3628800
- 15! = 1307674368000
- 20! = 2432902008176640000

We can see how brute forcing our way is simply not going to be helpful here.

So, we will see how Genetic Algorithm can help us find a optimal shortest path here.

In simple, Genetic Algorithm works on the following way,
- Choosing Random initial solutions (Called as Initial Population or Chromosomes)
- 