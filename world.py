import random
from individual import Individual
from predator import Predator
from food import Food
class World:
    def __init__(self):
        self.indiPop = 10
        self.predPop = 3
        self.foodCount = 20
    
    def spawn(self):
        indis = [Individual(random.randint(0,20)) for i in range(self.indiPop)]
        preds = [Predator(random.randint(0,20)) for i in range(self.predPop)]
        food = [Food(random.randint(0,500),random.randint(0,500),10)]
        self.indis = indis
        self.preds = preds
        self.food = food
    
        
