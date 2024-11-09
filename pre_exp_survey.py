import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Registration Form")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

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
    window.blit(text_surface, pos)

# Main form loop
running = True
while running:
    window.fill(WHITE)

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
    draw_text("Enter Your Details", (WIDTH // 2 - 80, 40), BLUE, font)

    # Display fields and current input
    y_offset = 0
    for field, rect in input_rects.items():
        pygame.draw.rect(window, GRAY if active_field == field else BLACK, rect, 2)
        draw_text(f"{field}:", (rect.x - 140, rect.y + 5), BLACK, small_font)
        draw_text(form_data[field], (rect.x + 5, rect.y + 5), BLACK, small_font)
        y_offset += 60

    # Draw rating radio buttons with labels
    draw_text("Rate Chrome Dino Game (1-5):", (50, 300), BLACK, small_font)
    for i, pos in enumerate(rating_pos):
        color = RED if form_data["Rating_Chrome_Dino_Game"] == rating_options[i] else GRAY
        pygame.draw.circle(window, color, pos, 10)
        pygame.draw.circle(window, BLACK, pos, 10, 1)  # Border around the circle
        draw_text(str(rating_options[i]), (pos[0] - 5, pos[1] - 25), BLACK, small_font)

    # Draw a submit button
    submit_button = pygame.Rect(WIDTH // 2 - 50, 400, 100, 40)
    pygame.draw.rect(window, BLUE, submit_button)
    draw_text("Submit", (submit_button.x + 10, submit_button.y + 5), WHITE, font)

    # Check if submit button was clicked
    if event.type == pygame.MOUSEBUTTONDOWN and submit_button.collidepoint(event.pos):
        print("Form Submitted:", form_data)  # Print or save form data
        running = False  # Exit the form to start the game

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
