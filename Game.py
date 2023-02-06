import pygame as p
import time
import MiniMax
from copy import deepcopy

p.init()


class Square(p.sprite.Sprite):
    def __int__(self, x_id, y_id, number):
        super().__init__()
        self.width = 120
        self.height = 120
        self.x = x_id * self.width
        self.y = y_id * self.height
        self.content = ''
        self.number = number
        self.image = blank_image
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

WIDTH = 500
HEIGHT = 500

win = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('four connect')
clock = p.time.Clock()

blank_image = p.image.load('Images\Blank.png')
x_image = p.image.load('Images\x.png')
o_image = p.image.load('Images\o.png')
background = p.image.load('Images\Background.png')
background = p.transform.scale(background, (WIDTH, HEIGHT))

move = True
won = False
compMove = 5

square_group = p.sprite.Group()
squares = []
