import pygame as pg
from random import randint as rand
from settings import *

class Food:
    def __init__(self, color=(0, 255, 0)):

        self.food = pg.sprite.Sprite()
        self.food.image = pg.Surface([WF, HF])
        self.food.rect = self.food.image.get_rect()
        self.food.rect.x = rand(0, SCR_W - WCR)
        self.food.rect.y = rand(0, SCR_H - HCR)

        self.food.image.fill(color)

    def type(self):
        return "Food"
