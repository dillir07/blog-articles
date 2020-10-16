"""
ref: https://www.hackerrank.com/challenges/tron?hr_b=1

Tron is a two player game based on the popular movie Tron. The objective of the game is to cut off players movement through each others motorbikes that leave a wall behind them as they move.

Input Format

This version of Tron takes place on a 15x15 grid. Top left of the grid is (0,0) and the bottom right of the grid is indexed as (14,14).
The 1st player is represented by r (ascii value 114) and is positioned with his bike at (7,1) and the 2nd player is represented by g (ascii value 103) and is positioned with his bike at the opposite end of the grid at (7,13).

The first line contains a character representing the current player.
The second line consists of four single spaced integers representing the current position of the 1st and 2nd players' motorbike.
15 lines follow which represents the grid map.
Boundary is represented by # (ascii value 35), an empty grid is represented by - (ascii value 45). Wall left behind by the player are represented by their respective characters.

Output Format

Player's are allowed to output any one of the following moves as the movement of their motorbikes.

    LEFT
    RIGHT
    UP
    DOWN

all in capital letters.
If (x,y) is the current position of the player's motorbike, then the new position on LEFT would be (x,y-1), RIGHT would be (x, y+1), UP would be (x-1,y) and DOWN would be (x+1,y).

Sample Input

r
4 3 5 13
###############
#-rr--------gg#
#-rr--------gg#
#-rr--------gg#
#-rr--------gg#
#-r---------g-#
#-r---------gg#
#rr----------g#
#-------------#
#-------------#
#-------------#
#-------------#
#-------------#
#-------------#
###############

Sample Output

RIGHT

The grid results in the following state.

###############
#-rr--------gg#
#-rr--------gg#
#-rr--------gg#
#-rrr-------gg#
#-r---------g-#
#-r---------gg#
#rr----------g#
#-------------#
#-------------#
#-------------#
#-------------#
#-------------#
#-------------#
###############

The current player is r whose motor bike is positioned currently at (4,3). Valid moves are DOWN and RIGHT. The player outputs RIGHT.

Note:- At any point during the gameplay, player's aren't allowed to trace back their moves. i.e., a LEFT is not allowed after a RIGHT and vice versa or an UP isn't allowed after a DOWN and vice versa.

Game Play

The game play is simultaneous. Both players get the same board state. If both the players move to the same cell in their next move or both hit the walls, the game is considered a draw. The player who is unable to move loses.

Sample Bot

Sample bot: Tronbot
"""

current_player =  input() # read the current player_id (whose turn is it)

# here we are reading both players' positions
player_pos = input().split(" ")
player_pos = list(map(int, player_pos))
rpos = [player_pos[0], player_pos[1]]
gpos = [player_pos[2], player_pos[3]]
grid_size = 15

# here we are reading the grid in to a array
# grid[0][1] -> means first row's second column
grid = []
for gr in range(grid_size):
    grid.append(input())
    
# Here were writing code, that actually makes the decision
def calculate_free_steps(grid, pos):
    """
    Reads the current grid state, and current player's position
    and returns a dictionary with free spaces in each direction.
    returns: {"LEFT":4, "RIGHT":5, "UP":9, "DOWN":0}
    """
    # we are initializing the free steps
    # l = free steps available in left direction
    l = r = u = d = 0

    # We're calculating free steps in each direction
    # i.e., places in grid having '-' as value

    # reading player's current row & current column values
    row, col = pos[0]-1, pos[1]

    # calculating how many steps are available in upward direction
    # if row is > 0, we can try to go 'UP'
    while row > 0:
        # if cell is '-', increment up_free_steps
        if grid[row][col] == "-":
            u += 1
            row -= 1 # go to top row
        else: # if cell is not '-' means it's not free
            break # so break the loop
    
    # do the same for 'DOWN'
    row, col = pos[0]+1, pos[1]
    # calculating how many steps are available in upward direction       
    while row < len(grid):
        if grid[row][col] == "-":
            d += 1
            row += 1
        else:
            break

    # now for 'RIGHT'
    row, col = pos[0], pos[1]+1
    while col < len(grid[0]): #right
        if grid[row][col] == "-":
            r += 1
            col += 1
        else:
            break

    # and finally for 'LEFT'
    row, col = pos[0], pos[1]-1
    while col > 0: # left
        if grid[row][col] == "-":
            l += 1
            col -= 1
        else:
            break
    
    # returning the free steps for each direction
    return {"LEFT":l, "RIGHT":r, "UP":u, "DOWN":d}

direction_to_go = None # initially unknown
free_steps_available = 0

# read the current player's position
ppos = rpos if current_player == "r" else gpos

# calling the method we created above
free_steps_data = calculate_free_steps(grid, ppos)

# looping each direction
# and choosing the one with max free steps
for direction in free_steps_data:
    if free_steps_data[direction] > free_steps_available:
        direction_to_go = direction
        free_steps_available = free_steps_data[direction]

# finally printing to the console
print(direction_to_go)
