import pygame, sys
from pygame.locals import *
import random, time

class Rectangles():
    def __init__(self, x, y, dim):
        self.x = x
        self.y = y
        self.colour = (255,255,255)
        self.selected = False
        self.dim = dim
    def caught(self):
        self.colour = (255, 100, 100)
        self.selected = True

def safe_check(x, vert):
    sides1 = []
    sides2 = []
    if vert:
        a = x % game_dim[1]
        b = (x - a) / game_dim[1]
        sides1 = [[1, int(a + ((b - 1) * (1 + game_dim[1])))], [1, int((a + 1) + ((b - 1) * (1 + game_dim[1])))], [0, int(x - game_dim[1])]]
        sides2 = [[1, int(a + (b*(1 + game_dim[1])))], [1, int((a + 1) + (b * (1 + game_dim[1])))], [0, int(x + game_dim[1])]]
    else:
        a = x % (game_dim[1] + 1)
        b = (x - a) / (game_dim[1] + 1)
        sides1 = [[0, int((a - 1) + (game_dim[1] * b))], [0, int((a - 1) + (game_dim[1] * (b + 1)))], [1, int(x - 1)]]
        sides2 = [[0, int(a + (game_dim[1] * b))], [0, int(a + (game_dim[1] * (b + 1)))], [1, int(x + 1)]]
    r = -1
    s = -1
    if (b != 0 and vert) or (a != 0 and (not vert)):
        for p in sides1:
            if all_rectangles[p[0]][p[1]].selected:
                r = r * (-2)
    if (b != game_dim[0] and vert) or (a != game_dim[1] and (not vert)):
        for p in sides2:
            if all_rectangles[p[0]][p[1]].selected:
                s = s * (-2)
    if 8 in [r, s]:
        return 2
    elif r < (-1):
        return 0
    elif s < (-1):
        return 0
    else:
        return 1

def player_select(e):
    global game_over
    global last_selected
    global player_turn
    for a in range(len(all_rectangles)):
        for i in range(len(all_rectangles[a])):
            if all_rectangles[a][i].x < e.pos[0] < (all_rectangles[a][i].x + all_rectangles[a][i].dim[0]) and all_rectangles[a][i].y < e.pos[1] < (all_rectangles[a][i].y + all_rectangles[a][i].dim[1]):
                if (not all_rectangles[a][i].selected):
                    player_turn = False
                    all_rectangles[a][i].caught()
                    last_selected = [a, i]
                    if safe_check(i, a == 0) == 2:
                        game_over = True

def generate_values(x):
    global game_over
    poss= []
    for p in range(len(all_rectangles)):
        for q in range(len(all_rectangles[p])):
            if safe_check(q, (p == 0)) == 2:
                poss.append([p, q])
                game_over = True
    if len(poss) >= 1:
        return random.choice(poss)
    else:
        poss = [[], [], []]
    preferred = []
    if last_selected[0] == 0:
        a = x[1] % game_dim[1]
        b = (x[1] - a) / game_dim[1]
        sides1 = [[1, int(a + ((b - 1) * (1 + game_dim[1])))], [1, int((a + 1) + ((b - 1) * (1 + game_dim[1])))],
                  [0, int(x[1] - game_dim[1])]]
        sides2 = [[1, int(a + (b * (1 + game_dim[1])))], [1, int((a + 1) + (b * (1 + game_dim[1])))],
                  [0, int(x[1] + game_dim[1])]]
        if b != 0: preferred.extend(sides1)
        if a != 0: preferred.append([0, x[1] - 1])
        if b != game_dim[1]: preferred.extend(sides2)
        if a != (game_dim[1] - 1):preferred.append([0, x[1] + 1])
    else:
        a = x[1] % (game_dim[1] + 1)
        b = (x[1] - a) / (game_dim[1] + 1)
        sides1 = [[0, int((a - 1) + (game_dim[1] * b))], [0, int((a - 1) + (game_dim[1] * (b + 1)))], [1, int(x[1] - 1)]]
        sides2 = [[0, int(a + (game_dim[1] * b))], [0, int(a + (game_dim[1] * (b + 1)))], [1, int(x[1] + 1)]]
        if b != 0: preferred.append([1, x[1] - (game_dim[1] + 1)])
        if b != (game_dim[1] - 1): preferred.append([1, x[1] + (game_dim[1] + 1)])
        if a != 0: preferred.extend(sides1)
        if a != game_dim[1]: preferred.extend(sides2)
    for p in range(len(all_rectangles)):
        for q in range(len(all_rectangles[p])):
            if safe_check(q, (p == 0)) >= 1:
                if [p, q] in preferred and (not all_rectangles[p][q].selected):
                    poss[0].append([p, q])
                elif (not all_rectangles[p][q].selected):
                    poss[1].append([p, q])
            elif (not all_rectangles[p][q].selected):
                poss[2].append([p, q])
    if len(poss[0]) >= 1:
        return random.choice(poss[0])
    elif len(poss[1]) >= 1:
        return random.choice(poss[1])
    elif len(poss[2]) >= 1:
        return random.choice(poss[2])
    return 0

def screen_move():
    x = generate_values(last_selected)
    all_rectangles[x[0]][x[1]].caught()

def game_main(dimensions):
    global screen
    global fpsClock

    global game_dim
    game_dim = dimensions
    global all_rectangles
    all_rectangles = [[],[]]
    global player_turn
    player_turn = False
    global last_selected
    last_selected = [random.randint(0, 1), random.randint(0, 11)]
    global game_over
    game_over = False
    counter = 0
    recw = int(100*(1/game_dim[1]))
    rec_length_x = int((640 - (recw*(game_dim[0] + 1)))/game_dim[0])
    rec_length_y = int((640 - (recw * (game_dim[1] + 1))) / game_dim[1])
    for x in range(game_dim[0] + 1):
        for y in range(game_dim[1]):
            all_rectangles[0].append(Rectangles(x*(rec_length_x + recw), (y*(rec_length_y + recw)) + recw, [recw, rec_length_y]))
    for x in range(game_dim[0]):
        for y in range(game_dim[1] + 1):
            all_rectangles[1].append(Rectangles((x*(rec_length_x + recw)) + recw, y*(rec_length_y + recw), [rec_length_x, recw]))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and player_turn and (not game_over):
                player_select(event)

        if not game_over:
            if not player_turn:
                counter += 1
                if counter == 10:
                    screen_move()
                    player_turn = True
                    counter = 0
        screen.fill((0,0,0))
        [[pygame.draw.rect(screen, i.colour, Rect(i.x, i.y, i.dim[0], i.dim[1])) for i in a] for a in all_rectangles]
        pygame.display.flip()
        fpsClock.tick(10)
        if game_over:
            time.sleep(2)
            break

def main():
    pygame.init()

    global screen
    global fpsClock
    screen = pygame.display.set_mode((640, 640))
    fpsClock = pygame.time.Clock()
    dim = [3,3]
    while True:
        game_main(dim)
        if dim[0] == dim[1]:
            dim[0] += 1
        else:
            dim[1] += 1

if __name__ == "__main__":
    main()