# Example Usage
from grid import Grid

# Initialize a grid with a size of 5x5 and an empty cell entity
my_grid = Grid((5, 5), {"entity": None, "display": "."})

# Populate the grid with entities
my_grid.populate("entity_A", "A", 5)
my_grid.populate("entity_B", "B", 3, coordinates=[(1, 2), (3, 4)])

# Display the grid
my_grid.show()