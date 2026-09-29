import pygame
import sys
import time

pygame.init()

WIDTH = 1536
HEIGHT = 1024

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Animated Insertion Sort Visualizer")

clock = pygame.time.Clock()

BG = (10, 27, 49)
PANEL = (20, 43, 69)
WHITE = (245, 245, 245)
BLUE = (20, 115, 220)
YELLOW = (255, 205, 35)
RED = (235, 55, 55)
GREEN = (50, 195, 85)
BLACK = (15, 15, 15)
SKIN = (255, 205, 170)
GRAY = (170, 180, 190)

title_font = pygame.font.SysFont("arial", 30, True)
number_font = pygame.font.SysFont("arial", 26, True)
text_font = pygame.font.SysFont("arial", 19)
small_font = pygame.font.SysFont("arial", 17, True)

arr = [8, 3, 6, 1, 9, 2, 5, 4]

original = arr.copy()

BOX_W = 36
BOX_H = 36
GAP = 5

STEP_TIME = 2.5
MOVE_SPEED = 2.0

COLS = 4
ROWS = 4

PANEL_W = WIDTH // COLS
PANEL_H = HEIGHT // ROWS


class Box:

    def __init__(self, value, x, y):
        self.value = value
        self.x = float(x)
        self.y = float(y)
        self.target_x = float(x)
        self.target_y = float(y)
        self.color = BLUE

    def move(self):

        dx = self.target_x - self.x
        dy = self.target_y - self.y

        if abs(dx) < MOVE_SPEED:
            self.x = self.target_x
        else:
            self.x += MOVE_SPEED if dx > 0 else -MOVE_SPEED

        if abs(dy) < MOVE_SPEED:
            self.y = self.target_y
        else:
            self.y += MOVE_SPEED if dy > 0 else -MOVE_SPEED

        return (
            abs(self.x - self.target_x) < 1 and
            abs(self.y - self.target_y) < 1
        )

    def draw(self):

        rect = pygame.Rect(
            int(self.x),
            int(self.y),
            BOX_W,
            BOX_H
        )

        pygame.draw.rect(
            screen,
            self.color,
            rect,
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            BLACK,
            rect,
            2,
            border_radius=4
        )

        text = number_font.render(
            str(self.value),
            True,
            WHITE
        )

        text_rect = text.get_rect(
            center=rect.center
        )

        screen.blit(text, text_rect)


def draw_stickman(x, y, carrying=False):

    x = int(x)
    y = int(y)

    pygame.draw.circle(
        screen,
        WHITE,
        (x, y - 45),
        15
    )

    pygame.draw.line(
        screen,
        WHITE,
        (x, y - 30),
        (x, y + 20),
        4
    )

    pygame.draw.line(
        screen,
        WHITE,
        (x, y - 15),
        (x - 25, y + 5),
        4
    )

    pygame.draw.line(
        screen,
        WHITE,
        (x, y - 15),
        (x + 25, y + 5),
        4
    )

    pygame.draw.line(
        screen,
        WHITE,
        (x, y + 20),
        (x - 18, y + 50),
        4
    )

    pygame.draw.line(
        screen,
        WHITE,
        (x, y + 20),
        (x + 18, y + 50),
        4
    )

    if carrying:

        pygame.draw.circle(
            screen,
            SKIN,
            (x + 28, y - 5),
            5
        )


def draw_panel(index, heading, description):

    row = index // 4
    col = index % 4

    px = col * PANEL_W
    py = row * PANEL_H

    pygame.draw.rect(
        screen,
        PANEL,
        (px, py, PANEL_W, PANEL_H)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (px, py, PANEL_W, PANEL_H),
        2
    )

    heading_text = title_font.render(
        heading,
        True,
        WHITE
    )

    screen.blit(
        heading_text,
        (px + 18, py + 15)
    )

    desc = text_font.render(
        description,
        True,
        WHITE
    )

    desc_rect = desc.get_rect(
        center=(px + PANEL_W // 2, py + 225)
    )

    screen.blit(
        desc,
        desc_rect
    )


def draw_array(data, panel_index, colors=None):

    row = panel_index // 4
    col = panel_index % 4

    px = col * PANEL_W
    py = row * PANEL_H

    total = (
        len(data) * BOX_W +
        (len(data) - 1) * GAP
    )

    start_x = px + (PANEL_W - total) // 2
    y = py + 120

    for i, value in enumerate(data):

        colour = BLUE

        if colors and i in colors:
            colour = colors[i]

        rect = pygame.Rect(
            start_x + i * (BOX_W + GAP),
            y,
            BOX_W,
            BOX_H
        )

        pygame.draw.rect(
            screen,
            colour,
            rect,
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            BLACK,
            rect,
            2,
            border_radius=4
        )

        number = number_font.render(
            str(value),
            True,
            WHITE
        )

        number_rect = number.get_rect(
            center=rect.center
        )

        screen.blit(number, number_rect)


def panel_position(index):

    row = index // 4
    col = index % 4

    return (
        col * PANEL_W,
        row * PANEL_H
    )


def draw_input_panel():

    draw_panel(
        0,
        "Insertion Sort Visualizer",
        "Initial array"
    )

    draw_array(arr, 0)

    px, py = panel_position(0)

    text = text_font.render(
        "Input: " + str(original),
        True,
        (150, 220, 255)
    )

    screen.blit(
        text,
        (px + 25, py + 190)
    )


def draw_step_panel(
        panel,
        heading,
        data,
        description,
        key_index=-1,
        red_indices=None,
        green_indices=None):

    draw_panel(
        panel,
        heading,
        description
    )

    colours = {}

    if green_indices:
        for i in green_indices:
            colours[i] = GREEN

    if red_indices:
        for i in red_indices:
            colours[i] = RED

    if key_index >= 0:
        colours[key_index] = YELLOW

    draw_array(
        data,
        panel,
        colours
    )

    px, py = panel_position(panel)

    draw_stickman(
        px + 70,
        py + 165,
        key_index >= 0
    )

    if key_index >= 0:

        key_x = px + 105
        key_y = py + 135

        rect = pygame.Rect(
            key_x,
            key_y,
            BOX_W,
            BOX_H
        )

        pygame.draw.rect(
            screen,
            YELLOW,
            rect,
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            BLACK,
            rect,
            2
        )

        text = number_font.render(
            str(data[key_index]),
            True,
            WHITE
        )

        screen.blit(
            text,
            text.get_rect(center=rect.center)
        )


def draw_final_panel():

    draw_panel(
        15,
        "Final Sorted Array",
        "Insertion Sort Completed!"
    )

    draw_array(
        [1, 2, 3, 4, 5, 6, 8, 9],
        15,
        {
            0: GREEN,
            1: GREEN,
            2: GREEN,
            3: GREEN,
            4: GREEN,
            5: GREEN,
            6: GREEN,
            7: GREEN
        }
    )

    px, py = panel_position(15)

    input_text = text_font.render(
        "Input: " + str(original),
        True,
        (150, 220, 255)
    )

    output_text = text_font.render(
        "Output: [1, 2, 3, 4, 5, 6, 8, 9]",
        True,
        GREEN
    )

    screen.blit(
        input_text,
        (px + 25, py + 170)
    )

    screen.blit(
        output_text,
        (px + 25, py + 200)
    )


def draw_all_panels(active):

    screen.fill(BG)

    draw_input_panel()

    draw_step_panel(
        1,
        "1. Key = 3",
        [8, 3, 6, 1, 9, 2, 5, 4],
        "Pick up key (3)",
        1
    )

    draw_step_panel(
        2,
        "2. Carrying key (3)",
        [8, 3, 6, 1, 9, 2, 5, 4],
        "Move to correct position",
        1
    )

    draw_step_panel(
        3,
        "3. Compare 3 with 8",
        [8, 3, 6, 1, 9, 2, 5, 4],
        "8 > 3  →  shift right",
        -1,
        [0]
    )

    draw_step_panel(
        4,
        "4. Shift 8 right",
        [3, 8, 6, 1, 9, 2, 5, 4],
        "Move 8 one position right",
        0,
        [1]
    )

    draw_step_panel(
        5,
        "5. Place 3",
        [3, 8, 6, 1, 9, 2, 5, 4],
        "3 placed correctly",
        -1,
        None,
        [0]
    )

    draw_step_panel(
        6,
        "6. Key = 6",
        [3, 8, 6, 1, 9, 2, 5, 4],
        "Pick up key (6)",
        2
    )

    draw_step_panel(
        7,
        "7. Compare 6 with 8",
        [3, 8, 6, 1, 9, 2, 5, 4],
        "8 > 6  →  shift right",
        -1,
        [1]
    )

    draw_step_panel(
        8,
        "8. Shift 8 right",
        [3, 6, 8, 1, 9, 2, 5, 4],
        "Move 8 one position right",
        1,
        [2]
    )

    draw_step_panel(
        9,
        "9. Place 6",
        [3, 6, 8, 1, 9, 2, 5, 4],
        "6 placed correctly",
        -1,
        None,
        [0, 1]
    )

    draw_step_panel(
        10,
        "10. Key = 1",
        [3, 6, 8, 1, 9, 2, 5, 4],
        "Pick up key (1)",
        3
    )

    draw_step_panel(
        11,
        "11. Shift 8, 6, 3",
        [3, 6, 8, 1, 9, 2, 5, 4],
        "Shift larger elements right",
        3,
        [0, 1, 2]
    )

    draw_step_panel(
        12,
        "12. Place 1",
        [1, 3, 6, 8, 9, 2, 5, 4],
        "1 placed correctly",
        -1,
        None,
        [0, 1, 2, 3]
    )

    draw_step_panel(
        13,
        "13. Continue",
        [1, 2, 3, 4, 5, 6, 8, 9],
        "Process repeats for 2, 5, 4",
        -1,
        None,
        [0, 1, 2, 3, 4, 5, 6, 7]
    )

    draw_final_panel()

    # Highlight currently active panel
    row = active // 4
    col = active % 4

    pygame.draw.rect(
        screen,
        YELLOW,
        (
            col * PANEL_W + 3,
            row * PANEL_H + 3,
            PANEL_W - 6,
            PANEL_H - 6
        ),
        4
    )


active_panel = 0
last_change = time.time()
paused = False

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_r:
                active_panel = 0
                last_change = time.time()

    if not paused:

        if time.time() - last_change > STEP_TIME:

            active_panel += 1
            last_change = time.time()

            if active_panel > 15:
                active_panel = 0

    draw_all_panels(active_panel)

    pygame.display.flip()

    clock.tick(60)