from classes import *
import resources
from levelprocesser import readlevel

player = None

# ----- This 2D array holds info on location lists accessible (common edge) from tile represented by address -----
thegraph = [[[] for i in range(64)] for j in range(64)]


def walltypecheck(location):
    r = t = l = b = 0
    if location[0] != 0:
        if level[location[0]-1][location[1]] == resources.constants.leveldef["wall"]:
            l = 1
    if location[0] != 63:
        if level[location[0]+1][location[1]] == resources.constants.leveldef["wall"]:
            r = 1
    if location[1] != 0:
        if level[location[0]][location[1]-1] == resources.constants.leveldef["wall"]:
            t = 1
    if location[1] != 63:
        if level[location[0]][location[1]+1] == resources.constants.leveldef["wall"]:
            b = 1
    return str(r) + str(t) + str(l) + str(b)

# ----- Graphing stuff (for pathfinding) -----
def graphbuilder():
    global level
    for i in range(64):
        for j in range(64):
            if level[j][i] != resources.constants.leveldef["wall"]:
                location = [i,j]
                if location[0] != 0:
                    if level[location[0] - 1][location[1]] != resources.constants.leveldef["wall"]:
                        thegraph[location[0]][location[1]] += [[location[0] - 1, location[1]]]
                if location[0] != 63:
                    if level[location[0] + 1][location[1]] != resources.constants.leveldef["wall"]:
                        thegraph[location[0]][location[1]] += [[location[0] + 1, location[1]]]
                if location[1] != 0:
                    if level[location[0]][location[1] - 1] != resources.constants.leveldef["wall"]:
                        thegraph[location[0]][location[1]] += [[location[0], location[1] - 1]]
                if location[1] != 63:
                    if level[location[0]][location[1] + 1] != resources.constants.leveldef["wall"]:
                        thegraph[location[0]][location[1]] += [[location[0], location[1] + 1]]


def find_nearest_not_wall(point):
    if point[0] > 63:
        point[0] = 63
    if point[0] < 0:
        point[0] = 0
    if point[1] > 63:
        point[1] = 63
    if point[1] < 0:
        point[1] = 0
    radius = 1
    if level[point[0]][point[1]] != resources.constants.leveldef['wall']:
        return point
    while True:
        for i in range(point[0]-radius, point[0]+radius):
            for j in range(point[1]-radius, point[1]+radius):
                try:
                    if level[i][j] != resources.constants.leveldef['wall']:
                        return [i, j]
                except IndexError:
                    pass
        radius += 1


def find_next_move(start, end):
    visited = []
    queue = []
    end = find_nearest_not_wall(end)
    # as start is guaranteed not to be wall, both ends are now places a Movable may move to
    neighbours = thegraph[start[0]][start[1]]
    queue.append(end)
    visited.append(end)
    for point in queue:
        if point in neighbours:
            return point
        for node in thegraph[point[0]][point[1]]:
            if node not in visited:
                visited.append(node)
                queue.append(node)

# ----- ----- -----


def loadlevel(file):
    global level
    # level-loading procedure with input of standard 64x64 bitmap level file
    level = readlevel(file)
    global player
    for col in range(0, 64):
        for row in range(0, 64):
            box = level[col][row]
            if box == resources.constants.leveldef["coin"]:
                eatable = Eatable(0, (col, row))
                eatables_list.add(eatable)
            elif box == resources.constants.leveldef["wall"]:
                wall = Wall((col, row), walltypecheck((col, row)))
                walls_list.add(wall)
            elif box == resources.constants.leveldef["player"]:
                player = Player((col, row))
                movables_list.add(player)

eatables_list = pygame.sprite.Group()
walls_list = pygame.sprite.Group()
movables_list = pygame.sprite.Group()

file = "0.bmp"
level = None
loadlevel(file)
graphbuilder()


def maingame():
    pygame.init()
    pygame.display.set_caption("PycMan by Jan Dziedzic (13MF2)")

    screen = pygame.display.set_mode(resources.constants.windowSize)
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
        surroundings = walltypecheck(player.location)
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


# maingame()
