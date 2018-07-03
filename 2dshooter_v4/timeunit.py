import pygame
class TimeManager():
    def __init__(self,timetowait):
        self.last = pygame.time.get_ticks()
        self.cooldown = timetowait  #milliseconds

    def time_over(self):
        # fire gun, only if cooldown has been 0.3 seconds since last
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            return True
        else:
            return False