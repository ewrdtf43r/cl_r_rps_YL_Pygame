import pygame
import csv

import os
import sys

import random

side_winner = None
time_win = 0
kill_player = 0
kill_enemy = 0

game_over = False


def change_kill_player(var):
    global kill_player
    kill_player = var


def get_kill_player():
    return kill_player


def change_kill_enemy(var):
    global kill_enemy
    kill_enemy = var


def get_kill_enemy():
    return kill_enemy


def change_time_win(var):
    global time_win
    time_win = var


def get_time_win():
    return time_win


def change_game_over(var):
    global game_over
    game_over = var


def game(level, speed, hp_base):
    global time_win
    global kill_player
    global kill_enemy
    global game_over


    with open(level, encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        level_data = list(reader)
        way_start_player_pos = [elem[0].split(",") for elem in
                                [elem.split(";") for elem in level_data[0]["way"].split("|")]]
        way_start_enemy_pos = [elem[-1].split(",") for elem in
                               [elem.split(";") for elem in level_data[0]["way"].split("|")]]
        h_w_cell = level_data[0]["h_w_cell"].split(",")

        player_tick = speed // 2
        enemy_tick = 0

        fps = 60

        print(level_data)
        print(way_start_player_pos)
        print(h_w_cell)

        print(str([elem.split(";")[1:] for elem in level_data[0]["way"].split("|")]))

    pygame.init()
    pygame.font.init()
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    player_unit = pygame.sprite.Group()
    enemy_unit = pygame.sprite.Group()

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    class Unit(pygame.sprite.Sprite):

        def __init__(self, *group, type_unit=None, side=None):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(*group)

            self.add(player_unit if side == "player" else enemy_unit)

            if type_unit == "paper":
                self.image = load_image("sprites/paper/paper-50-0.png")
            elif type_unit == "rock":
                self.image = load_image("sprites/rock/rock-50-0.png")
            elif type_unit == "scissors":
                self.image = load_image("sprites/scissors/scissors-50-0.png")
            self.type_unit = type_unit

            self.rect = self.image.get_rect()
            self.side = side
            self.start_pos = None
            self.enemy_c = False

        def update(self, board, event=None):
            if self.side == "player":
                if player_tick == 0:
                    self.update_movement()
                if pygame.sprite.spritecollideany(self, enemy_unit):
                    print(pygame.sprite.spritecollideany(self, enemy_unit))
                    if pygame.sprite.spritecollideany(self, enemy_unit).get_type_unit() == "paper" and self.type_unit == "scissors" or pygame.sprite.spritecollideany(self, enemy_unit).get_type_unit() == "rock" and self.type_unit == "paper" or pygame.sprite.spritecollideany(self, enemy_unit).get_type_unit() == "scissors" and self.type_unit == "rock":
                        change_kill_player(get_kill_player() + 1)
                        pygame.sprite.spritecollideany(self, enemy_unit).kill()
                    elif pygame.sprite.spritecollideany(self, enemy_unit).get_type_unit() == self.type_unit:
                        change_kill_enemy(get_kill_enemy() + 1)
                        change_kill_player(get_kill_player() + 1)
                        pygame.sprite.spritecollideany(self, enemy_unit).kill()
                        self.kill()
                    else:
                        change_kill_enemy(get_kill_enemy() + 1)
                        self.kill()

            elif self.side == "enemy":
                if enemy_tick == 0:
                    self.update_movement()
                if pygame.sprite.spritecollideany(self, player_unit):
                    print(pygame.sprite.spritecollideany(self, player_unit))


        def spawn(self, board, cell):
            self.rect.x = cell[0] * 50 + board.get_left_and_top()[1]
            self.rect.y = cell[1] * 50 + board.get_left_and_top()[0]
            self.cell = cell
            if self.side == "player":
                self.start_pos = (cell if cell in list(
                    map(lambda x: tuple(map(lambda y: int(y), x)), way_start_player_pos)) else self.start_pos)
            else:
                self.start_pos = (cell if cell in list(
                    map(lambda x: tuple(map(lambda y: int(y), x)), way_start_enemy_pos)) else self.start_pos)
            #print(self.start_pos)
            #print(self.cell)


        def get_cell(self):
            return self.cell

        def get_side(self):
            return self.side

        def get_type_unit(self):
            return self.type_unit

        def update_movement(self):
            enemy_c = False
            if self.side == "player" and not game_over:
                try:
                    section = way_start_player_pos.index(list(map(lambda x: str(int(x)), self.start_pos)))
                    path = level_data[0]["way"].split("|")[section].split(";")
                    new_cell = path[path.index(",".join(list(map(lambda x: str(int(x)), self.cell)))) + 1]
                except IndexError:
                    enemy_base.hearth()
                    self.kill()
                    return
            elif self.side == "enemy" and not game_over:
                section = way_start_enemy_pos.index(list(map(lambda x: str(int(x)), self.start_pos)))
                path = level_data[0]["way"].split("|")[section].split(";")
                if path[path.index(",".join(list(map(lambda x: str(int(x)), self.cell)))) - 1].split(",") not in way_start_player_pos and not self.enemy_c:
                    new_cell = path[path.index(",".join(list(map(lambda x: str(int(x)), self.cell)))) - 1]
                elif path[path.index(",".join(list(map(lambda x: str(int(x)), self.cell)))) - 1].split(",") in way_start_player_pos and not self.enemy_c:
                    new_cell = path[path.index(",".join(list(map(lambda x: str(int(x)), self.cell)))) - 1]
                    self.enemy_c = True
                else:
                    player_base.hearth()
                    self.kill()
                    return

            else:
                return
            self.spawn(board, tuple(map(lambda x: float(x), new_cell.split(","))))

           # print(self.get_cell(), self.get_side(), self.get_type_unit())
           # print(path.index(",".join(list(map(lambda x: str(int(x)), self.start_pos)))))
           # print(path)
           # print(",".join(list(map(lambda x: str(int(x)), self.start_pos))))
           # print(section)
           # print(tuple(map(lambda x: float(x), new_cell.split(","))))


    class Base(pygame.sprite.Sprite):

        def __init__(self, *group, side=None):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(*group)

            self.add(player_unit if side == "player" else enemy_unit)

            self.image = load_image("sprites/base/basе-100-0.jpg")

            self.type_unit = "base"

            self.rect = self.image.get_rect()

            self.side = side

            self.hp = hp_base


        def update(self, board, event=None):
            pass

        def spawn(self, board, cell):
            self.rect.x = cell[0] * 50 + board.get_left_and_top()[1]
            self.rect.y = cell[1] * 50 + board.get_left_and_top()[0]
            self.cell = cell

        def get_cell(self):
            return self.cell

        def get_cell(self):
            return self.cell

        def get_side(self):
            return self.side

        def get_type_unit(self):
            return self.type_unit

        def hearth(self):
            self.hp -= 5
            print(self.hp)
            if self.hp <= 0:
                change_game_over(self.side)
                self.kill()


    class Board:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.board = [[0] * width for _ in range(height)]
            self.left = 10
            self.top = 10
            self.cell_size = 50
            self.way = [elem.split(";") for elem in level_data[0]["way"].split("|")]

        # настройка внешнего вида
        def set_view(self, left, top, cell_size):
            self.top = top
            self.left = left
            self.cell_size = cell_size

        print(way_start_player_pos)
        print(way_start_player_pos + way_start_enemy_pos)
        def render(self, screen):
            for j in range(self.height):
                for i in range(self.width):
                    if f"{i},{j}" in str([elem.split(";")[1:-1] for elem in level_data[0]["way"].split("|")]):
                        pygame.draw.rect(screen, pygame.Color("green"), (i * self.cell_size + self.top, j * self.cell_size + self.left, self.cell_size, self.cell_size), 1)
                    else:
                        pygame.draw.rect(screen, pygame.Color("blue") if any(map(lambda x: True if int(x[0]) == i and int(x[1]) == j else False, way_start_player_pos + way_start_enemy_pos)) else pygame.Color("black"), (i * self.cell_size + self.top, j * self.cell_size + self.left, self.cell_size, self.cell_size), 1)

        def get_left_and_top(self):
            return (self.left, self.top)

        def get_cell(self, mouse_pos):
            coord = ((mouse_pos[0] - self.top) // self.cell_size, (mouse_pos[1] - self.left) // self.cell_size)
            return None if coord[0] >= len(self.board[0]) or coord[0] < 0 or coord[1] >= len(self.board) or coord[1] < 0 else coord

        def get_cell_size(self):
            return self.cell_size

        def get_board(self):
            return self.board

        def on_click(self, cell):
            if cell:
                pass

        def get_click(self, mouse_pos):
            cell = self.get_cell(mouse_pos)
            print(cell)
            self.on_click(cell)


    board = Board(int(h_w_cell[0]), int(h_w_cell[1]))
    board.set_view(width / 2 - (len(board.get_board()) / 2 * board.get_cell_size()), height / 2 - (len(board.get_board()[0]) / 2 * board.get_cell_size()), 50)

    subject_selection = "paper"

    player_base = Base(all_sprites, side="player")
    enemy_base = Base(all_sprites, side="enemy")
    player_base.spawn(board, tuple(map(lambda x: int(x), level_data[0]["base_player"].split(","))))
    enemy_base.spawn(board, tuple(map(lambda x: int(x), level_data[0]["base_enemy"].split(","))))

    clock = pygame.time.Clock()

    running = True

    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('Some Text', False, (0, 0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(board.get_cell(event.pos))
                if board.get_cell(event.pos):
                    cell = board.get_cell(event.pos)
                    if any(map(lambda x:
                               True if int(x[0]) == cell[0] and int(x[1]) == cell[1] else False, way_start_player_pos)) \
                            and cell not in [elem.get_cell() for elem in player_unit.sprites()] and not game_over:
                        Unit(all_sprites, type_unit=subject_selection, side="player").spawn(board, board.get_cell(event.pos))

            elif event.type == pygame.KEYDOWN:
                if event.key == 49:
                    subject_selection = "paper"
                elif event.key == 50:
                    subject_selection = "rock"
                elif event.key == 51:
                    subject_selection = "scissors"
        if enemy_tick == player_tick // 2 and not game_over:
            #print(random.choice(tuple(map(lambda x: tuple(map(lambda y: int(y), x)), way_start_enemy_pos))))
            Unit(all_sprites, type_unit=random.choice(('paper', 'rock', 'scissors')), side="enemy").spawn(board, random.choice(tuple(map(lambda x: tuple(map(lambda y: int(y), x)), way_start_enemy_pos))))


        screen.fill((255, 255, 255))
        board.render(screen)
        all_sprites.update(board)
        all_sprites.draw(screen)
        if game_over:
            win_text_surface = my_font.render(f"{'enemy' if game_over == 'player' else 'player'} win", False, (0, 0, 0))
            screen.blit(win_text_surface, (width // 2.5, height // 15))
            print("time: ", get_time_win() // 60)
            print("kill enemy: ", get_kill_enemy())
            print("kill player: ", get_kill_player())
        else:
            change_time_win(get_time_win() + 1)
        clock.tick(fps)
        pygame.display.flip()

        player_tick += 1
        enemy_tick += 1

        if player_tick >= speed:
            player_tick = 0
        if enemy_tick >= speed:
            enemy_tick = 0


game("data/levels/1_level.csv", 50, 10)