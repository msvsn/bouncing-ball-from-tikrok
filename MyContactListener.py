

import Box2D
from Box2D import b2ContactListener


class MyContactListener(b2ContactListener):
    def __init__(self):
        super(MyContactListener, self).__init__()
        self.collisions = []

    def BeginContact(self, contact):
        fixtureA = contact.fixtureA
        fixtureB = contact.fixtureB
        bodyA = fixtureA.body
        bodyB = fixtureB.body

        from Ring import Ring
        from Ball import Ball
        if (isinstance(bodyA.userData,Ring) and isinstance(bodyB.userData,Ball))\
                or (isinstance(bodyA.userData,Ball) and isinstance(bodyB.userData,Ring)):
            self.collisions.append((bodyA, bodyB))


