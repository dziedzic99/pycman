import pygame
import resources


class GameObject(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = None
        self.location = location
        self.rect = None

    def setimage(self, image, size=resources.constants.boxSize, rotation=0):
        self.image = pygame.image.load(resources.paths.image[image])
        self.image = pygame.transform.scale(self.image, size)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.location[0] * 10, self.location[1] * 10


class Eatable(GameObject):
    def __init__(self, type, location):
        super().__init__(location)
        self.type = type
        self.setimage("coin", resources.constants.eatableSize)


class Wall(GameObject):
    def __init__(self, location, type):
        super().__init__(location)
        self.setimage('w'+str(type))


class Movable(GameObject):
    def __init__(self, location):
        super().__init__(location)
        self.image = None
        self.speed = (0, 0)

    def setimage(self, image, size=resources.constants.movableSize, rotation=0):
        super().setimage(image, size, rotation)

    def move(self, direction, part=resources.constants.timeSegmentSize-1):
        if direction == 'up':
            self.speed = (0, -1)
        elif direction == 'down':
            self.speed = (0, 1)
        elif direction == 'left':
            self.speed = (-1, 0)
        elif direction == 'right':
            self.speed = (1, 0)
        part2 = (part+1) / resources.constants.timeSegmentSize
        self.rect.x, self.rect.y = (self.location[0] + self.speed[0] * resources.constants.speedFactor * part2) * 10,\
                                   (self.location[1] + self.speed[1] * resources.constants.speedFactor * part2) * 10
        if part == resources.constants.timeSegmentSize - 1:
            self.location = self.location[0] + self.speed[0] * resources.constants.speedFactor,\
                            self.location[1] + self.speed[1] * resources.constants.speedFactor


class Player(Movable):
    def __init__(self, location):
        super().__init__(location)
        self.setimage('player', resources.constants.playerSize)

    def move(self, direction, part=resources.constants.timeSegmentSize-1):
        rotation = 0
        if self.speed == (1, 0):
            rotation = 0
        elif self.speed == (-1, 0):
            rotation = 180
        elif self.speed == (0, -1):
            rotation = 90
        elif self.speed == (0, 1):
            rotation = 270
        super().setimage('player', resources.constants.playerSize, rotation)
        super().move(direction, part)


class Ghost(Movable):
    def __init__(self, location):
        super().__init__(location)

