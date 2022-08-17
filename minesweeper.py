import pygame
from pygame.constants import *
import sys
import time
import random
from configparser import ConfigParser


class Game:
    def __init__(self):
        pygame.init()
        self.map_size_x = int(self.read_ini("settings.ini", "game", "size_x"))
        self.map_size_y = int(self.read_ini("settings.ini", "game", "size_y"))
        self.mine_count = int(self.read_ini("settings.ini", "game", "mines"))
        self.blsz_x = int(self.read_ini("settings.ini", "game", "blsz_x"))
        self.blsz_y = int(self.read_ini("settings.ini", "game", "blsz_y"))

        self.screen = pygame.display.set_mode((self.blsz_x*self.map_size_x, self.blsz_y*self.map_size_y))
        self.pics = {"1": pygame.transform.smoothscale(pygame.image.load("1.png"), (self.blsz_x, self.blsz_y)),
                     "2": pygame.transform.smoothscale(pygame.image.load("2.png"), (self.blsz_x, self.blsz_y)),
                     "3": pygame.transform.smoothscale(pygame.image.load("3.png"), (self.blsz_x, self.blsz_y)),
                     "4": pygame.transform.smoothscale(pygame.image.load("4.png"), (self.blsz_x, self.blsz_y)),
                     "5": pygame.transform.smoothscale(pygame.image.load("5.png"), (self.blsz_x, self.blsz_y)),
                     "6": pygame.transform.smoothscale(pygame.image.load("6.png"), (self.blsz_x, self.blsz_y)),
                     "7": pygame.transform.smoothscale(pygame.image.load("7.png"), (self.blsz_x, self.blsz_y)),
                     "8": pygame.transform.smoothscale(pygame.image.load("8.png"), (self.blsz_x, self.blsz_y)),
                     "block": pygame.transform.smoothscale(pygame.image.load("block.png"), (self.blsz_x, self.blsz_y)),
                     "mark": pygame.transform.smoothscale(pygame.image.load("mark.png"), (self.blsz_x, self.blsz_y)),
                     "mine": pygame.transform.smoothscale(pygame.image.load("mine.png"), (self.blsz_x, self.blsz_y)),
                     "not_a_mine": pygame.transform.smoothscale(pygame.image.load("not_a_mine.png"),
                                                                (self.blsz_x, self.blsz_y)),
                     "opened": pygame.transform.smoothscale(pygame.image.load("opened.png"),
                                                            (self.blsz_x, self.blsz_y)),
                     "question": pygame.transform.smoothscale(pygame.image.load("question.png"),
                                                              (self.blsz_x, self.blsz_y)),
                     "trigger": pygame.transform.smoothscale(pygame.image.load("trigger.png"),
                                                             (self.blsz_x, self.blsz_y)),
                     "win": pygame.transform.smoothscale(pygame.image.load("win.png"),
                                                            (self.map_size_x*self.blsz_x, self.map_size_y*self.blsz_y)),
                     "lose": pygame.transform.smoothscale(pygame.image.load("lose.png"),
                                                          (self.map_size_x * self.blsz_x,
                                                           self.map_size_y * self.blsz_y)),
                     "icon": pygame.image.load("icon.png")

                     }

        pygame.display.set_icon(self.pics["icon"])
        self.mine_map = []
        self.ground = []
        self.slist = ((-1, -1), (0, -1), (1, -1),
                      (-1, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1))
        temp = []
        for i in range(self.map_size_x):
            temp.append("block")
        for j in range(self.map_size_y):
            self.mine_map.append(temp.copy())
            self.ground.append(temp.copy())
        self.opened = []
        self.status = "running"
        self.keyprs = []
        self.fps = 0
        self.opened_count = 0
        self.flag_count = 0

        self.generate_mines((self.map_size_x, self.map_size_y), self.mine_count)
        self.generate_mine_map((self.map_size_x, self.map_size_y))

        self.running()

    def running(self):
        temp = ["block", "mark", "question"]
        test_fps = 0
        timer = 0
        start_time = time.time()
        while True:
            self.keyprs = pygame.key.get_pressed()
            now_time = time.time()-start_time
            self.opened_count = self.opened_counter(self.ground)
            self.flag_count = self.flag_counter(self.ground)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    cy = event.pos[1] // self.blsz_y
                    cx = event.pos[0] // self.blsz_x
                    if event.button == 1 and self.status == "running":
                        if self.ground[cy][cx] in ["block", "question"]:
                            self.open(cx, cy, (self.map_size_x, self.map_size_y))
                    elif event.button == 3 and self.status == "running":
                        if self.ground[cy][cx] in temp:
                            self.ground[cy][cx] = temp[(temp.index(self.ground[cy][cx])+1) % 3]

            if self.mine_count == self.opened_count:
                self.status = "win"

            self.paint(self.ground, (self.map_size_x, self.map_size_y))
            if self.status == "running":
                pass
            elif self.status == "gameover":
                self.screen.blit(self.pics["lose"], (0, 0))
            elif self.status == "win":
                self.screen.blit(self.pics["win"], (0, 0))
                if self.keyprs[K_r]:
                    self.__init__()
            if self.keyprs[K_r]:
                self.__init__()

            pygame.display.update()
            test_fps += 1
            if now_time > timer+1:
                timer = now_time
                self.fps = test_fps
                test_fps = 0
                pygame.display.set_caption("Minesweeper 1.1 [{}] FPS:{} by chenchen".format(
                    str(self.mine_count-self.flag_count), str(self.fps)))

    def generate_mines(self, size: tuple, counts, click: tuple = None):
        for i in range(counts):
            while 1:
                x = random.randint(0, size[0] - 1)
                y = random.randint(0, size[1] - 1)
                if (x, y) != click and self.mine_map[y][x] != "mine":
                    self.mine_map[y][x] = "mine"
                    break

    def generate_mine_map(self, size: tuple):
        for y in range(size[1]):
            for x in range(size[0]):
                if self.mine_map[y][x] != "mine":
                    count = 0
                    for dx, dy in self.slist:
                        if ((x + dx) >= 0 and x + dx <= size[0] - 1) and ((y + dy) >= 0 and y + dy <= size[1] - 1):
                            if self.mine_map[y + dy][x + dx] == "mine":
                                count += 1
                    if count > 0:
                        self.mine_map[y][x] = str(count)
                    else:
                        self.mine_map[y][x] = "block"

    def open(self, x, y, size: tuple):
        self.opened = []
        if self.mine_map[y][x] == "mine":
            self.show_all_mines(self.mine_map, (self.map_size_x, self.map_size_y))
            self.ground[y][x] = "trigger"
            self.status = "gameover"
        elif self.mine_map[y][x] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            self.ground[y][x] = self.mine_map[y][x]
        else:
            self.opened.append((x, y))
            if self.mine_map[y][x] == "block":
                self.ground[y][x] = "opened"
            self.opening(x, y, size)

    def opening(self, x, y, size: tuple):
        for dx, dy in self.slist:
            if ((x + dx) >= 0 and x + dx <= size[0] - 1) and ((y + dy) >= 0 and y + dy <= size[1] - 1):
                if not (x + dx, y + dy) in self.opened:
                    self.opened.append((x + dx, y + dy))
                    if not self.ground[y+dy][x+dx] in ["mark"]:
                        if self.mine_map[y+dy][x+dx] == "block":
                            self.ground[y+dy][x+dx] = "opened"
                            self.opening(x+dx, y+dy, size)
                        elif self.mine_map[y+dy][x+dx] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                            self.ground[y+dy][x+dx] = self.mine_map[y+dy][x+dx]

    def debug_print(self, something):
        for i in something:
            for j in i:
                if j == "block":
                    print("-", end=" ")
                elif j == "mine":
                    print("m", end=" ")
                elif j == "opened":
                    print(" ", end=" ")
                else:
                    print(j, end=" ")
            print()

    def paint(self, map, size: tuple):
        self.screen.fill((255, 255, 255))
        for y in range(size[1]):
            for x in range(size[0]):
                self.screen.blit(self.pics[map[y][x]], (x*self.blsz_x, y*self.blsz_y))

    def read_ini(self, path, ini0, ini1):
        config = ConfigParser()
        config.read(path)
        convaluse = config.get(ini0, ini1)
        return convaluse

    def font(self, text, font_name, size, color=(0, 0, 0)):
        temp = pygame.font.Font(font_name, size)
        return temp.render(text, True, color)

    def opened_counter(self, ground):
        # 计算未打开的格子数量
        ct = 0
        for y in ground:
            for x in y:
                if x in ["block", "mark", "question"]:
                    ct += 1
        return ct

    def flag_counter(self, ground):
        ct = 0
        for y in ground:
            for x in y:
                if x in ["mark"]:
                    ct += 1
        return ct

    def show_all_mines(self, mine_map, size: tuple):
        for y in range(size[1]):
            for x in range(size[0]):
                if mine_map[y][x] == "mine":
                    if self.ground[y][x] == "mark":
                        pass
                    else:
                        self.ground[y][x] = "mine"
                elif self.ground[y][x] == "mark":
                    self.ground[y][x] = "not_a_mine"


Game()
