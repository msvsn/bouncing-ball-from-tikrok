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
        
        # Створення більшої кількості кіл
        self.rings = []
        
        # Параметри для розміщення кіл
        num_rings = random.randint(5, 8)
        min_radius = 12
        max_radius = 25
        
        # Створюємо кільця з різними радіусами, що розташовані концентрично
        for i in range(num_rings):
            # Розраховуємо радіус для кільця, щоб вони були близько одне до одного
            radius = min_radius + i * ((max_radius - min_radius) / (num_rings - 1))
            
            # Випадкове обертання (від -2 до 2, крім 0)
            rotate_dir = random.choice([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2])
            
            # Додаємо нове кільце
            self.rings.append(
                Ring(Vector2(utils.width / 2, utils.height / 2), radius, rotate_dir)
            )
        
        # Зберігаємо інформацію про те, в яких колах знаходиться м'яч
        self.ball_inside_rings = [True] * len(self.rings)

    def update(self):
        utils.world.Step(1.0 / 60.0, 6, 2)
        
        # Перевіряємо, чи вийшов м'яч за межі якогось кола
        ball_pos = self.ball.getPos()
        center = Vector2(utils.width/2, utils.height/2)
        
        rings_to_remove = []
        
        for i, ring in enumerate(self.rings):
            # Відстань від м'яча до центру
            distance = (ball_pos - center).length()
            
            # Перевіряємо, чи м'яч був всередині кола
            if self.ball_inside_rings[i]:
                # Якщо м'яч вийшов за межі кола
                if distance > ring.radius * utils.PPM:
                    # Позначаємо коло для видалення
                    rings_to_remove.append(i)
                    # Відтворюємо звук
                    sounds.play()
        
        # Видаляємо кола, через які м'яч пройшов (у зворотному порядку)
        for i in sorted(rings_to_remove, reverse=True):
            # Видаляємо тіло з фізичного світу
            utils.world.DestroyBody(self.rings[i].body)
            # Видаляємо кільце зі списку
            del self.rings[i]
            del self.ball_inside_rings[i]
        
        # Обробляємо зіткнення
        if utils.contactListener:
            # Якщо відбулися зіткнення
            if utils.contactListener.collisions:
                # Збільшуємо м'яч на 0.01 одиницю
                for bodyA, bodyB in utils.contactListener.collisions:
                    from Ball import Ball
                    # Знаходимо м'яч серед тіл, що зіткнулися
                    ball_body = None
                    if isinstance(bodyA.userData, Ball):
                        ball_body = bodyA
                    elif isinstance(bodyB.userData, Ball):
                        ball_body = bodyB
                    
                    if ball_body:
                        # Збільшуємо радіус м'яча
                        old_radius = ball_body.fixtures[0].shape.radius
                        new_radius = old_radius + 0.01
                        
                        # Видаляємо старий fixture та створюємо новий з новим радіусом
                        ball_body.DestroyFixture(ball_body.fixtures[0])
                        ball_body.CreateCircleFixture(radius=new_radius, density=1, friction=0.0, restitution=1.0)
                        
                        # Відтворюємо звук
                        sounds.play()
                    break
                
                # Очищаємо список зіткнень
                utils.contactListener.collisions = []
        
        # Оновлюємо інформацію про те, в яких колах знаходиться м'яч
        for i, ring in enumerate(self.rings):
            if i < len(self.ball_inside_rings):
                distance = (ball_pos - center).length()
                self.ball_inside_rings[i] = distance < ring.radius * utils.PPM

    def draw(self):
        for ring in self.rings:
            ring.draw()
        self.ball.draw()