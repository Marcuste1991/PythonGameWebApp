# import section
import pygame as pg
import sys
from os import path
from config import *
from map import *

# redefined file structure
# !!!! das sprite file war zu groß und unübersichtlich deswegen hab ich es aufgeteilt !!!!
from Player import *
from Enemy import *
from Wall import *
from Bullet import *

pg.mixer.pre_init(44100, 16, 2, 4096)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE, VERSION)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'img')
        self.sound_folder = path.join(game_folder, 'sounds')
        self.map = Map(path.join(game_folder, 'mapfile.txt'))
        self.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, PLAYER_IMG_SIZE)
        self.enemy_img = pg.image.load(path.join(self.img_folder, ENEMY_IMG)).convert_alpha()
        self.enemy_img = pg.transform.scale(self.enemy_img, ENEMY_IMG_SIZE)

        # load background fx
        sound_background = pg.mixer.music.load(self.sound_folder + "/" + SOUND_BACKGROUND)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

    def initialize(self):
        # initialize all variables and do all the setup for a new game
        EnemyNum = 0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.camera = Camera(self.map.width, self.map.height)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'S':
                    self.player = Player(self, col, row, self.camera)
                if tile == 'E':
                    EnemyNum += 1
                    self.enemy = Enemy(self, col, row, EnemyNum)

    # game loop
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    # update - update all values of objects
    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # bullet update

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Bullet(self, self.player)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.initialize()
    g.run()
    g.show_go_screen()
