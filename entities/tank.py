import entities
import entities.projectile
import images
import vector

class Tank(entities.Entity, entities.ProjectileCollider):
    aimVector = vector.Vector(0, -1)

    def __init__(self):
        self.image = images.get('tank')
        self.setSize(vector.Vector(self.image.get_width(), self.image.get_height()))

    def update(self, time, timePassed):
        pass

    def render(self, screen, offset):
        screen.blit(self.image, (offset[0] + self.location.x, offset[1] + self.location.y))

    def moveLeft(self):
        self.setLocation(vector.Vector(self.location.x - 3, self.location.y))

    def moveRight(self):
        self.setLocation(vector.Vector(self.location.x + 3, self.location.y))

    def moveUp(self):
        self.setLocation(vector.Vector(self.location.x, self.location.y - 3))

    def moveDown(self):
        self.setLocation(vector.Vector(self.location.x, self.location.y + 3))

    def fire(self):
        projectile = entities.projectile.Projectile(self.location, self.aimVector.toUnit())
        entities.manager.add(projectile)
