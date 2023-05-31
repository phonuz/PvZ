import random
import globals

LEARNING_RATE = 0.5

############################################################################
# Perceptron class
#
#   This class has the weights for a perceptron, and the functions to train it, get a prediction, and get the 2D line Y values
#
class Perceptron:

    # Initialization function
    #   1. create class variable "weights"
    #   2. initialize weights with random numbers between -1.0 and 1.0
    #
    def __init__(self, numWeights):
        self.weights = []
        for i in range(0, numWeights):
            weight = random.uniform(-1.0,1.0)
            self.weights.append(weight) 

    # Training function
    #
    def train( self, inputs, answer ):
        prediction = self.getPrediction(inputs)
        direction = answer - prediction

        for i in range(0, len(self.weights)):
            self.weights[i] = self.weights[i] + ( LEARNING_RATE * inputs[i] * direction )
                
    # Prediction function
    #   
    def getPrediction(self, inputs):
        value = 0
        for i in range(0, len(self.weights)):
            value += self.weights[i] * inputs[i]
        
        if value > 0:
            return 1
        else:
            return 0
        
    # Get weights
    #
    def getWeights(self):
        return self.weights

############################################################################


############################################################################
# Brain class
#
class Brain:
    
    NUM_WEIGHTS = 3

    # Initialization function
    #   1. 
    #
    def __init__(self):
        self.perceptron = Perceptron( self.NUM_WEIGHTS )
        
    # Training function
    #   
    #
    def train(self, inputs, answer):
        self.perceptron.train(inputs, answer)

    # Prediction function
    #   1.
    #
    def getPrediction(self, inputs):
        return self.perceptron.getPrediction(inputs)
    
    # "Get the Y coordinate for graphing the line" function
    #   The equation for a 2D line is:
    #       ax + by + c = 0
    #
    #   Therefor, the equation for calculating the Y of a 2D line is:
    #       y = ( -( a * x) - c ) / b
    #
    #   a is weights[0]    b is weights[1]        c is weights[2]
    #
    #   1. if b is 0, set b to a very small but non-zero number (to prevent division by zero errors)
    #   2. set y to ( -( a * x) - c ) / b
    #   3. return y
    #
    def getY(self, x):
        weights = self.perceptron.getWeights()
        a = weights[0]
        b = weights[1]
        c = weights[2]

        if b == 0:
            b = globals.VERY_SMALL_NUMBER

        y =  ( - ( a * x ) - c ) / b
        
        return y
    
    def getX(self, y):
        weights = self.perceptron.getWeights()
        a = weights[0]
        b = weights[1]
        c = weights[2]

        if a == 0:
            a = globals.VERY_SMALL_NUMBER

        x =  ( - ( b * y ) - c ) / a
        
        return x
    
    def getSlope(self):
        weights = self.perceptron.getWeights()
        a = weights[0]
        b = weights[1]

        if b == 0:
            b = globals.VERY_SMALL_NUMBER
        
        return -(a / b)
    
