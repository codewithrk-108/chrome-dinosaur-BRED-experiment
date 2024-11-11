import pygame
import json
import os
import sys
import random
import time
pygame.init()
pygame.mixer.init()


# json file path
# JSON_FILE_PATH='data_file.json'
# with open(JSON_FILE_PATH,'r') as file:
#     data = json.load(file)

# idno = len(data)
# new_data = {
#     str(idno) : {
#         "Name" : "",
#         "Age" : "",
#         "Email_id": "",
#         "Rating_Chrome_Dino_Game":0,
#         "Game_End_Time":[],
#         "Score":[],
#         "Distance_Threshold":[],
#         "REACTION_TIME_AUDIO_CUE":[],
#         "REACTION_TIME_VISUAL_CUE":[]
#     }
# }
# added by vatsa
new_data = {
    "Name" : "",
    "Age" : "",
    "Email_id": "",
    "Rating_Chrome_Dino_Game":0,
    "Game_End_Time":[],
    "Score":[],
    "Distance_Threshold":[],
    "REACTION_TIME_AUDIO_CUE":[[],[],[]],
    "REACTION_TIME_VISUAL_CUE":[[],[],[]]
}

font = pygame.font.Font('freesansbold.ttf', 30)

#sound cue
OBSTACLE_SOUND_CUE = pygame.mixer.Sound("Assets/sounds/jump.wav")
CUE_DISTANCE_THRESH = 300
REACTION_TIME_VISUAL_CUE=0
REACTION_TIME_AUDIO_CUE=0
ROUND=0

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
disable=1
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
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

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
        global REACTION_TIME_AUDIO_CUE,REACTION_TIME_VISUAL_CUE,new_data,ROUND
        
        
        if(REACTION_TIME_AUDIO_CUE!=-1):
            REACTION_TIME_AUDIO_CUE = time.time()-REACTION_TIME_AUDIO_CUE
            new_data["REACTION_TIME_AUDIO_CUE"][ROUND].append(REACTION_TIME_AUDIO_CUE)
            REACTION_TIME_AUDIO_CUE=-1
        if(REACTION_TIME_VISUAL_CUE!=-1):
            REACTION_TIME_VISUAL_CUE = time.time()-REACTION_TIME_VISUAL_CUE
            new_data["REACTION_TIME_VISUAL_CUE"][ROUND].append(REACTION_TIME_VISUAL_CUE)
            REACTION_TIME_VISUAL_CUE=-1
        
        # print(REACTION_TIME_VISUAL_CUE)
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
    
    def glow(self,SCREEN):
        # red_glow = pygame.Surface((self.dino_rect.width,self.dino_rect.height), pygame.SRCALPHA)
        # red_glow.fill((255, 0, 0, 128))  # Red with 50% transparency
        
        screen_glow_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        screen_glow_surface.fill((255, 0, 0, 128))  # Red color with 50% transparency


        # Blit the overlay on top of the object
        SCREEN.blit(screen_glow_surface, (0, 0))


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
        global disable
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
            disable=1

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
        self.rect.y = random.randrange(230,300)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

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

def pre_exp_form():
    global new_data,idno
    # Fonts
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)

    # Form fields and data
    form_data = {
        "Name": "",
        "Age": "",
        "Email_id": "",
        "Rating_Chrome_Dino_Game": 0
    }
    active_field = None

    # Rating radio buttons
    rating_options = [1, 2, 3, 4, 5]
    rating_pos = [(200 + i * 50, 350) for i in range(len(rating_options))]  # Increase spacing

    # Input field rects
    input_rects = {
        "Name": pygame.Rect(200, 100, 300, 32),
        "Age": pygame.Rect(200, 150, 300, 32),
        "Email_id": pygame.Rect(200, 200, 300, 32),
    }

    # Helper function to draw text
    def draw_text(text, pos, color=BLACK, font=font):
        text_surface = font.render(text, True, color)
        SCREEN.blit(text_surface, pos)

    # Main form loop
    running = True
    while running:
        SCREEN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any input field was clicked
                for field, rect in input_rects.items():
                    if rect.collidepoint(event.pos):
                        active_field = field
                        break
                else:
                    active_field = None
                
                # Check for rating selection
                for i, pos in enumerate(rating_pos):
                    rating_rect = pygame.Rect(pos[0] - 10, pos[1] - 10, 20, 20)
                    if rating_rect.collidepoint(event.pos):
                        form_data["Rating_Chrome_Dino_Game"] = rating_options[i]

            elif event.type == pygame.KEYDOWN:
                # Handle text input
                if active_field:
                    if event.key == pygame.K_BACKSPACE:
                        form_data[active_field] = form_data[active_field][:-1]
                    elif event.key == pygame.K_RETURN:
                        active_field = None  # Move focus away on Enter
                    else:
                        form_data[active_field] += event.unicode

        # Draw labels and input fields with more space
        draw_text("Enter Your Details", (SCREEN_WIDTH // 2 - 80, 40), BLUE, font)

        # Display fields and current input
        y_offset = 0
        for field, rect in input_rects.items():
            pygame.draw.rect(SCREEN, GRAY if active_field == field else BLACK, rect, 2)
            draw_text(f"{field}:", (rect.x - 140, rect.y + 5), BLACK, small_font)
            draw_text(form_data[field], (rect.x + 5, rect.y + 5), BLACK, small_font)
            y_offset += 60

        # Draw rating radio buttons with labels
        draw_text("Rate Chrome Dino Game (1-5):", (50, 300), BLACK, small_font)
        for i, pos in enumerate(rating_pos):
            color = RED if form_data["Rating_Chrome_Dino_Game"] == rating_options[i] else GRAY
            pygame.draw.circle(SCREEN, color, pos, 10)
            pygame.draw.circle(SCREEN, BLACK, pos, 10, 1)  # Border around the circle
            draw_text(str(rating_options[i]), (pos[0] - 5, pos[1] - 25), BLACK, small_font)

        # Draw a submit button
        submit_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, 400, 100, 40)
        pygame.draw.rect(SCREEN, BLUE, submit_button)
        draw_text("Submit", (submit_button.x + 10, submit_button.y + 5), WHITE, font)

        # Check if submit button was clicked
        if event.type == pygame.MOUSEBUTTONDOWN and submit_button.collidepoint(event.pos):
            # new_data[str(idno)] = {
            #     "Name": form_data["Name"],
            #     "Age": form_data["Age"],
            #     "Email_id": form_data["Email_id"],
            #     "Rating_Chrome_Dino_Game": form_data["Rating_Chrome_Dino_Game"]
            # }
            new_data = {
                "Name": form_data["Name"],
                "Age": form_data["Age"],
                "Email_id": form_data["Email_id"],
                "Rating_Chrome_Dino_Game": form_data["Rating_Chrome_Dino_Game"]
            }
            running = False  # Exit the form to start the game

        # Update the display
        pygame.display.flip()

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
        "UP Arrow Key - Jump over obstacles"
    ]
    for i, line in enumerate(controls_text):
        control_text = text_font.render(line, True, ORANGE if i == 0 else BLACK)
        SCREEN.blit(control_text, (SCREEN_WIDTH // 2 - control_text.get_width() // 2, 350 + i * 30))
    
    # Instruction to start
    start_text = text_font.render("Press SPACE to Start", True, GREEN)
    SCREEN.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT - 100))
    
    pygame.display.flip()

def GAME():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles,font,disable,REACTION_TIME_AUDIO_CUE,REACTION_TIME_VISUAL_CUE
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 40
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    obstacles = []
    death_count = 0
    
    def score():
        global points, game_speed
        points += 1
        # constant game speed; added by vatsa
        # if points % 100 == 0:
        #     game_speed += 2

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
        #threshold changed by vatsa
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
        if rect2.x - (rect1.x + rect1.width) <= CUE_DISTANCE_THRESH and  rect2.x - (rect1.x + rect1.width)>0: 
            return True
        return False
    
    def reset_sound(rect1, rect2):
        if rect2.x - (rect1.x + rect1.width) <=-50 or rect2.x - (rect1.x + rect1.width) > CUE_DISTANCE_THRESH:
            return True
        return False
    
    sound_played=True
    glow_active = False
    cue_glow_time_start=-1
    while run:
        if disable==0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        
        if glow_active and time.time()-cue_glow_time_start<0.14:
            # RED with 50% transparency
            SCREEN.fill((255,0,0,128))
        else:
            SCREEN.fill((255, 255, 255))
            glow_active = False
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 25) == 2:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 25) == 18:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            # elif random.randint(0, 2) == 2:
                # obstacles.append(Bird(BIRD))
        
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            
            if sound_played== False:
                sound_played = reset_sound(player.dino_rect,obstacle.rect)
            
            
            if sound_played and check_upcoming_collision(player.dino_rect,obstacle.rect):
                soundOrVisual = random.choice([0,1])
                if soundOrVisual:
                    REACTION_TIME_AUDIO_CUE = time.time()
                    REACTION_TIME_VISUAL_CUE=-1
                    OBSTACLE_SOUND_CUE.play()
                    sound_played=False
                else:
                    REACTION_TIME_VISUAL_CUE = time.time()
                    REACTION_TIME_AUDIO_CUE=-1
                    glow_active=True
                    sound_played=False
                    cue_glow_time_start = time.time()
                    
                disable=0
            
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
        
def play_game():
    GAME()        
        
def main():
    # Play games in 3 parts, with 2 games each
    global CUE_DISTANCE_THRESH,new_data,ROUND
    TOTAL_GAMES = 3
    # delay_thresh_var=[350,650,500]
    delay_thresh_var = [350,650,500]
    random.shuffle(delay_thresh_var)
    
    pre_exp_form()
    
    running = True
    while running:
        start_page()
        
        # event listener        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False  # Exit start page and proceed to game
        
        
    for i in range(1,TOTAL_GAMES+1):
        CUE_DISTANCE_THRESH=delay_thresh_var[i-1]
        wait_for_spacebar(i)
        start_time = time.time()
        play_game()
        new_data["Score"].append(points)
        new_data["Game_End_Time"].append(time.time()-start_time)
        new_data["Distance_Threshold"].append(CUE_DISTANCE_THRESH) #added by vatsa
        ROUND+=1

    print("All parts completed!")
    pygame.quit()

# Run the game
#TODO: save the data into a jsonl file
if __name__ == "__main__":
    main()
    # data.update(new_data)
    data = new_data
    print(new_data)
    # with open(JSON_FILE_PATH,'a') as file:
    #     json.dump(data,file,indent=4)

    # save in jsonl format; added by vatsa
    import jsonlines
    with jsonlines.open('data_file.jsonl', mode='a') as writer:
        writer.write(new_data)