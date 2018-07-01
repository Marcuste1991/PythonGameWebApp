# packet import section
from config import *
import pygame as pg
import math
from random import *
# defined import section

# definition section
vec = pg.math.Vector2
pg.mixer.pre_init(44100, 16, 2, 4096)


class EnemyBullet(pg.sprite.Sprite):
    def __init__(self, game, enemy):
        self.groups = game.all_sprites, game.enemy_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((7, 3), pg.SRCALPHA)
        self.image.fill(RED)
        self.velocity = (math.cos(math.radians(enemy.img_rot)) * ENEMY_BULLET_SPEED + randrange(-2,2),
                         -math.sin(math.radians(enemy.img_rot)) * ENEMY_BULLET_SPEED + randrange(-2,2))
        self.image = pg.transform.rotate(self.image, (enemy.img_rot))
        self.rect = self.image.get_rect(center=(enemy.pos.x, enemy.pos.y))
        self.pos = list(self.rect.center)
        self.bullet_sound()

    def bullet_sound(self):
        shot = pg.mixer.Sound(self.game.sound_folder + "/" + ENEMY_BULLET_SHOT_SOUND)
        shot.set_volume(0.5)
        pg.mixer.Channel(7).play(shot)

    def update(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.center = self.pos
        self.collide_with_walls()
        #self.collide_with_destroyable_sprite()

    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        d_hits = pg.sprite.spritecollide(self, self.game.destroyable_objects, False)
        if d_hits:
            self.kill()
            for d_object in d_hits:
                d_object.break_sound()
                d_object.kill()
        if hits:
            self.kill()

    # def collide_with_destroyable_sprite(self):
    #     d_hits = pg.sprite.spritecollide(self, self.game.destroyable_objects, False)
    #     if d_hits:
    #         self.kill()

    # def collide_with_figure(self):
    #     global f_hits
    #     f_hits = pg.sprite.spritecollide(self, self.game.player, False)
    #
    #     if f_hits:
    #         self.kill()
    #         self.game.player.hp -= 10
    #         print(self.game.player.hp)
