class Predator:
    def __init__(self,vision):
        self.vision = vision
        self.hp = 100
        self.speed = 100
        self.maxVision = 150
    
    def eat(self,individual):
        self.hp += max(individual.hp//2 , individual.hp-20)
    
    def kill(self):
        self.hp = 0

    def getFitness(self):
        return (self.hp/100)

