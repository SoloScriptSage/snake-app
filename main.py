from itertools import count
import pygame
import random
from pygame.version import PygameVersion

# Initialize pygame
pygame.init()

# RGB COLORS
frame_color = (45,10,35)
light_frame_color = (65, 55, 60)
black = (0,0,0)
white = (255,255,255)
grey = (128,128,128)
snake_color = (100, 160, 50)
head_color = (120,200,50)
button_color = (0, 128, 0)
button_hover_color = (0, 255, 0)

# Blocks
size_block = 35
border_thickness = 1
count_block = 20

size = [1000,780]

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake Game')

font = pygame.font.Font(None, 74)
game_over_text = font.render('Game Over!', True, white)
restart_text = font.render('Press Enter to Restart', True, white)
start_text = font.render('Start Game', True, black)

# Logo image to the right
logo_img = pygame.image.load('logo.png')
logo_h = 200
logo_w = 200
logo_resized = pygame.transform.scale(logo_img, (logo_w, logo_h))

# Play button
play_button_font = pygame.font.SysFont('Corbel', 35)
play_button_label = play_button_font.render('Play', True, white)

# Score generation
my_score_font = pygame.font.SysFont("monospace", 25)
score = 0

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def draw_block(color, col, row):
    x = 20 + col * size_block
    y = 20 + row * size_block
    # draw the border
    pygame.draw.rect(screen, white,
                     [x - border_thickness,
                      y - border_thickness,
                      size_block + 2 * border_thickness,
                      size_block + 2 * border_thickness])

    # main block inside the border
    pygame.draw.rect(screen, color,
                     [x, y, size_block, size_block])

class Apple:
    def __init__(self):
        self.x = random.randint(0, count_block - 1)
        self.y = random.randint(0, count_block - 1)

    def draw(self):
        draw_block((255, 0, 0), self.x, self.y)

def draw_start_button():
    button_rect = pygame.Rect(size[0] // 2 - 100, size[1] // 2 - 50, 200, 100)
    pygame.draw.rect(screen, button_color, button_rect)  # Draw the button
    screen.blit(start_text, (size[0] // 2 - 70, size[1] // 2 - 30))  # Draw the button text
    return button_rect

apple = Apple()

# Initial snake blocks
snake_blocks = [
    SnakeBlock(9,8),
    SnakeBlock(9,9),
    SnakeBlock(9,10)
]

# Moves
d_row = 0
d_col = 1

# Frame rate
clock = pygame.time.Clock()

# Main loop
running = True
game_over = False

while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            print('pygame.KEYDOWN')
            if not game_over:  # Only check for directional input when the game is running
                if event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1
            elif event.key == pygame.K_RETURN:
                # Reset the game state if Enter is pressed during game over
                snake_blocks = [
                    SnakeBlock(9, 8),
                    SnakeBlock(9, 9),
                    SnakeBlock(9, 10)
                ]
                score = 0
                apple = Apple()
                d_row = 0
                d_col = 1
                game_over = False

    if not game_over:
        screen.fill(frame_color)

        # Draw the board
        for row in range(count_block):
            for col in range(count_block):
                color = frame_color if (row + col) % 2 == 0 else light_frame_color
                draw_block(color, col, row)

        # Draw the logo
        screen.blit(logo_resized, (750, 20))

        # Draw the score
        score_label = my_score_font.render(f"Score: {score}", 1, white)
        screen.blit(score_label, (750, 250))

        # Draw the apple
        apple.draw()

        # Draw the snake
        for i, block in enumerate(snake_blocks):
            if i == len(snake_blocks) - 1:
                draw_block(head_color, block.x, block.y)
            else:
                draw_block(snake_color, block.x, block.y)

        # Move the snake
        snake_head = snake_blocks[-1]
        new_x = snake_head.x + d_col
        new_y = snake_head.y + d_row

        # Wrap-around `log`ic for x
        if new_x < 0:
            new_x = count_block - 1
        elif new_x >= count_block:
            new_x = 0
        # Wrap-around logic for y
        if new_y < 0:
            new_y = count_block - 1
        elif new_y >= count_block:
            new_y = 0

        new_snake_head = SnakeBlock(new_x, new_y)

        if any(block.x == new_x and block.y == new_y for block in snake_blocks):
            game_over=True
        else:
            if new_snake_head.x == apple.x and new_snake_head.y == apple.y:
                score += 10

                apple = Apple()
            else:
                snake_blocks.pop(0)

            snake_blocks.append(new_snake_head)
    else:
        screen.blit(game_over_text, (size[0] // 2 - 200, size[1] // 2 - 50))
        screen.blit(restart_text, (size[0] // 2 - 250, size[1] // 2 + 50))  # Display restart instruction

    # Update display and control frame rate
    pygame.display.flip()
    clock.tick(10)  # 10 frames per second

# Quit the game
pygame.quit()
