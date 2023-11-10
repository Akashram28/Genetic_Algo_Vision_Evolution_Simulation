import pygame
import sys
import math
import random
from world import World

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define simulation parameters
width, height = 800, 600
fps = 60

# Define agent parameters
num_preds = 30
num_indis = 50
num_food = 60
mutationChance = 0.1

pred_speed = 15
indi_speed = 20

food_size = 3
pred_size = 4
indi_size = 4

vision = math.radians(90)  # Field of vision angle for both pred and indi
visionRadius = 50  # Field of vision radius for both pred and indi

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("pred-indi Simulation")
    clock = pygame.time.Clock()

    w = World(indiPop = num_indis,
              predPop = num_preds,
              foodCount = num_food,
              mutationChance = mutationChance,
              visionRadius=visionRadius,
              width=width,
              height=height,
              predSpeed = 2,
              indiSpeed = 3,
              foodSize = 3,
              predSize = 4,
              indiSize = 4
              )
    w.spawn(indiVisionRange = 100,
            predVisionRange = 100,
            width = width,
            height = height)
    
    is_game_start = True
    
    while is_game_start:
        preds = w.preds
        indis = w.indis
        foods = w.food
        while is_game_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # pred behavior
            for pred in preds:
                if pred.hp <=0:
                    preds.remove(pred)
                    continue
                found_indi = False
                for indi in indis:
                    dist = math.sqrt((indi.x - pred.x)**2 + (indi.y - pred.y)**2)
                    if dist <= pred.visionRadius:
                        if dist < 10:
                            pred.eat(indi)
                            indis.remove(indi)
                            break
                        angle_to_indi = math.atan2(indi.y - pred.y, indi.x - pred.x)
                        angle_difference = abs(angle_to_indi - pred.angle)
                        if angle_difference <= pred.vision / 2:
                            pred.move_towards(indi.x, indi.y)
                            found_indi = True
                            

                if not found_indi:
                    pred.random_movement()

            # indi behavior
            for indi in indis:
                if indi.hp <=0:
                    indis.remove(indi)
                    continue
                found_pred = False
                for food in foods:
                    dist = math.sqrt((food.x - indi.x)**2 + (food.y - indi.y)**2)
                    if dist <= indi.visionRadius:
                        if dist<10:
                            indi.eat(food)
                            foods.remove(food)
                            break
                        angle_to_food = math.atan2(food.x - indi.y, food.y - indi.x)
                        angle_difference = abs(angle_to_food - indi.angle)
                        if angle_difference <= indi.vision / 2:
                            indi.move_towards(food.x, food.y)
                            found_pred = True
                
                for pred in preds:
                    if math.sqrt((pred.x - indi.x)**2 + (pred.y - indi.y)**2) <= indi.visionRadius:
                        angle_to_pred = math.atan2(pred.y - indi.y, pred.x - indi.x)
                        angle_difference = abs(angle_to_pred - indi.angle)
                        if angle_difference <= indi.vision / 2:
                            indi.move_away(pred.x, pred.y)
                            found_pred = True
                            
                if not found_pred:
                    indi.random_movement()

            # Draw everything
            screen.fill(WHITE)
            for food in foods:
                food.draw(screen)
            for pred in preds:
                pred.draw(screen)
                pred.hp-=0.2
            for indi in indis:
                indi.draw(screen)
                indi.hp-=0.1

            pygame.display.flip()
            clock.tick(fps)

            if len(foods) == 0 or len(indis) == 0:
                is_game_start = False
        
        font_big = pygame.font.Font('freesansbold.ttf', 32)
        font_small = pygame.font.Font('freesansbold.ttf', 20)
        message = "All indis Dead" if len(indis) == 0 else "All Food Eaten"
        text = font_big.render(message, True, RED)
        text_rect = text.get_rect(center=(width // 2, height // 2 - 50))

        restart_button = pygame.Rect(width // 2 - 60, height // 2 + 20, 120, 40)

        while is_game_start == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and restart_button.collidepoint(event.pos):
                        is_game_start = True
                        break

            screen.fill(WHITE)
            screen.blit(text, text_rect)

            pygame.draw.rect(screen, GREEN, restart_button)
            restart_text = font_small.render("Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=restart_button.center)
            screen.blit(restart_text, restart_rect)

            pygame.display.flip()
            clock.tick(30)
            
            
        

if __name__ == "__main__":
    main()
