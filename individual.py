import math
import random
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Individual:
    def __init__(self,hp,vision,speed,mateSelectionProb,color,width,height,indiSize,maxVision):
        self.color = color
        self.hp = hp
        self.vision = vision
        self.speed = speed
        self.mateSelectionProb = mateSelectionProb # Prob of using biased random instead of tournament
        self.maxVision = maxVision
        self.angle = random.uniform(0, 2*math.pi)  # Initial random angle
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.width = width
        self.height = height
        self.indiSize = indiSize
        
    def eat(self,food):
        self.hp += food.hp
    
    def die(self):
        self.hp = 0

    def getFitness(self):
        return (self.hp/100)
    
    def move_towards(self, target_x, target_y):
        angle_to_target = math.atan2(target_y - self.y, target_x - self.x)
        self.x += self.speed * math.cos(angle_to_target)
        self.y += self.speed * math.sin(angle_to_target)
        self.check_boundaries()

    def move_away(self, target_x, target_y):
        angle_away = math.atan2(target_y - self.y, target_x - self.x) + math.pi
        self.x += self.speed * math.cos(angle_away) + random.randint(0,15)
        self.y += self.speed * math.sin(angle_away) + random.randint(0,15)
        self.check_boundaries()

    def random_movement(self):
        self.angle += random.uniform(-1, 1)  # Add a small random angle change
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.check_boundaries()

    def check_boundaries(self):
        # Ensure agents stay within the screen boundaries
        self.x = max(0, min(self.x, self.width))
        self.y = max(0, min(self.y, self.height))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.indiSize)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.vision, width=1)
        # pygame.draw.line(screen,RED, (self.x, self.y), (self.x + self.visionRadius*math.sin(self.angle), self.y + self.visionRadius*math.cos(self.angle)))
        # pygame.draw.line(screen,BLUE, (self.x, self.y), (self.x + self.visionRadius*math.sin(self.angle + self.vision), self.y + self.visionRadius*math.cos(self.angle + self.vision)))
        # pygame.draw.line(screen,BLUE, (self.x, self.y), (self.x + self.visionRadius*math.sin(self.angle), self.y + self.visionRadius*math.cos(self.angle)))


