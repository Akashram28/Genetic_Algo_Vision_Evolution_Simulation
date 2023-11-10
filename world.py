import random
from individual import Individual
from predator import Predator
from food import Food


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class World:
    def __init__(self,indiPop,predPop,foodCount,mutationChance,visionRadius,width,height,predSpeed,indiSpeed,foodSize,predSize,indiSize):
        self.indiPop = indiPop
        self.predPop = predPop
        self.foodCount = foodCount
        self.mutationChance = mutationChance
        self.visionRadius = visionRadius
        self.width = width
        self.height = height
        self.predSpeed = predSpeed
        self.indiSpeed = indiSpeed
        self.foodSize = foodSize
        self.predSize = predSize
        self.indiSize = indiSize
    
    def spawn(self,indiVisionRange,predVisionRange,width,height):
        # self,hp,vision,speed,mateSelectionProb,color,visionRadius,width,height,size
        indis = [Individual(50,random.randint(50,indiVisionRange),self.indiSpeed,0.5,GREEN,self.visionRadius,self.width,self.height,self.indiSize) for i in range(self.indiPop)]
        preds = [Predator(100,random.randint(50,predVisionRange),self.predSpeed,0.5,RED,self.visionRadius,self.width,self.height,self.predSize) for i in range(self.predPop)]
        food = [Food(10,random.randint(0,width),random.randint(0,height),self.foodSize) for i in range(self.foodCount)]
        self.indis = indis
        self.preds = preds
        self.food = food

    def endGeneration(self):
        # TODO : Randomly select one individual and one predator, compare they're stats and kill accordlingly

        indis = []
        for i in self.indis:
            if i.hp > 0:
                indis.append(i)
        self.indis = indis
        self.indiPop = len(indis)

        #---- Preprocessing for biased random as we don't need to precompute this again and again ----#
        fitnessSum = 0
        for i in self.indis:
            fitnessSum += i.getFitness()
        individual_probs = [i.getFitness()/fitnessSum for i in self.indis]
        cumulative_probs = []
        cumulativeSum = 0
        for i in range(self.indiPop):
            cumulativeSum += individual_probs[i]
            cumulative_probs[i].append(cumulativeSum)
        self.probs = cumulative_probs        

    
    def selectParents(self):
        indi1 = self.indis[random.randint(0,self.indiPop-1)]
        if random.random() < indi1.mateSelectionProb:
            indi2 = self.tournamentSelection()
        else:
            indi2 = self.biasedRandomSelection(indi1)
        return indi1,indi2
    
    def tournamentSelection(self):
        indi2 = self.indis[random.randint(0,self.indiPop-1)]
        indi3 = self.indis[random.randint(0,self.indiPop-1)]
        while indi2 == indi3:
            indi3 = self.indis[random.randint(0,self.indiPop-1)]
        if indi2.getFitness() > indi3.getFitness():
            return indi2
        else:
            return indi3

    def biasedRandomSelection(self,indi1):
        hasGotPair = False
        while hasGotPair == False:
            selectedValue = random.random()
            for i in range(self.indiPop):
                if selectedValue <= self.probs[i]:
                    if self.indis[i] != indi1:
                        return self.indis[i]
                    break
        
    def crossover(self,indi1,indi2):
        parents =[indi1,indi2]

        hp1 = parents[random.randint(0,1)].hp
        vision1 = parents[random.randint(0,1)].vision
        speed1 = parents[random.randint(0,1)].speed
        mateSelectionProb1 = parents[random.randint(0,1)].mateSelectionProb

        hp2 = parents[0 if hp1==1 else 1].hp
        vision2 = parents[0 if vision1==1 else 1].vision
        speed2 = parents[0 if speed1==1 else 1].speed
        mateSelectionProb2 = parents[0 if mateSelectionProb1==1 else 1].mateSelectionProb

        child1 = Individual(hp1,vision1,speed1,mateSelectionProb1)
        child1 = self.mutate(child1)
        child2 = Individual(hp2,vision2,speed2,mateSelectionProb2)
        child2 = self.mutate(child2)

        return child1,child2

    def mutate(self,indi):
        if random.random() < self.mutationChance:
            newVision = min(indi.vision + random.randint(-10,10),indi.maxVision)
            newSpeed = indi.speed + random.randint(-5,5)
            newHp = indi.hp + random.randint(-10,10)
            newMateSelectionProb = indi.mateSelectionProb + random.randint(-10,10)/100

            indi.vision = newVision
            indi.speed = newSpeed
            indi.hp = newHp
            indi.mateSelectionProb = newMateSelectionProb
            return indi
        return indi

    def newGeneration(self):
        self.endGeneration()
        indis = []
        for i in range(self.indiPop//2):
            parent1 , parent2 = self.selectParents()
            child1 , child2 = self.crossover(parent1,parent2)
            indis.append(child1)
            indis.append(child2)
        self.indis = indis
        self.indiPop = len(indis)
    
    def getBestIndi(self):
        bestFitness = -float('inf')
        bestIndi = None
        for i in self.indis:
            fitness = i.getFitness()
            if fitness > bestFitness:
                bestFitness = fitness
                bestIndi = i
        return bestIndi


    
        
