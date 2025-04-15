import pygame
import random
import sys
import time
import psycopg2

########################
#  1. POSTGRES SETUP   #
########################

def connect_db():
    return psycopg2.connect(
        host="localhost",
        dbname="suppliers",
        user="postgres",
        password="Almaty2500505"
    )

def get_user_id(username):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user:
                return user[0]
            else:
                cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
                new_id = cur.fetchone()[0]
                conn.commit()
                return new_id

def load_progress(user_id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT score, level 
                FROM user_score 
                WHERE user_id = %s 
                ORDER BY savet_at DESC 
                LIMIT 1
            """, (user_id,))
            row = cur.fetchone()
            return row if row else (0, 0)

def save_progress(user_id, score, level):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_score (user_id, score, level, savet_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            """, (user_id, score, level))
            conn.commit()
    print(f"Progress saved: user_id={user_id}, score={score}, level={level}")

########################
#  2. GAME CONSTANTS   #
########################

USERNAME = input("Enter your username: ")
USER_ID = get_user_id(USERNAME)
score, level = load_progress(USER_ID)

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

eat_sound = None
crash_sound = None
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
    crash_sound = pygame.mixer.Sound("crash.wav")
except:
    print("Optional: place 'eat.wav' and 'crash.wav' in the same folder if you want sound.")

########################
#  3. LEVEL & WALLS    #
########################

def get_level(score):
    if score < 5:
        return 0
    elif score < 10:
        return 1
    else:
        return 2

def get_speed(level):
    if level == 0:
        return 8
    elif level == 1:
        return 12
    else:
        return 15

def get_walls_for_level(level):
    walls = set()
    if level >= 0:
        for x in range(GRID_WIDTH):
            walls.add((x, 0))
            walls.add((x, GRID_HEIGHT - 1))
        for y in range(GRID_HEIGHT):
            walls.add((0, y))
            walls.add((GRID_WIDTH - 1, y))

    if level >= 1:
        for i in range(5, 15):
            walls.add((i, i))

    if level >= 2:
        for i in range(10, 20):
            walls.add((i, GRID_HEIGHT - i))

    return walls

########################
#  4. GAME VARIABLES   #
########################

snake = [(5, 5)]
direction = (1, 0)
game_over = False

food = (0, 0)
food_timer = time.time()
FOOD_LIFETIME = 5
food_value = 1

speed = get_speed(level)
walls = get_walls_for_level(level)

def spawn_food():
    global food, food_timer
    while True:
        new_food = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
        if new_food not in snake and new_food not in walls:
            food = new_food
            food_timer = time.time()
            break

spawn_food()

########################
#  5. DRAW FUNCTIONS   #
########################

def draw_all():
    win.fill(BLACK)

    for x, y in walls:
        pygame.draw.rect(win, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for segment in snake:
         pygame.draw.rect(win, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(win, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    score_text = font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

    pygame.display.update()

def pause_game():
    paused = True
    pause_text = font.render("Paused. Press P to continue.", True, YELLOW)
    win.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

def update_snake():
    global food, score, direction, game_over, level, speed, walls

    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    if new_head in snake or new_head in walls:
        if crash_sound:
            crash_sound.play()
        game_over = True
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += food_value
        level = get_level(score)
        speed = get_speed(level)
        walls = get_walls_for_level(level)
        spawn_food()
        if eat_sound:
            eat_sound.play()
    else:
        snake.pop()

########################
#  6. MAIN LOOP        #
########################

while True:
    if not game_over:
        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress(USER_ID, score, level)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_p:
                    pause_game()

        if time.time() - food_timer > FOOD_LIFETIME:
            spawn_food()

        update_snake()
        draw_all()
    else:
        win.fill(BLACK)
        go_text = font.render("Game Over! Press R to Restart", True, YELLOW)
        sc_text = font.render(f"Final Score: {score}", True, WHITE)
        win.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 30))
        win.blit(sc_text, (WIDTH // 2 - sc_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress(USER_ID, score, level)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                snake = [(5, 5)]
                direction = (1, 0)
                score, level = 0, 0
                speed = get_speed(level)
                walls = get_walls_for_level(level)
                spawn_food()
                game_over = False