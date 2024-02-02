

class CarPart:


    def __init__ (self, x_axis_value, y_axis_value):

        self.x = x_axis_value
        self.y = y_axis_value

    
    #overloading the "<" operator needed in getting the minimum of two "carpart" class
    
    def __lt__ (self, rhs):

        return self.x < rhs.x 
    
    #Overloading the ">" operator needed when getting the tip of a car

    def __get__ (self, rhs):

        return self.y > rhs.y 
    