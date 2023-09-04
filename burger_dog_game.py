# sound effects https://www.fiftysounds.com
# images "https://www.flaticon.com/free-icons/samoyed

import pygame, random

pygame.init()

# Set display surface
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 7
PLAYER_BOOST_VELOCITY = 15
STARTING_BOOST_LVL = 100
STARTING_BURGER_VEOCITY = 3
BURGER_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

score = 0
burger_points = 0
burger_eaten = 0
burger_velocity = STARTING_BURGER_VEOCITY

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY

boost_level = STARTING_BOOST_LVL

# Set colors
ORANGE = (250, 200, 104)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set fonts
font = pygame.font.Font("font.ttf", 28)

# Set text
points_text = font.render(f"Burger points: {burger_points}", True, ORANGE)
point_rect = points_text.get_rect()
point_rect.topleft = (10, 10)

score_text = font.render(f"Score: {score}", True, ORANGE)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 50)

title_text = font.render("Burger Dog", True, ORANGE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH // 2
title_rect.y = 10

eaten_text = font.render(f"Burgers eaten: {burger_eaten}", True, ORANGE)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = WINDOW_WIDTH // 2
eaten_rect.y = 50

lives_text = font.render(f"Lives: {player_lives}", True, ORANGE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

boost_text = font.render(f"Boost: {boost_level}", True, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH - 10, 50)

game_over_text = font.render(f"Final score: {score}", True, ORANGE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("Press any mouse button to play again", True, ORANGE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

# Import images
left_dog_img = pygame.image.load("left_dog.png")
right_dog_img = pygame.image.load("right_dog.png")
player_img = left_dog_img
player_rect = player_img.get_rect()
player_rect.centerx = WINDOW_WIDTH // 2
player_rect.bottom = WINDOW_HEIGHT

burger_img = pygame.image.load("cheeseburger.png")
burger_rect = burger_img.get_rect()
burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 64), -BUFFER_DISTANCE)

# Import music and sounds
bark_sound = pygame.mixer.Sound("barking_dog.mp3")
bark_sound.set_volume(0.5)
miss_sound = pygame.mixer.Sound("miss_sound.mp3")
miss_sound.set_volume(0.5)
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.15)


# The main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_img = left_dog_img
    if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += player_velocity
        player_img = right_dog_img
    if keys[pygame.K_UP] and player_rect.top > 100:
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity

    # Engage Boost
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = PLAYER_NORMAL_VELOCITY

    # Move the burger and update burger points
    burger_rect.y += burger_velocity
    burger_points = int(burger_velocity * (WINDOW_HEIGHT - burger_rect.y + 100))

    # Player missed the burger
    if burger_rect.y > WINDOW_HEIGHT:
        player_lives -= 1
        miss_sound.play()

        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 64), -BUFFER_DISTANCE)
        burger_velocity = STARTING_BURGER_VEOCITY

        player_rect.centerx = WINDOW_WIDTH // 2
        player_rect.bottom = WINDOW_HEIGHT
        boost_level = STARTING_BOOST_LVL

    # Check for collisions
    if player_rect.colliderect(burger_rect):
        score += burger_points
        burger_eaten += 1
        bark_sound.play()

        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 64), -BUFFER_DISTANCE)
        burger_velocity += BURGER_ACCELERATION

        boost_level += 25
        if boost_level > STARTING_BOOST_LVL:
            boost_level = STARTING_BOOST_LVL

    # Update the HUD
    points_text = font.render(f"Burger points: {burger_points}", True, ORANGE)
    score_text = font.render(f"Score: {score}", True, ORANGE)
    eaten_text = font.render(f"Burgers eaten: {burger_eaten}", True, ORANGE)
    lives_text = font.render(f"Lives: {player_lives}", True, ORANGE)
    boost_text = font.render(f"Boost: {boost_level}", True, ORANGE)

    # Check for GAME OVER
    if player_lives == 0:
        game_over_text = font.render(f"Final score: {score}", True, ORANGE)
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game
        pygame.mixer.music.stop()
        is_pause = True
        while is_pause:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    burger_points = 0
                    burger_eaten = 0
                    burger_velocity = STARTING_BURGER_VEOCITY
                    player_lives = PLAYER_STARTING_LIVES
                    boost_level = STARTING_BOOST_LVL

                    pygame.mixer.music.play(-1, 0.0)
                    is_pause = False

                if event.type == pygame.QUIT:
                    is_pause = False
                    running = False

    # Fill display surface
    display_surface.fill(BLACK)

    # Blit the HUD
    display_surface.blit(points_text, point_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(eaten_text, eaten_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(boost_text, boost_rect)
    pygame.draw.line(display_surface, ORANGE, (0, 100), (WINDOW_WIDTH, 100), 3)

    # Blit assets
    display_surface.blit(player_img, player_rect)
    display_surface.blit(burger_img, burger_rect)

    # Update display surface and tick a clock
    pygame.display.update()
    clock.tick(FPS)

# Quit the game
pygame.quit()
