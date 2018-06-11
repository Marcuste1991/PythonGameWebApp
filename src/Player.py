# packet import section
import pygame as pg
import math

# defined import section
from config import *
from map import collide_hit_rect
from Enemy import *
from Wall import *
from Bullet import *

# definition section
vec = pg.math.Vector2
pg.mixer.pre_init(44100, 16, 2, 4096)

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, camera):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.camera = camera
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.img_rot = 0
        # player stats
        self.enemy_kills = 0
        self.hp = PLAYER_HP
        # logic for ai
        self.posPlayer = self.pos

    def get_keys(self):
        # self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_w] and keys[pg.K_d]:
            self.vel = vec(PLAYER_SPEED, -PLAYER_SPEED) * 0.773
        elif keys[pg.K_w] and keys[pg.K_a]:
            self.vel = vec(-PLAYER_SPEED, -PLAYER_SPEED) * 0.773
        elif keys[pg.K_s] and keys[pg.K_d]:
            self.vel = vec(PLAYER_SPEED, PLAYER_SPEED) * 0.773
        elif keys[pg.K_s] and keys[pg.K_a]:
            self.vel = vec(-PLAYER_SPEED, PLAYER_SPEED) * 0.773

        elif keys[pg.K_w]:
            self.vel = vec(0, -PLAYER_SPEED)
        elif keys[pg.K_s]:
            self.vel = vec(0, PLAYER_SPEED)
        elif keys[pg.K_a]:
            self.vel = vec(-PLAYER_SPEED, 0)
        elif keys[pg.K_d]:
            self.vel = vec(PLAYER_SPEED, 0)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2.0
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2.0
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2.0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2.0
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    # calc rotation of char with mouse
    def rotate(self):
        self.mousex, self.mousey = pg.mouse.get_pos()
        if self.camera.camera.topleft[0] < 0:
            self.mousex -= self.camera.camera.topleft[0]
        if self.camera.camera.topleft[1] < 0:
            self.mousey -= self.camera.camera.topleft[1]
        run, rise = (self.mousex - self.pos.x, self.mousey - self.pos.y)
        self.img_rot = math.degrees(math.atan2(-rise, run))

    def hit_by_enemy(self):
        P_hits = pg.sprite.spritecollide(self, self.game.bullets, False)

        if P_hits:
            if self.hp > 0:
                self.hp -= BULLET_DAMAGE
                # Bullet.collide_with_figure(self.game.player)
            else:
                P_killed = pg.mixer.Sound(self.game.sound_folder + "/" + ENEMY_DEATH_SOUND)
                pg.mixer.Channel(1).play(P_killed)
                self.game.player.kill()
                self.game.enemy.player_kills += 1
                print("Got killed by bots. ---> Game Over!")
                pg.quit()

    def update(self):
        self.get_keys()
        self.rotate()
        # self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        # self.debuggerPlayer()

        # self.hit_by_enemy()
        self.rect.center = self.pos
        self.image = pg.transform.rotate(self.game.player_img, self.img_rot + PLAYER_ROT_ADJUST)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.hit_rect.center
        # print("playerpos:" + str(self.pos[0]) + " " + str(self.pos[1]) +"   mousepos:" + str("(" + str(self.mousex) + "," + str(self.mousey) + ")") + "  camerapos: " + str(self.camera.camera.topleft))

    def debuggerPlayer(self):
        logicalPos = self.posPlayer[0], self.posPlayer[1]
        print("Player :" + str(logicalPos))