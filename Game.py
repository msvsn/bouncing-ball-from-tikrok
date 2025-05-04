from pygame import Vector2

from Ball import Ball
from Ring import Ring
from Sounds import sounds
from utils import utils
import random
import math


class Game:
    def __init__(self):
        self.ball = Ball(Vector2(utils.width/2,utils.height/2),1,(255,255,255))
        
        self.rings = []
        
        num_rings = random.randint(5, 8)
        min_radius = 12
        max_radius = 25
        
        for i in range(num_rings):
            radius = min_radius + i * ((max_radius - min_radius) / (num_rings - 1))
            
            rotate_dir = random.choice([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2])
            
            self.rings.append(
                Ring(Vector2(utils.width / 2, utils.height / 2), radius, rotate_dir)
            )
        
        self.ball_inside_rings = [True] * len(self.rings)

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        
        ball_pos = self.ball.getPos()
        center = Vector2(utils.width/2, utils.height/2)
        
        rings_to_remove = []
        
        for i, ring in enumerate(self.rings):
            distance = (ball_pos - center).length()
            
            if self.ball_inside_rings[i]:
                if distance > ring.radius * utils.PPM:
                    rings_to_remove.append(i)
                    sounds.play()
        
        for i in sorted(rings_to_remove, reverse=True):
            utils.world.DestroyBody(self.rings[i].body)
            del self.rings[i]
            del self.ball_inside_rings[i]
        
        if utils.contactListener:
            if utils.contactListener.collisions:
                for bodyA, bodyB in utils.contactListener.collisions:
                    from Ball import Ball
                    ball_body = None
                    if isinstance(bodyA.userData, Ball):
                        ball_body = bodyA
                    elif isinstance(bodyB.userData, Ball):
                        ball_body = bodyB
                    
                    if ball_body:
                        old_radius = ball_body.fixtures[0].shape.radius
                        new_radius = old_radius + 0.01
                        
                        ball_body.DestroyFixture(ball_body.fixtures[0])
                        ball_body.CreateCircleFixture(radius=new_radius, density=1, friction=0.0, restitution=1.0)
                        
                        sounds.play()
                    break
                
                utils.contactListener.collisions = []
        
        for i, ring in enumerate(self.rings):
            if i < len(self.ball_inside_rings):
                distance = (ball_pos - center).length()
                self.ball_inside_rings[i] = distance < ring.radius * utils.PPM

    def draw(self):
        for ring in self.rings:
            ring.draw()
        self.ball.draw()