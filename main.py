import tkinter as tk
import random

GAME_WIDTH = 700
GAME_HEIGHT = 500
SPEED = 120
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [(0, 0)] * BODY_PARTS
        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        while True:
            x = random.randint(0, (GAME_WIDTH - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT - SPACE_SIZE) // SPACE_SIZE) * SPACE_SIZE

            if (x, y) not in snake.coordinates:
                break

        self.coordinates = (x, y)
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    if new_direction in ('up', 'down', 'left', 'right'):
        opposite_directions = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
        if direction != opposite_directions[new_direction]:
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    return any(part == snake.coordinates[0] for part in snake.coordinates[1:])


def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, font=('consolas', 70), text="GAME OVER", fill="red",
                       tag="gameover")


def restart_game():
    global snake, food, score, direction
    canvas.delete(tk.ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    next_turn(snake, food)


window = tk.Tk()
window.title("Snake game")
window.resizable(True, True)

score = 0
direction = 'down'

label = tk.Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

restart_button = tk.Button(window, text="Restart", command=restart_game, font=('consolas', 20))
restart_button.place(x=0, y=0)

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()  # Ensure the initial window size is set properly

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
