import pygame
import sys
import math
import random

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define simulation parameters
width, height = 800, 600
fps = 60

# Define agent parameters
num_predators = 40
num_preys = 50
num_food = 60
predator_speed = 2
prey_speed = 3
food_size = 3
predator_size = 4
prey_size = 4
vision_angle = math.radians(120)  # Field of vision angle for both predator and prey
vision_radius = 100  # Field of vision radius for both predator and prey

class Agent:
    def __init__(self, color, speed, vision_angle, vision_radius):
        self.color = color
        self.speed = speed
        self.vision_angle = vision_angle
        self.vision_radius = vision_radius
        self.angle = random.uniform(0, 2*math.pi)  # Initial random angle
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)

    def move_towards(self, target_x, target_y):
        angle_to_target = math.atan2(target_y - self.y, target_x - self.x)
        self.x += self.speed * math.cos(angle_to_target)
        self.y += self.speed * math.sin(angle_to_target)
        self.check_boundaries()

    def move_away(self, target_x, target_y):
        angle_away = math.atan2(target_y - self.y, target_x - self.x) + math.pi
        self.x += self.speed * math.cos(angle_away)
        self.y += self.speed * math.sin(angle_away)
        self.check_boundaries()

    def random_movement(self):
        self.angle += random.uniform(-1, 1)  # Add a small random angle change
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.check_boundaries()

    def check_boundaries(self):
        # Ensure agents stay within the screen boundaries
        self.x = max(0, min(self.x, width))
        self.y = max(0, min(self.y, height))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), predator_size)

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Predator-Prey Simulation")
    clock = pygame.time.Clock()

    is_game_start = True
    
    while is_game_start:
        predators = [Agent(RED, predator_speed, vision_angle, vision_radius) for _ in range(num_predators)]
        preys = [Agent(GREEN, prey_speed, vision_angle, vision_radius) for _ in range(num_preys)]
        foods = [(random.randint(0, width), random.randint(0, height)) for _ in range(num_food)]

        while is_game_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Predator behavior
            for predator in predators:
                found_prey = False
                for prey in preys:
                    dist = math.sqrt((prey.x - predator.x)**2 + (prey.y - predator.y)**2)
                    if dist <= predator.vision_radius:
                        if dist < 10:
                            preys.remove(prey)
                            break
                        angle_to_prey = math.atan2(prey.y - predator.y, prey.x - predator.x)
                        angle_difference = abs(angle_to_prey - predator.angle)
                        if angle_difference <= predator.vision_angle / 2:
                            predator.move_towards(prey.x, prey.y)
                            found_prey = True
                            

                if not found_prey:
                    predator.random_movement()

            # Prey behavior
            for prey in preys:
                found_predator = False
                for food in foods:
                    dist = math.sqrt((food[0] - prey.x)**2 + (food[1] - prey.y)**2)
                    if dist <= prey.vision_radius:
                        if dist<10:
                            foods.remove(food)
                            break
                        angle_to_food = math.atan2(food[1] - prey.y, food[0] - prey.x)
                        angle_difference = abs(angle_to_food - prey.angle)
                        if angle_difference <= prey.vision_angle / 2:
                            prey.move_towards(food[0], food[1])
                            found_predator = True
                
                for predator in predators:
                    if math.sqrt((predator.x - prey.x)**2 + (predator.y - prey.y)**2) <= prey.vision_radius:
                        angle_to_predator = math.atan2(predator.y - prey.y, predator.x - prey.x)
                        angle_difference = abs(angle_to_predator - prey.angle)
                        if angle_difference <= prey.vision_angle / 2:
                            prey.move_away(predator.x, predator.y)
                            found_predator = True
                            
                if not found_predator:
                    prey.random_movement()

            # Draw everything
            screen.fill(WHITE)
            for food in foods:
                pygame.draw.circle(screen, BLUE, (int(food[0]), int(food[1])), food_size)
            for predator in predators:
                predator.draw(screen)
            for prey in preys:
                prey.draw(screen)

            pygame.display.flip()
            clock.tick(fps)

            if len(foods) == 0 or len(preys) == 0:
                is_game_start = False
        font_big = pygame.font.Font('freesansbold.ttf', 32)
        font_small = pygame.font.Font('freesansbold.ttf', 20)
        message = "All Preys Dead" if len(preys) == 0 else "All Food Eaten"
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
