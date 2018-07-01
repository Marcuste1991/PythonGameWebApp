# packet import section

# defined import section
from sprites.Player import *
from sprites.Bullet import *
import pygame as pg
from config import *
from math import *
from sprites.EnemyBullet import *
from map import collide_hit_rect
import random

# definition section
vec = pg.math.Vector2
pg.mixer.pre_init(44100, 16, 2, 4096)


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, num):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.hit_rect = ENEMY_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.image = self.game.enemy_img
        self.pos = vec(x, y) * TILESIZE
        self.rot = ENEMY_ROT_ADJUST
        self.img_rot = 0
        self.hp = ENEMY_HP
        self.player_kills = 0
        self.enemy_clock  = pg.time.Clock()
        self.time_since_last = 0


        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        # logic behind ai
        self.distance = 0
        self.eff_dist = 0
        self.num = num
        self.CountEnemy = 21
        # debugging no real function !!!
        self.posEnemy = self.pos[0], self.pos[1], self.num

    def hit_by_player(self):
        E_hits = pg.sprite.spritecollide(self, self.game.bullets, False)

        if E_hits:
            if self.hp > 0:
                self.hp -= BULLET_DAMAGE
                # Bullet.collide_with_figure(self.game.enemies)
            else:
                E_killed = pg.mixer.Sound(self.game.sound_folder + "/" + ENEMY_DEATH_SOUND)
                pg.mixer.Channel(1).play(E_killed)
                self.kill()
                # Bullet.collide_with_figure(self.game.enemies)
                self.game.player.enemy_kills += 1
                print("Enemy killed. Total: " + str(self.game.player.enemy_kills))
                if (self.CountEnemy - self.game.player.enemy_kills) == 0:
                    pg.quit()
                print(self.CountEnemy - self.game.player.enemy_kills)
                self.debuggerEnemy()

    def rotate(self):
        self.x_player = self.game.player.pos.x
        self.y_player = self.game.player.pos.y

        # if self.game.camera.camera.topleft[0] > 0:
        #     self.x_player -= self.game.camera.camera.topleft[0]
        # if self.game.camera.camera.topleft[1] > 0:
        #     self.y_player -= self.game.camera.camera.topleft[1]

        run, rise = (self.x_player - self.rect.x, self.y_player - self.rect.y)
        #run, rise = self.x_player, self.y_player
        self.img_rot = math.degrees(math.atan2(-rise, run))
        #print("Run,rise = " + str([int(run),int(rise)]) + "  EnemyPos = " + str([int(self.rect.x), int(self.rect.x)]) + " Winkel = " + str(self.img_rot))
        self.image = pg.transform.rotate(self.game.enemy_img, self.img_rot)

    def debuggerEnemy(self):
        logicalPos = self.posEnemy
        print("Enemy :" + str(logicalPos))

    # def collide_with_walls(self, dir):
    #     if dir == 'x':
    #         E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
    #         if E_hits:
    #             if self.vel.x > 0:
    #                 self.pos.x = E_hits[0].rect.left - self.hit_rect.width / 2.0
    #             if self.vel.x < 0:
    #                 self.pos.x = E_hits[0].rect.right + self.hit_rect.width / 2.0
    #             self.vel.x = 0
    #             self.hit_rect.centerx = self.pos.x
    #     if dir == 'y':
    #         E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
    #         if E_hits:
    #             if self.vel.y > 0:
    #                 self.pos.y = E_hits[0].rect.top - self.hit_rect.height / 2.0
    #             if self.vel.y < 0:
    #                 self.pos.y = E_hits[0].rect.bottom + self.hit_rect.height / 2.0
    #             self.vel.y = 0
    #             self.hit_rect.centery = self.pos.y

    def update(self):
        self.hit_by_player()
        self.shoot()
        #self.walk_through_map()
        #self.rect.center = self.pos

        #self.image = pg.transform.rotate(self.game.enemy_img, self.img_rot + self.rot)
        #self.rect = self.image.get_rect()
        #self.rect.center = self.pos
        #self.pos += self.vel * self.game.dt
        #self.hit_rect.centerx = self.pos.x
        #self.collide_with_walls('x')
        #elf.hit_rect.centery = self.pos.y
        #self.collide_with_walls('y')
        #self.rect.center = self.hit_rect.center

        self.distance_to_player()

    # def walk_through_map(self):
    #     # enemy should avoid to hit walls and needs to be able to hunt player
    #     # only possible for actual map atm
    #     self.vel = vec(0, 0)
    #     EnNum = 1
    #     maxRange = self.num
    #     for EnNum in range(maxRange):
    #         # 0 -> w, 1 -> a, 2 -> s, 3 -> d
    #         # 4 -> w + d, 5 -> w + a, 6 -> s + d, 7 -> s + a
    #         moveNum = (random.randint(0, 20000) % 7)
    #         EnNum += 1
    #
    #         if moveNum == 4:
    #             self.vel = vec(ENEMY_SPEED, -ENEMY_SPEED) * 0.773
    #             self.rot = 90
    #         elif moveNum == 5:
    #             self.vel = vec(-ENEMY_SPEED, -ENEMY_SPEED) * 0.773
    #             self.rot = 90
    #         elif moveNum == 6:
    #             self.vel = vec(ENEMY_SPEED, ENEMY_SPEED) * 0.773
    #             self.rot = -90
    #         elif moveNum == 7:
    #             self.vel = vec(-ENEMY_SPEED, ENEMY_SPEED) * 0.773
    #             self.rot = -90
    #
    #         elif moveNum == 0:
    #             self.vel = vec(0, -ENEMY_SPEED)
    #             self.rot = 90
    #         elif moveNum == 1:
    #             self.vel = vec(0, ENEMY_SPEED)
    #             self.rot = 180
    #         elif moveNum == 2:
    #             self.vel = vec(-ENEMY_SPEED, 0)
    #             self.rot = 0
    #         elif moveNum == 3:
    #             self.vel = vec(ENEMY_SPEED, 0)
    #             self.rot = -90

    def distance_to_player(self):
        # effective distance with ignoring walls
        # real distance need to include walls for shoot and hunt
        distance = (self.game.player.pos // 80) - (self.game.enemy.pos // 80)
        # print(self.game.player.pos, self.game.enemy.pos) # debug
        coord_distance = distance
        #print(coord_distance)

    def shoot(self):
        self.clock_time = self.enemy_clock.tick()
        if abs(self.rect.x - self.game.player.pos.x) < ENEMY_SHOOT_RANGE and abs(self.rect.y - self.game.player.pos.y) < ENEMY_SHOOT_RANGE*0.773:
            self.rotate()
            self.time_since_last += self.clock_time
            if self.time_since_last > ENEMY_SHOOT_SPEED:
                EnemyBullet(self.game, self)
                self.time_since_last = 0

