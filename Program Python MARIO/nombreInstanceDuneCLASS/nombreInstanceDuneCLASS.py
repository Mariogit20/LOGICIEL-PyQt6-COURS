# COMPTER les INSTANCES D'UNE CLASS en PYTHON :

class Rectangle:
    # Class attributes
    shape_type = "Rectangle"
    instances_count = 0

    # Constructors
    def __init__(self, width, height):
        # Attributes
        self.width = width
        self.height = height
        # update class attribute
        Rectangle.instances_count += 1

    # Methods
    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# Create class instance
rect1 = Rectangle(4, 6)
rect2 = Rectangle(10, 9)
rect3 = Rectangle(20, 15)

print(Rectangle.instances_count)




# Bien cordialement,
# ANDRIANTSIMBAHARILANTO Halley Mario
# 034 09 035 59
