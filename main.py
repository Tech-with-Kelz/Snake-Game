# importing libraries
import pygame
import time
import random

snake_speed = 15

# Window size
x = 720
y = 530

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
gray = pygame.Color(128, 128, 128)
nav_color = pygame.Color(40, 40, 40)  # Dark color for nav bar
golden = pygame.Color(255, 215, 0)    # Color for special food
dark_gray = pygame.Color(64, 64, 64)

# Food sizes
regular_food_size = 10
special_food_size = regular_food_size * 2  # Double the size

# Nav bar dimensions
nav_height = 50
button_width = 80
button_height = 30
# Position buttons vertically centered in nav bar
button_y = (nav_height - button_height) // 2
pause_button = pygame.Rect(x - 190, button_y, button_width, button_height)
exit_button = pygame.Rect(x - 90, button_y, button_width, button_height)

# Game state
paused = False

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Kelz Snake')
game_window = pygame.display.set_mode((x, y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50 + nav_height]

# defining first 4 blocks of snake body
snake_body = [[100, 50 + nav_height],
              [90, 50 + nav_height],
              [80, 50 + nav_height],
              [70, 50 + nav_height]
              ]
# fruit position
fruit_position = [random.randrange(1, (x//10)) * 10, 
                  random.randrange(1, ((y - nav_height)//10)) * 10 + nav_height]

fruit_spawn = True

# Special food variables
special_food_position = None
special_food_timer = 0
special_food_spawn_count = 0
special_food_duration = 4000  # 4                            seconds in milliseconds
special_food_active = False

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

# displaying Score function
def show_score(choice, color, font, size):
  
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)
    
    # create the display surface object 
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)
    
    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()
    
    # Position score in the middle of nav bar
    score_rect.center = (120, nav_height // 2)
    
    # displaying text
    game_window.blit(score_surface, score_rect)

# game over function
def game_over():
  
    # creating font object my_font
    my_font = pygame.font.SysFont('sans serif', 50)
    
    # creating a text surface on which text 
    # will be drawn
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    
    # create a rectangular object for the text 
    # surface object
    game_over_rect = game_over_surface.get_rect()
    
    # setting position of the text
    game_over_rect.midtop = (x/2, (y - nav_height)/4 + nav_height)
    
    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    # after 2 seconds we will quit the program
    time.sleep(2)
    
    # deactivating pygame library
    pygame.quit()
    
    # quit the program
    quit()


# Function to draw a rounded rectangle
def draw_rounded_rect(surface, color, rect, radius):
    """Draw a rectangle with rounded corners"""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Main Function
while True:
    
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            # Add space key for pause/play
            if event.key == pygame.K_SPACE:
                paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if pause_button.collidepoint(mouse_pos):
                paused = not paused
            elif exit_button.collidepoint(mouse_pos):
                pygame.quit()
                quit()

    if not paused:
        # If two keys pressed simultaneously
        # we don't want snake to move into two 
        # directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
            if snake_position[1] < nav_height:
                snake_position[1] = y - 10
        if direction == 'DOWN':
            snake_position[1] += 10
            if snake_position[1] >= y:
                snake_position[1] = nav_height
        if direction == 'LEFT':
            snake_position[0] -= 10
            if snake_position[0] < 0:
                snake_position[0] = x - 10
        if direction == 'RIGHT':
            snake_position[0] += 10
            if snake_position[0] >= x:
                snake_position[0] = 0

        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            special_food_spawn_count += 1
            fruit_spawn = False
            
            # Check if we should spawn special food
            if special_food_spawn_count >= 5 and not special_food_active:
                special_food_position = [
                    random.randrange(1, (x//10)) * 10,
                    random.randrange(1, ((y - nav_height)//10)) * 10 + nav_height
                ]
                special_food_timer = pygame.time.get_ticks()
                special_food_active = True
                special_food_spawn_count = 0
        
        # Check for special food collision
        elif (special_food_active and special_food_position and 
              snake_position[0] >= special_food_position[0] and 
              snake_position[0] < special_food_position[0] + special_food_size and
              snake_position[1] >= special_food_position[1] and 
              snake_position[1] < special_food_position[1] + special_food_size):
            score = score * 2  # Double the current score
            special_food_active = False
            special_food_position = None
            # Add one more segment for each current segment to double the size
            current_length = len(snake_body)
            for _ in range(current_length):  # Add same number of segments as current length
                # Add new segments following the last segment's position
                last_segment = snake_body[-1]
                snake_body.append(list(last_segment))
        else:
            snake_body.pop()
        
        # Check if special food should disappear
        if special_food_active and pygame.time.get_ticks() - special_food_timer > special_food_duration:
            special_food_active = False
            special_food_position = None

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (x//10)) * 10, 
                              random.randrange(1, ((y - nav_height)//10)) * 10 + nav_height]
            
        fruit_spawn = True

    game_window.fill(white)
    
    # Draw navigation bar
    nav_bar = pygame.Rect(0, 0, x, nav_height)
    pygame.draw.rect(game_window, nav_color, nav_bar)
    
    # Draw buttons with rounded corners
    draw_rounded_rect(game_window, dark_gray, pause_button, 10)
    draw_rounded_rect(game_window, dark_gray, exit_button, 10)
    
    # Button text
    font = pygame.font.SysFont('arial', 16)
    pause_text = font.render("PAUSE" if not paused else "PLAY", True, white)
    exit_text = font.render("QUIT", True, white)
    
    # Center text on buttons
    pause_text_rect = pause_text.get_rect(center=pause_button.center)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    
    game_window.blit(pause_text, pause_text_rect)
    game_window.blit(exit_text, exit_text_rect)
    
    # Show score in nav bar (using white color for visibility)
    show_score(1, white, 'times new roman', 24)

    # Adjust game area to be below nav bar
    game_window.fill(white, (0, nav_height, x, y - nav_height))

    # Draw snake and fruit regardless of pause state
    # Draw snake body
    for pos in snake_body:
        pygame.draw.rect(game_window, black,
                         pygame.Rect(pos[0], pos[1], regular_food_size, regular_food_size))
    
    # Draw snake eyes on the head
    if len(snake_body) > 0:
        head_pos = snake_body[0]
        eye_size = 3  # Size of the eyes
        eye_color = pygame.Color(255, 255, 255)  # Yellow eyes
        eye_offset = 2  # Distance of eyes from the edge
        
        # Draw eyes based on direction
        if direction == 'RIGHT':
            # Right-facing eyes
            pygame.draw.circle(game_window, eye_color, 
                             (head_pos[0] + regular_food_size - eye_offset, head_pos[1] + eye_offset), eye_size)
            pygame.draw.circle(game_window, eye_color, 
                             (head_pos[0] + regular_food_size - eye_offset, head_pos[1] + regular_food_size - eye_offset), eye_size)
        elif direction == 'LEFT':
            # Left-facing eyes
            pygame.draw.circle(game_window, eye_color, 
                             (head_pos[0] + eye_offset, head_pos[1] + eye_offset), eye_size)
            pygame.draw.circle(game_window, eye_color, 
                             (head_pos[0] + eye_offset, head_pos[1] + regular_food_size - eye_offset), eye_size)
        elif direction == 'UP':
            # Upward-facing eyes
            pygame.draw.circle(game_window, eye_color, 
                             (head_pos[0] + eye_offset, head_pos[1] + eye_offset), eye_size)
            pygame.draw.circle(game_window, eye_color, 
                             (head_pos[0] + regular_food_size - eye_offset, head_pos[1] + eye_offset), eye_size)
        else:  # DOWN
            # Downward-facing eyes
            pygame.draw.circle(game_window, eye_color, 
                             (head_pos[0] + eye_offset, head_pos[1] + regular_food_size - eye_offset), eye_size)
            pygame.draw.circle(game_window, eye_color, 
                             (head_pos[0] + regular_food_size - eye_offset, head_pos[1] + regular_food_size - eye_offset), eye_size)
    
    # Draw regular food as oval
    pygame.draw.ellipse(game_window, green, pygame.Rect(
        fruit_position[0], fruit_position[1], regular_food_size, regular_food_size))
        
    # Draw special food if active
    if special_food_active and special_food_position:
        # Draw larger golden food as oval
        pygame.draw.ellipse(game_window, golden, pygame.Rect(
            special_food_position[0], special_food_position[1], special_food_size, special_food_size))
            
        # Draw timer bar above special food
        time_left = special_food_duration - (pygame.time.get_ticks() - special_food_timer)
        if time_left > 0:
            bar_width = (time_left / special_food_duration) * special_food_size
            pygame.draw.rect(game_window, red, pygame.Rect(
                special_food_position[0], special_food_position[1] - 5, bar_width, 3))

    # If game is paused, draw a semi-transparent overlay with "PAUSED" text
    if paused:
        # Create a semi-transparent overlay
        pause_overlay = pygame.Surface((x, y - nav_height))
        pause_overlay.set_alpha(128)
        pause_overlay.fill(white)
        game_window.blit(pause_overlay, (0, nav_height))
        
        # Draw "PAUSED" text
        pause_font = pygame.font.SysFont('arial', 48)
        pause_label = pause_font.render('PAUSED', True, black)
        pause_rect = pause_label.get_rect(center=(x/2, (y + nav_height)/2))
        game_window.blit(pause_label, pause_rect)

    # Game Over conditions
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score continuously
    #show_score(1, black, 'times new roman', 20)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
