import math
import random

import pygame
from Box2D import b2EdgeShape, Box2D
from pygame import Vector2

from utils import utils


class Ring:
    def __init__(self, pos, radius, rotateDir):
        self.color = (255,255,255)
        self.radius = radius
        self.rotateDir = rotateDir
        
        self.size = 360
        
        self.holeSize = random.randint(9, 12) 
        self.holePosition = random.randint(0, self.size-1) 
        
        self.vertices = []
        for i in range(self.size):
            angle = i * (2 * math.pi / self.size)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.vertices.append((x, y))

        self.body = utils.world.CreateStaticBody(position=utils.from_Pos(pos))
        self.body.userData = self

        self.create_edge_shape()
        self.hue = random.uniform(0,1)


    def create_edge_shape(self):
        for i in range(self.size):
            holeStart = (self.holePosition - self.holeSize) % self.size
            holeEnd = (self.holePosition + self.holeSize) % self.size
            
            skipEdge = False
            if holeStart < holeEnd:
                if holeStart <= i <= holeEnd:
                    skipEdge = True
                if i >= holeStart or i <= holeEnd:
                    skipEdge = True
            
            if not skipEdge:
                v1 = self.vertices[i]
                v2 = self.vertices[(i + 1) % self.size]
                edge = b2EdgeShape(vertices=[v1, v2])
                self.body.CreateEdgeFixture(shape=edge, density=1, friction=0.0, restitution=1.0)


    def draw(self):
        self.hue = (self.hue + utils.deltaTime()/10) % 1
        self.color = utils.hueToRGB(self.hue)

        self.body.angle += self.rotateDir * utils.deltaTime()
        self.draw_edges()

    def draw_edges(self):
        for fixture in self.body.fixtures:
            v1 = utils.to_Pos(self.body.transform * fixture.shape.vertices[0])
            v2 = utils.to_Pos(self.body.transform * fixture.shape.vertices[1])
            pygame.draw.line(utils.screen, self.color, v1, v2, 4)

