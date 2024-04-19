class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    # Distance from point to point
    def distance_to(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5
    
    def __str__(self):
        return f"{self.x}, {self.y}"
    

class Point3D(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        
        self.z = z
    
    def distance_to(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2 
                + (self.z - point.z))**0.5
    
    def __str__(self):
        return super().__str__() + f", {self.z}"