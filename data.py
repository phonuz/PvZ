import random
import globals

MAX_SAMPLES = 100
CLEAN = 1
INFECTED = -1
NOT_CHECKED = 0
CHECKED = 1

############################################################################
# Data class
#
#   This class has the samples containing either infected or clean soil from the map.
#   It also has the a, b, c values for the line equation that perfectly predicts the split.
#   This line is used to determine whether a person can randomly become infected.
#
class Data:
    # Initialization function
    #   1. Generate random values a, b, and c between -10 an 10
    #   2. Create a "line" variable with those values (to represent the 2D line)
    #   3. Create a "samples" variable as an array that will hold the soil samples
    #   4. Generate random samples and set each to either be "CLEAN" or "INFECTED"
    #
    def __init__(self):
        a = random.randrange(-10,10)
        b = random.randrange(-10,10)
        c = random.randrange(-10,10)

        self.line = {'a':a, 'b':b, 'c':c }

        self.samples = []
    
        for i in range(0, MAX_SAMPLES):
            x = random.randrange(-globals.SCREEN_CENTER_X, globals.SCREEN_CENTER_X)
            y = random.randrange(-globals.SCREEN_CENTER_Y, globals.SCREEN_CENTER_Y)
            
            answer = (a*x) + (b*y) + c
            
            type = CLEAN
            color = globals.CLEAN_COLOR
            if answer < 0:
                type = INFECTED
                color = globals.INFECTED_COLOR
    
            self.samples.append({'x':x, 'y':y, 'type':type, 'color':color, 'checked':NOT_CHECKED})

    # "Get a random Sample" function
    #   1. Generate a random number between 0 and the number of samples - 1
    #   2. Set that sample to "CHECKED" so that it is drawn to the screen
    #   3. Access the x, y, and type fields from that sample
    #   4. Return those three fields
    #
    def getSample(self):
        sampleNum = random.randrange(0, len(self.samples))
        self.samples[sampleNum]['checked'] = CHECKED

        x = self.samples[sampleNum]['x']
        y = self.samples[sampleNum]['y'] 
        type = self.samples[sampleNum]['type']
        
        return { 'x': x, 'y': y, 'type': type }
    
    # "Is this coordinate safe from infection" function
    #   1. Solve the line equation (ax + by + c) for the line a, b, c values and the given x,y values
    #       (If the solution is < 0 then it means this coordinate is not safe from infection)
    #   2. Return True or False depending on the value obtained
    #
    def isSafe( self, x,y ):
        value = ( self.line['a'] * x ) + ( self.line['b'] * y ) + self.line['c']
        
        if value < 0:
            return False
        else:
            return True
        


