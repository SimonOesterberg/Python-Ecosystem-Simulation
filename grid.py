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
        
        # Create the grid using references to the same empty cell object
        self.grid = [[Cell(self.empty_cell["entity"], self.empty_cell["display"], self, (x, y)) for y in range(self.size[1])] for x in range(self.size[0])]
        self.available_cells = {(x, y): True for x in range(self.size[0]) for y in range(self.size[1]) if self.grid[x][y].entity == self.empty_cell["entity"]}

    def populate(self, entity, display, nr_of_cells):

        available_cells = [k for k, v in self.available_cells.items() if v is True]

        random.shuffle(available_cells)
        
        selected_cells = available_cells[:min(nr_of_cells, len(available_cells))]
        
        for x, y in selected_cells:
            selected_cell = self.grid[x][y]
            selected_cell.entity = deepcopy(entity)
            selected_cell.display = display
            self.available_cells[(x, y)] = False

    def show(self):
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

        directions = [
            (pos_x, pos_y - 1),
            (pos_x, pos_y + 1),
            (pos_x - 1, pos_y),
            (pos_x + 1, pos_y)
        ]

        # Extract grid once
        grid_cells = grid.grid

        surrounding_cells = [
            grid_cells[direction_x][direction_y]
            for direction_x, direction_y in directions
            if 0 <= direction_x < gridsize_x and 0 <= direction_y < gridsize_y
        ]

        return surrounding_cells
    
    def move(self, new_pos, possible_moves = []):
        """
        Move the entity to a new position in the grid.

        Args:
        - new_pos: New position for the entity. Can be a tuple (x, y) or 'random' for a random move.

        Returns:
        - Boolean: True if the move was successful, False otherwise.
        """

        if type(new_pos) == tuple:
            grid = self.grid.grid
            new_x, new_y = new_pos

            if (new_x, new_y) in list(self.grid.available_cells.keys()):
                origin_x, origin_y = self.position

                grid[new_x][new_y].entity = deepcopy(self.entity)
                grid[new_x][new_y].display = self.display

                self.grid.available_cells[(new_x, new_y)] = False
                self.grid.available_cells[(origin_x, origin_y)] = True

                grid[origin_x][origin_y].clear()

                return True # Return True if move was possible
            return False # Return False if move was not possible
        elif new_pos == "random":

            if len(possible_moves) == 0:
                possible_moves = self.get_surrounding_cells()

            random.shuffle(possible_moves) # Get the surrounding cells'
            
            for cell in possible_moves:
                # Try to move to the new position
                if cell.position in list(self.grid.available_cells.keys()):
                    self.move(cell.position)
                    break
                
    def clear(self):
        """
        Clear the cell by resetting it to an empty state.
        """
        empty_cell = self.grid.empty_cell
        pos_x, pos_y = self.position

        self.grid.available_cells[(pos_x, pos_y)] = True
        self.entity = empty_cell["entity"]
        self.display = empty_cell["display"]