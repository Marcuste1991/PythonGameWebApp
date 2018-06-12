# packet import section
import pygame as pg
import math

# defined import section
from config import *
from Player import *
from Enemy import *
from Wall import *
from Bullet import *

# definition section
vec = pg.math.Vector2
pg.mixer.pre_init(44100, 16, 2, 4096)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((7, 3), pg.SRCALPHA)
        self.image.fill(YELLOW)
        self.velocity = (math.cos(math.radians(player.img_rot)) * BULLET_SPEED,
                         -math.sin(math.radians(player.img_rot)) * BULLET_SPEED)
        self.image = pg.transform.rotate(self.image, (player.img_rot))
        self.rect = self.image.get_rect(center=(player.pos.x, player.pos.y))
        self.pos = list(self.rect.center)
        self.bullet_sound()

    def bullet_sound(self):
        shot = pg.mixer.Sound(self.game.sound_folder + "/" + BULLET_SHOT_SOUND)
        shot.set_volume(0.5)
        pg.mixer.Channel(0).play(shot)

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.center = self.pos
        self.collide_with_walls()

    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.kill()

    def collide_with_figure(self):
        global f_hits
        if self == self.game.player:
            f_hits = pg.sprite.spritecollide(self, self.game.player, False)
        elif self == self.game.enemies:
            f_hits = pg.sprite.spritecollide(self, self.game.enemies, False)

        if f_hits:
            self.kill()
