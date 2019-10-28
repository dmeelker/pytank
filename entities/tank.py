import entities
import entities.projectile
import images
import vector

class Tank(entities.Entity, entities.ProjectileCollider):
    aimVector = vector.Vector(0, -1)
    hitpoints = 10
    movementSpeed = 3

    def __init__(self, location, aimVector = vector.Vector(1, 0)):
        self.image = images.get('tank')
        self.setSize(vector.Vector(self.image.get_width(), self.image.get_height()))
        self.setLocation(location)
        self.aimVector = aimVector

    def update(self, time, timePassed):
        pass

    def render(self, screen, offset):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def moveLeft(self):
        self.setLocation(vector.Vector(self.location.x - self.movementSpeed, self.location.y))
        self.aimVector = vector.Vector(-1, 0)

    def moveRight(self):
        self.setLocation(vector.Vector(self.location.x + self.movementSpeed, self.location.y))
        self.aimVector = vector.Vector(1, 0)

    def moveUp(self):
        self.setLocation(vector.Vector(self.location.x, self.location.y - self.movementSpeed))
        self.aimVector = vector.Vector(0, -1)

    def moveDown(self):
        self.setLocation(vector.Vector(self.location.x, self.location.y + self.movementSpeed))
        self.aimVector = vector.Vector(0, 1)

    def fire(self):
        projectile = entities.projectile.Projectile(self.location, self.aimVector.toUnit(), self)
        entities.manager.add(projectile)

    def hitByProjectile(self, projectile):
        self.hitpoints -= projectile.power