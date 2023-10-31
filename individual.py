class Individual:
    def __init__(self,hp,vision,speed,mateSelectionProb):
        self.hp = hp
        self.vision = vision
        self.speed = speed
        self.mateSelectionProb = mateSelectionProb # Prob of using biased random instead of tournament
        self.maxVision = 180
    
    def eat(self,food):
        self.hp += food.hp
    
    def die(self):
        self.hp = 0

    def getFitness(self):
        return (self.hp/100)

