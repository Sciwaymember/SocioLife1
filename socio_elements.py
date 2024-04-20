from geometry import Point

class Cell(Point):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.is_exist = True
        self.radius = radius

    def delete(self):
        self.is_exist = False

    # Move cell into specified coordinates
    def move(self, direction):

        self.x = direction.x
        self.y = direction.y

    # Make a step in the direction of the specified point 
    def move_to(self, point, steps, cell_speed):

        for _ in range(steps):
            if self.distance_to(point) < cell_speed:
                cell_speed = self.distance_to(point)

            self.dir_step = Point(
                self.x + cell_speed * ((point.x - self.x) / self.distance_to(point)),
                self.y + cell_speed * ((point.y - self.y) / self.distance_to(point)),
            )
            
            self.move(self.dir_step)

    # Make a step in the reverse direction of the specified point 
    def move_from(self, point, steps, cell_speed):

        if self.x != point.x and self.y != point.y:

            for _ in range(steps):
                if self.distance_to(point) < cell_speed:
                    cell_speed = self.distance_to(point)


                self.dir_step = Point(
                    self.x - cell_speed * ((point.x - self.x) / self.distance_to(point)),
                    self.y - cell_speed * ((point.y - self.y) / self.distance_to(point)),
                )
            
                self.move(self.dir_step)

    def collidecell(self, cell):
        """Check for the collision and return collision degree"""
        collision_degree = self.radius * 2 - self.distance_to(cell)
        return self.distance_to(cell) <= self.radius * 2, collision_degree


class CallPoint(Point):
    def __init__(self, x, y, width, height, t):
        super().__init__(x, y)
        self.is_exist = True
        self.width = width
        self.height = height
        self.life_time = t

    def delete(self):
        self.is_exist = False
