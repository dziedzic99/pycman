from classes import *
import resources
from levelprocesser import readlevel

player = None


def walltypecheck(level, location):
    r = t = l = b = 0
    if location[0] != 0:
        if level[location[0]-1][location[1]] == resources.constants.leveldef["wall"]:
            l = 1
    if location[0] != 64:
        if level[location[0]+1][location[1]] == resources.constants.leveldef["wall"]:
            r = 1
    if location[1] != 0:
        if level[location[0]][location[1]-1] == resources.constants.leveldef["wall"]:
            t = 1
    if location[1] != 64:
        if level[location[0]][location[1]+1] == resources.constants.leveldef["wall"]:
            b = 1
    return str(r) + str(t) + str(l) + str(b)


def loadlevel(level):
    # level-loading procedure with input of standard 64x64 bitmap level file
    level = readlevel(level)
    global player
    for col in range(0, 64):
        for row in range(0, 64):
            box = level[col][row]
            if box == resources.constants.leveldef["coin"]:
                eatable = Eatable(0, (col, row))
                eatables_list.add(eatable)
            elif box == resources.constants.leveldef["wall"]:
                wall = Wall((col, row), walltypecheck(level, (col, row)))
                walls_list.add(wall)
            elif box == resources.constants.leveldef["player"]:
                player = Player((col, row))
                movables_list.add(player)

pygame.init()
pygame.display.set_caption("P@cM@n by Jan Dziedzic 13MF2")
eatables_list = pygame.sprite.Group()
walls_list = pygame.sprite.Group()
movables_list = pygame.sprite.Group()
screen = pygame.display.set_mode(resources.constants.windowSize)
level = "0.bmp"
loadlevel(level)
level = readlevel(level)


def maingame():
    # game starter
    gameOn = True
    clock = pygame.time.Clock()
    # ----- Main game loop -----
    while gameOn:
        # ----- Handling user input ------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False
                break

        # ----- input handling pt 1 -----
        keys = pygame.key.get_pressed()  # checking pressed keys
        # ----- wall collision check -----
        surroundings = walltypecheck(level, player.location)
        # ----- handling some frames/move -----
        timeSegment = resources.constants.timeSegmentSize
        while timeSegment:
            part = resources.constants.timeSegmentSize - timeSegment

            # ----- input handling pt 2-----
            if keys[pygame.K_LEFT] and surroundings[2] == '0':
                player.move('left', part)
            elif keys[pygame.K_RIGHT] and surroundings[0] == '0':
                player.move('right', part)
            elif keys[pygame.K_UP] and surroundings[1] == '0':
                player.move('up', part)
            elif keys[pygame.K_DOWN] and surroundings[3] == '0':
                player.move('down', part)

            # ----- Updating sprites position -----
            eatables_list.update()
            walls_list.update()
            movables_list.update()
            # ----- Fill screen with background -----
            screen.fill(resources.colors.background)
            # ----- ...and sprites -----
            eatables_list.draw(screen)
            walls_list.draw(screen)
            movables_list.draw(screen)
            # ----- Refresh Screen -----
            pygame.display.flip()

            # ----- FPS handling -----
            timeSegment -= 1
            clock.tick(resources.constants.fps)

        # ----- eating handling -----
        for eatable in eatables_list.sprites():
            if eatable.location == player.location:
                eatable.kill()
                # TODO point counter


maingame()
