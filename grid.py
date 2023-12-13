import random
from copy import deepcopy

class Grid:
    def __init__(self, size, empty_cell):
        """
        Initialize the Grid object.

        Args:
        - size (tuple or int): Tuple representing the grid size (rows, columns) or a single integer for a square grid.
        - empty_cell (dict): Dictionary containing information about the empty cell entity and its display symbol.

        Attributes:
        - size (tuple): Represents the size of the grid (rows, columns).
        - empty_cell (dict): Contains information about the empty cell entity and its display symbol.
        - grid (list): 2D list representing the grid populated with Cell objects.
        """
        self.size = (0, 0)
        
        # Check and set the grid size
        if type(size) == tuple:
            self.size = size
        elif type(size) == int:
            self.size = (size, size)
            
        self.empty_cell = empty_cell
        
        # Create the grid
        self.grid = [[Cell(deepcopy(self.empty_cell["entity"]), self.empty_cell["display"], self, (x, y)) for y in range(self.size[0])] for x in range(self.size[1])]
    
    def populate(self, entity, display, nr_of_cells, positions = []):
        """
        Populate the grid with entities.

        Args:
        - entity: The entity to be populated in the grid.
        - display: Display symbol for the entity.
        - nr_of_cells: Number of cells to be populated with the entity.
        """
        available_cells = [(x, y) for x in range(self.size[0]) for y in range(self.size[1]) if self.grid[x][y].entity == self.empty_cell["entity"]]
        
        random.shuffle(available_cells)  # Shuffle the available cells

        selected_cells = []

        for position in positions:
            x,y = position
            selected_cells.append(self.grid[x][y])

        if len(selected_cells) < nr_of_cells:
            random_cells_needed = nr_of_cells - len(selected_cells)

            for cell in available_cells[:random_cells_needed]:
                selected_cells.append(cell)

        for x, y in selected_cells:
            selected_cell = self.grid[x][y]

            selected_cell.entity = deepcopy(entity)
            selected_cell.display = display
                
    def show(self):
        """
        Display the grid.

        This function prints the grid to the console, displaying the entities in each cell using their display symbols.
        """    
        for row in self.grid:
            row_string = ' '.join(cell.display for cell in row)
            print(row_string)

class Cell():
    def __init__(self, entity, display, grid, position):
        """
        Initialize a Cell object.

        Args:
        - entity: The entity contained in the cell.
        - display: Display symbol for the entity.
        - grid (Grid): Reference to the Grid object to which the cell belongs.
        - position (tuple): Position of the cell in the grid (x, y).
        """
        self.entity = entity
        self.display = display
        self.grid = grid
        self.position = position

    def get_surrounding_cells(self):
        """
        Get surrounding cells of the current cell.

        Returns:
        - surrounding_cells (list): List of neighboring Cell objects.
        """
        pos_x, pos_y = self.position
        
        grid = self.grid
        gridsize_x, gridsize_y = grid.size

        surrounding_cells = []

        directions = [
            (pos_x, pos_y - 1),
            (pos_x, pos_y + 1),
            (pos_x - 1, pos_y),
            (pos_x + 1, pos_y)
        ]

        grid_cells = grid.grid

        surrounding_cells = [
            grid_cells[direction_x][direction_y]
            for direction_x, direction_y in directions
            if 0 <= direction_x < gridsize_x and 0 <= direction_y < gridsize_y
        ]

        return surrounding_cells
    
    def move(self, new_pos):
        """
        Move the entity to a new position in the grid.

        Args:
        - new_pos: New position for the entity. Can be a tuple (x, y) or 'random' for a random move.

        Returns:
        - Boolean: True if the move was successful, False otherwise.
        """
        if type(new_pos) == tuple:
            grid = self.grid
            grid_grid = grid.grid
            gridsize_x, gridsize_y = grid.size

            new_x, new_y = new_pos

            if 0 < new_x < gridsize_x and 0 < new_y < gridsize_y and grid_grid[new_x][new_y].entity == grid.empty_cell["entity"]:
                origin_x, origin_y = self.position

                grid_grid[new_x][new_y].entity = deepcopy(self.entity)
                grid_grid[new_x][new_y].display = self.display

                grid_grid[origin_x][origin_y].clear()

                return True # Return True if move was possible
            return False # Return False if move was not possible
        elif new_pos == "random":

            possible_moves = self.get_surrounding_cells()

            random.shuffle(possible_moves) # Get the surrounding cells'

            for cell in possible_moves:
                    # Try to move to the new position
                    if self.move(cell.position):
                        break
                
    def clear(self):
        """
        Clear the cell by resetting it to an empty state.
        """
        empty_cell = self.grid.empty_cell
        self.entity = empty_cell["entity"]
        self.display = empty_cell["display"]