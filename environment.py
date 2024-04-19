import random

from numpy import sqrt
from geometry import Point
from socio_elements import CallPoint, Cell


class Grid:
    def __init__(self, cols, rows, width, height):
        """Initialize this node of the grid of general field
          consists of equals quadrants"""

        self.cols = cols
        self.rows = rows
        self.width = width
        self.height = height

        self.col_width, self.row_height = (
            width / self.cols,
            height / self.rows,
        )

        # Initializing a two-dimensional array (table) of quadrants
        self.quadrants = [(0)] * rows
        for i in range(rows):
            self.quadrants[i] = [
                Quadrant(j, i, self.col_width, self.row_height) for j in range(cols)
            ]


class Quadrant:
    def __init__(self, col, row, w, h):
        """A quadrant which placed on grid and has number of column and row
        
        It has reference to cells that are within it"""

        self.col = col
        self.row = row
        self.w = w
        self.h = h
        self.cells = list()

    def intersects(self, cell):
        """Check that cell intersects the quadrant or not"""

        # Define the boundaries of that quadrant
        left = self.col * self.w
        right = (self.col + 1) * self.w
        top = self.row * self.h
        bottom = (self.row + 1) * self.h

        # Closest quadrant point to cell center
        closest_x = max(left, min(cell.x, right))
        closest_y = max(top, min(cell.y, bottom))

        # Distance from closest point to cell center
        distance = sqrt((closest_x - cell.x) ** 2 + (closest_y - cell.y) ** 2)

        # If distance less than cell radius, means that cell intersects quadrant
        if distance < cell.radius:
            return True
        return False

    def insert(self, cell):
        """Insert cell into the quadrant"""

        self.cells.append(cell)
    
    def remove(self, cell):
        """Remove cell from the quadrant"""

        for c in self.cells:
            if c == cell:
                self.cells.remove(cell)

    def __repr__(self):
        return f"({self.col}) ({self.row})"
    
    def get_adjacent_quads(self, grid):

        adjacent_quads = []
        
        if self.row > 0:
            adjacent_quads.append(grid.quadrants[self.row - 1][self.col])
            if self.col > 0:
                adjacent_quads.append(grid.quadrants[self.row - 1][self.col - 1])
            if self.col < grid.cols - 1:
                adjacent_quads.append(grid.quadrants[self.row - 1][self.col + 1])
        
        if self.row < grid.rows - 1:
            adjacent_quads.append(grid.quadrants[self.row + 1][self.col])
            if self.col > 0:
                adjacent_quads.append(grid.quadrants[self.row + 1][self.col - 1])
            if self.col < grid.cols - 1:
                adjacent_quads.append(grid.quadrants[self.row + 1][self.col + 1])
        
        if self.col > 0:
            adjacent_quads.append(grid.quadrants[self.row][self.col - 1])
        
        if self.col < grid.cols - 1:
            adjacent_quads.append(grid.quadrants[self.row][self.col + 1])
        
        return adjacent_quads


class Field:
    def __init__(self, width, height, cell_size, cells_number, cell_speed):
        """Initialization of the field representing all the main processes in the game"""

        self.width = width
        self.height = height
        self.cells = list()
        self.flags = (
            list()
        ) # there will be several flags present in the game at the same time

        self.cell_speed = cell_speed

        self.grid_cols, self.grid_rows = (
            int(width / (cell_size * 4)),
            int(height / (cell_size * 4)),
        )

        self.grid = Grid(self.grid_cols, self.grid_rows, width + 1, height + 1)


        # Initializing cells and put them on the grid
        for _ in range(cells_number):
            new_cell = Cell(
                random.randint(1, width), random.randint(1, height), cell_size
            )
            self.cells.append(new_cell)
            self.grid.quadrants[int(new_cell.y / self.grid.row_height)][
                int(new_cell.x / self.grid.col_width)
            ].insert(new_cell)

    def put_the_flag(self, x, y, cell_size, t=2):
        """Place the flag at the specified coordinates"""

        self.flags.clear() # Delete previous flags
        self.flag = CallPoint(x, y, cell_size, cell_size, t)
        self.flags.append(self.flag)

    def move_to_flag(self):
        """Make a step for all cells in the direction of the flag"""

        if self.flag.is_exist:
            for c in self.cells:
                if not ((c.x == self.flag.x) & (c.y == self.flag.y)):
                    # Cell moving and updating on the grid

                    self.grid.quadrants[int(c.y / self.grid.row_height)][
                        int(c.x / self.grid.col_width)
                    ].remove(c) # Removing cell from the quadrant before move

                    c.move_to(self.flag, 1, self.cell_speed)

                    self.grid.quadrants[int(c.y / self.grid.row_height)][
                        int(c.x / self.grid.col_width)
                    ].insert(c) # Inserting cell in a new quadrant from the actuall coordinates

    def rand_move(self):
        """Make a step in a random direction for all cells"""

        for cell in self.cells:

            step = random.randint(-1, 1), random.randint(-1, 1)
            x, y = cell.x + step[0], cell.y + step[1]

            if x > self.width:
                x = x - 1
            elif x < 0:
                x = x + 1

            if y > self.height:
                y = y - 1
            elif y < 0:
                y = y + 1

            # Cell moving and updating on the grid
            self.grid.quadrants[int(cell.y / self.grid.row_height)][
                int(cell.x / self.grid.col_width)
            ].remove(cell)

            cell.move(Point(x, y))

            self.grid.quadrants[int(cell.y / self.grid.row_height)][
                int(cell.x / self.grid.col_width)
            ].insert(cell)

    def check_collision(self):
        """Checking for collisions in the quadrants that intercects cell"""

        cells = self.cells
        for cell in cells:
            # Checking each of cells in the field

            for r in self.cell_quadrants(cell):
                # This loop for all cells that placed in intersected quadrants

                for other_cell in r.cells:
                    if cell.collidecell(other_cell) and cell != other_cell:
                        # Checking cell for a collision

                        self.grid.quadrants[int(cell.y / self.grid.row_height)][
                            int(cell.x / self.grid.col_width)
                        ].remove(cell)

                        # moving from the another cell of collide
                        cell.move_from(other_cell, 1, self.cell_speed)

                        self.grid.quadrants[int(cell.y / self.grid.row_height)][
                            int(cell.x / self.grid.col_width)
                        ].insert(cell)


    def cell_quadrants(self, cell):
        """Get quadrants of cell intersection"""

        cell_quads = []

        cell_col, cell_row = int(cell.x / self.grid.col_width), int(cell.y / self.grid.row_height)
        cell_quads.append(self.grid.quadrants[cell_row][cell_col])

        adjacent_quads = self.grid.quadrants[cell_row][cell_col].get_adjacent_quads(self.grid)

        for quad in adjacent_quads:
            if quad.intersects(cell):
                cell_quads.append(quad)

        return cell_quads
