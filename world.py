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
        indis = [Individual(50,random.randint(0,20),80,0.5) for i in range(self.indiPop)]
        preds = [Predator(random.randint(0,20)) for i in range(self.predPop)]
        food = [Food(random.randint(0,500),random.randint(0,500),10)]
        self.indis = indis
        self.preds = preds
        self.food = food

    def endGeneration(self):
        # TODO : Randomly select one individual and one predator, compare they're stats and kill accordlingly

        indis = []
        for i in self.indis:
            if random.randint(0,180) < i.vision:
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
            indi2 = self.tournamentSelection(indi1)
        else:
            indi2 = self.biasedRandomSelection(indi1)
        return (indi1,indi2)
    
    def tournamentSelection(self,indi1):
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
        child2 = Individual(hp2,vision2,speed2,mateSelectionProb2)

    def mutate(self,indi):
        pass

    def newGeneration(self):
        pass


    
        
