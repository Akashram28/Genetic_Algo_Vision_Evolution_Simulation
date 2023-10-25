class Individual:
    def __init__(self,vision):
        self.vision = vision
        self.hp = 50
        self.speed = 80
        self.maxVision = 180
    
    def eat(self,food):
        self.hp += food.hp
    
    def die(self):
        self.hp = 0

    def getFitness(self):
        return (self.hp/100)

