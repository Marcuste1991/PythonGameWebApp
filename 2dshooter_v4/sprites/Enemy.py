# packet import section

import time, datetime, os
import easygui  # easy_install easygui !!! important for Username input !!!!!!
import pygame as pg
# defined import section
from config import *
from map import *
from sprites.Wall import *
from sprites.Bullet import *
from sprites.Player import *
from sprites.ActionArea import *
from math import *
from sprites.EnemyBullet import *
from prettytable import PrettyTable

# definition section
vec = pg.math.Vector2
pg.mixer.pre_init(44100, 16, 2, 4096)

# Enemy Counter for Quit Game at Win #
global xnum
global max_num
max_num = [0]  # needed here otherwise it would be rewrite every time it gets used


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
        self.enemy_clock = pg.time.Clock()
        self.time_since_last = 0

        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        # logic behind ai
        self.distance = self.EnemyNum = 0
        self.eff_dist = 0
        self.num = num
        self.exec = False
        # debugging no real function !!!
        # self.posEnemy = self.pos[0], self.pos[1], self.num

    def on_objective_keypressed(self):
        keys = pg.key.get_pressed()

        objective = {}
        height = {}

        if keys[pg.K_o]:
            objective[0] = "Remaining Enemies: " + str(self.CountEnemy() - self.game.player.enemy_kills)
            height[0] = 60
            objective[1] = "Gate opened: " + str(self.game.a_area.Gate_open)
            height[1] = 90

            print(len(objective))

            self.game.a_area.objective_text(objective[0], height[0])
            self.game.a_area.objective_text(objective[1], height[1])

    # os path to scorefiles
    def score_switch(self, file):
        score_file = os.path.abspath("scores/" + file)

        return score_file

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
                # Game Win Sequence with Scoreboard Writing
                if (self.CountEnemy() - self.game.player.enemy_kills) == 0:
                    Time = datetime.datetime.now()

                    PlayerName = easygui.enterbox(
                        msg="Please enter your Name below: ",
                        title="Name input  for Scoreboard!",
                        strip=True,  # will remove whitespace around whatever the user types in
                        default="Username")

                    overTime = Time - self.game.Time_start
                    convert_time = overTime.total_seconds()

                    if os.path.exists(self.score_switch("score.txt")) and os.path.getsize(self.score_switch("score.txt")):
                        with open(self.score_switch("score.txt"), "r+") as f:
                            f.read()
                            f.seek(0, 2)
                            f.writelines(
                                str("\n" + PlayerName + " | " + str(convert_time) + " | " + str(datetime.date.today())))
                        f.close()
                    else:
                        with open(self.score_switch("score.txt"), "r+") as f:
                            f.read()
                            f.seek(0, 2)
                            f.writelines(
                                str(PlayerName + " | " + str(convert_time) + " | " + str(datetime.date.today())))
                        f.close()

                    self.exec = True
                    text_1 = 'All Enemies killed!'
                    text_2 = 'You win!'
                    text = text_1 + ".." + text_2
                    self.game.a_area.event_display_text(text)
                    time.sleep(5)

                    ####################################################################################################
                    # Scoreboard output ### Pretty Tables hat auch ne SQLite Doku
                    # --> http://zetcode.com/python/prettytable/ ### bissle nach unten scrollen
                    data = self.game.a_area.score_board_data(self.score_switch("score.txt"))
                    NameList = data[0]
                    TimeList = data[1]  #### Highscore relevant <- ordered by
                    DateList = data[2]

                    RowNum = len(NameList)
                    x = PrettyTable()

                    x.field_names = ["Name", "Time needed", "Date"]
                    row = 0
                    for row in range(RowNum):
                        x.add_row([NameList[row], TimeList[row], DateList[row]])
                        row += 1
                    # debugger
                    # print(NameList, TimeList, DateList)

                    # TABLE Properties
                    x.sortby = "Time needed"  # ascending sort
                    x.align["Name"] = "l"

                    # table printer
                    # print(x)
                    self.game.a_area.score_board_print(x, row)

                    if os.path.exists(self.score_switch("scoreboard.txt")) and os.path.getsize(self.score_switch("score.txt")):
                        with open(self.score_switch("scoreboard.txt"), "r+") as f:
                            f.write(str(x))
                        f.close()
                    ####################################################################################################
                    time.sleep(15)  # 15 seconds Scoreboard Displaying
                    self.game.quit()

    def rotate(self):
        self.x_player = self.game.player.pos.x
        self.y_player = self.game.player.pos.y

        # if self.game.camera.camera.topleft[0] > 0:
        #     self.x_player -= self.game.camera.camera.topleft[0]
        # if self.game.camera.camera.topleft[1] > 0:
        #     self.y_player -= self.game.camera.camera.topleft[1]

        run, rise = (self.x_player - self.rect.x, self.y_player - self.rect.y)
        # run, rise = self.x_player, self.y_player
        self.img_rot = math.degrees(math.atan2(-rise, run))
        # print("Run,rise = " + str([int(run),int(rise)]) + "  EnemyPos = " + str([int(self.rect.x), int(self.rect.x)]) + " Winkel = " + str(self.img_rot))
        self.image = pg.transform.rotate(self.game.enemy_img, self.img_rot)

    def debuggerEnemy(self):
        # logicalPos = self.posEnemy
        # print("Enemy :" + str(logicalPos))
        pass

    def CountEnemy(self):
        for xnum in range(self.num):
            if max(max_num) < self.num:
                max_num.append(xnum + 1)
            else:
                break
            xnum += 1

        return max(max_num)

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
    #
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
        # self.walk_through_map()
        self.rect.center = self.pos

        self.image = pg.transform.rotate(self.game.enemy_img, self.img_rot + self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # self.pos += self.vel * self.game.dt
        # self.hit_rect.centerx = self.pos.x
        # self.collide_with_walls('x')
        # self.hit_rect.centery = self.pos.y
        # self.collide_with_walls('y')
        # self.rect.center = self.hit_rect.center

        self.distance_to_player()

    # def movement_collision(self, dir):
    #     if dir == 'x':
    #         E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
    #         if E_hits:
    #             if self.vel.x > 0:
    #                 self.pos.x = E_hits[0].rect.left - self.hit_rect.width / 2.0
    #             if self.vel.x < 0:
    #                 self.pos.x = E_hits[0].rect.right + self.hit_rect.width / 2.0
    #             self.vel.x = 0
    #             self.hit_rect.centerx = self.pos.x
    #
    #     if dir == 'y':
    #         E_hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
    #         if E_hits:
    #             if self.vel.y > 0:
    #                 self.pos.y = E_hits[0].rect.top - self.hit_rect.height / 2.0
    #             if self.vel.y < 0:
    #                 self.pos.y = E_hits[0].rect.bottom + self.hit_rect.height / 2.0
    #             self.vel.y = 0
    #             self.hit_rect.centery = self.pos.y
    #
    # def movement_collision_Handler(self):
    #
    #     if self.movement_collision('x'):
    #         self.hit_rect.centery = self.pos.x
    #         collision = True
    #     elif self.movement_collision('y'):
    #         self.hit_rect.centery = self.pos.y
    #         collision = True
    #     else:
    #         collision = False
    #
    #     return collision
    #
    # def movement(self):
    #     while True:
    #         move = (random.randint(0, 20000) % 7)
    #         return move
    #
    # def make_move(self):
    #     move = self.movement()
    #     return move
    #
    # def walk_through_map(self):
    #     global moveNum
    #     global collision
    #     collision = False
    #     moveNum = 0
    #     # enemy should avoid to hit walls and needs to be able to hunt player
    #     # only possible for actual map atm
    #     init = vec(0, 0)
    #     self.vel = init
    #     EnNum = 1
    #     maxRange = self.num
    #
    #     pg.time.delay(10)
    #
    #     for EnNum in range(maxRange):
    #         EnNum += 1
    #         if not collision:
    #             if moveNum == '':
    #                 pass
    #                 # moveNum = self.make_move()
    #             # elif not self.movement_collision(moveNum):
    #             # moveNum = moveNum
    #             else:
    #                 pass
    #                 # moveNum = self.make_move()
    #
    #             # 0 -> w, 1 -> a, 2 -> s, 3 -> d
    #             # 4 -> w + d, 5 -> w + a, 6 -> s + d, 7 -> s + a
    #             if moveNum == 4:
    #                 self.vel = vec(ENEMY_SPEED, -ENEMY_SPEED) * 0.773
    #                 self.rot = 90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 5:
    #                 self.vel = vec(-ENEMY_SPEED, -ENEMY_SPEED) * 0.773
    #                 self.rot = 90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 6:
    #                 self.vel = vec(ENEMY_SPEED, ENEMY_SPEED) * 0.773
    #                 self.rot = -90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 7:
    #                 self.vel = vec(-ENEMY_SPEED, ENEMY_SPEED) * 0.773
    #                 self.rot = -90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 0:
    #                 self.vel = vec(0, -ENEMY_SPEED)
    #                 self.rot = 90
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 1:
    #                 self.vel = vec(0, ENEMY_SPEED)
    #                 self.rot = 180
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 2:
    #                 self.vel = vec(-ENEMY_SPEED, 0)
    #                 self.rot = 0
    #                 collision = self.movement_collision_Handler()
    #             if moveNum == 3:
    #                 self.vel = vec(ENEMY_SPEED, 0)
    #                 self.rot = -90
    #                 collision = self.movement_collision_Handler()
    #         else:
    #             moveNum = self.make_move()

    def distance_to_player(self):
        # effective distance with ignoring walls
        # real distance need to include walls for shoot and hunt
        distance = (self.game.player.pos // 80) - (self.game.enemy.pos // 80)
        # print(self.game.player.pos, self.game.enemy.pos) # debug
        coord_distance = distance
        # print(coord_distance)

    def shoot(self):
        self.clock_time = self.enemy_clock.tick()
        if abs(self.rect.x - self.game.player.pos.x) < ENEMY_SHOOT_RANGE and abs(
                self.rect.y - self.game.player.pos.y) < ENEMY_SHOOT_RANGE * 0.773:
            self.rotate()
            self.time_since_last += self.clock_time
            if self.time_since_last > ENEMY_SHOOT_SPEED:
                EnemyBullet(self.game, self)
                self.time_since_last = 0
