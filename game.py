import pygame
import os
import random
import time
pygame.init()
pygame.mixer.init()

font = pygame.font.Font('freesansbold.ttf', 30)

#sound cue
OBSTACLE_SOUND_CUE = pygame.mixer.Sound("Assets/sounds/jump.wav")
CUE_DISTANCE_THRESH = 250

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH + random.randrange(0,500)

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
        
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randrange(200,300)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


# def menu(death_count):
#     global points
#     run = True
#     while run:
#         SCREEN.fill((255, 255, 255))

#         if death_count == 0:
#             text = font.render("Press any Key to Start", True, (0, 0, 0))
#         elif death_count > 0:
#             text = font.render("Press any Key to Restart", True, (0, 0, 0))
#             score = font.render("Your Score: " + str(points), True, (0, 0, 0))
#             scoreRect = score.get_rect()
#             scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
#             SCREEN.blit(score, scoreRect)
#         textRect = text.get_rect()
#         textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
#         SCREEN.blit(text, textRect)
#         SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
#         pygame.display.update()
#         time.sleep(5)
#         run=False
#         # for event in pygame.event.get():
#             # if event.type == pygame.QUIT:
#                 # pygame.quit()
#                 # run = False
#             # if event.type == pygame.KEYDOWN:
#                 # main()

def wait_for_spacebar(game_no):
    """Wait for the spacebar to start each game round."""
    waiting = True
    while waiting:
        SCREEN.fill(BLACK)
        text = font.render(f"Press SPACE to start the game {game_no}.", True, WHITE)
        SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


def start_page():
    title_font = pygame.font.Font(None, 74)
    text_font = pygame.font.Font(None, 36)
    # Fill the background
    SCREEN.fill(YELLOW)
    
    # Title text
    title_text = title_font.render("Dino Game Adventure", True, BLACK)
    SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
    
    # Subtitle text
    subtitle_text = text_font.render("Test your reflexes and get ready for a fun journey!", True, GREEN)
    SCREEN.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 130))
    
    # Game description
    description_lines = [
        "In this game, you'll guide a little dinosaur through an obstacle-filled desert.",
        "Jump over cacti and duck under birds to survive as long as possible!",
    ]
    for i, line in enumerate(description_lines):
        description_text = text_font.render(line, True, BLACK)
        SCREEN.blit(description_text, (SCREEN_WIDTH // 2 - description_text.get_width() // 2, 200 + i * 30))
    
    # Controls description
    controls_text = [
        "Controls:",
        "UP Arrow Key - Jump over obstacles",
        "DOWN Arrow Key - Duck under obstacles",
    ]
    for i, line in enumerate(controls_text):
        control_text = text_font.render(line, True, ORANGE if i == 0 else BLACK)
        SCREEN.blit(control_text, (SCREEN_WIDTH // 2 - control_text.get_width() // 2, 350 + i * 30))
    
    # Instruction to start
    start_text = text_font.render("Press SPACE to Start", True, GREEN)
    SCREEN.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT - 100))
    
    pygame.display.flip()

def DINO_GAME(sound_index):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles,font
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 25
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    obstacles = []
    death_count = 0
    prev_time = time.time()
    
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 2

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
    
    # added by rohan
    def check_collision(rect1, rect2):
        # Check if the rectangles do not overlap horizontally
        if rect1.x + rect1.width-15 < rect2.x or rect2.x + rect2.width < rect1.x+15:
            return False
        # Check if the rectangles do not overlap vertically
        if rect1.y + rect1.height-15 < rect2.y or rect2.y + rect2.height < rect1.y+15:
            return False
        # If neither of the above conditions are true, the rectangles must overlap
        return True
    
    # added by rohan
    def check_upcoming_collision(rect1, rect2):
        if rect1.x + rect1.width+CUE_DISTANCE_THRESH >= rect2.x and rect1.x + rect1.width+CUE_DISTANCE_THRESH < rect2.x+30:
            return True
        return False
    
    def check_upcoming_collision_hoax(rect1, rect2):
        a = random.randrange(-250,-30)
        b = random.randrange(35,500)
        if rect1.x + rect1.width+ a+b>= rect2.x and rect1.x + rect1.width + a+b < rect2.x+30:
            return True
        return False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            
            if check_upcoming_collision(player.dino_rect,obstacle.rect):
                if sound_index==1:
                    OBSTACLE_SOUND_CUE.play()
            
            if sound_index==3:
                # a = (time.time()-prev_time)
                if(random.randrange(0,75)==50):
                    OBSTACLE_SOUND_CUE.play()
            # print(player.dino_rect.x,obstacle.rect.x,obstacle.rect.width)
            if check_collision(player.dino_rect,obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                return -1
                
        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()
        
        clock.tick(30)
        pygame.display.update()
        
def play_game(round_number):
    """Main game logic for each round. Customize this function with your game code."""
    DINO_GAME(round_number)        
        
def main():
    # Play games in 3 parts, with 2 games each
    total_games = 6
    games_per_part = 2
    cntr=1
    
    L1 = [1,2,3]
    L2= [2,1,3]
    random.shuffle(L1)
    random.shuffle(L2)
    sound_order = L1 + L2 
    print(sound_order)
    # Main loop for START PAGE
    running = True
    while running:
        start_page()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False  # Exit start page and proceed to game

    for part in range(1, (total_games // games_per_part) + 1):
        for game_round in range((part - 1) * games_per_part + 1, part * games_per_part + 1):
            wait_for_spacebar(cntr)
            play_game(sound_order[cntr-1])
            cntr+=1
        print(f"Part {part} complete")

    print("All parts completed!")
    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()