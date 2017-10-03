from classes import *
import resources
from levelprocesser import readlevel
from datetime import datetime
player = None
coins_total = 0
coins_eaten = 0
level = None
level_number = 0

# ----- This 2D array holds info on location lists accessible (common edge) from tile represented by address -----
thegraph = [[[] for i in range(resources.constants.gamesize)] for j in range(resources.constants.gamesize)]


def walltypecheck(location):
    r = t = l = b = 0
    if location[0] != 0:
        if level[location[0]-1][location[1]] == resources.constants.leveldef["wall"]:
            l = 1
    if location[0] != resources.constants.gamesize-1:
        if level[location[0]+1][location[1]] == resources.constants.leveldef["wall"]:
            r = 1
    if location[1] != 0:
        if level[location[0]][location[1]-1] == resources.constants.leveldef["wall"]:
            t = 1
    if location[1] != resources.constants.gamesize-1:
        if level[location[0]][location[1]+1] == resources.constants.leveldef["wall"]:
            b = 1
    return str(r) + str(t) + str(l) + str(b)


# ----- Graphing stuff (for pathfinding) -----


def graphbuilder():
    global level
    for i in range(resources.constants.gamesize):
        for j in range(resources.constants.gamesize):
            if level[i][j] != resources.constants.leveldef["wall"]:
                location = [i, j]
                if location[0] != 0:
                    if level[location[0] - 1][location[1]] != resources.constants.leveldef["wall"]:
                        thegraph[location[0]][location[1]] += [[location[0] - 1, location[1]]]
                if location[0] != resources.constants.gamesize-1:
                    if level[location[0] + 1][location[1]] != resources.constants.leveldef["wall"]:
                        thegraph[location[0]][location[1]] += [[location[0] + 1, location[1]]]
                if location[1] != 0:
                    if level[location[0]][location[1] - 1] != resources.constants.leveldef["wall"]:
                        thegraph[location[0]][location[1]] += [[location[0], location[1] - 1]]
                if location[1] != resources.constants.gamesize-1:
                    if level[location[0]][location[1] + 1] != resources.constants.leveldef["wall"]:
                        thegraph[location[0]][location[1]] += [[location[0], location[1] + 1]]


def find_nearest_not_wall(point):
    if point[0] > resources.constants.gamesize-1:
        point[0] = resources.constants.gamesize-1
    if point[0] < 0:
        point[0] = 0
    if point[1] > resources.constants.gamesize-1:
        point[1] = resources.constants.gamesize-1
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


def find_next_move(start, end, forbidden):
    beginning = datetime.now()
    visited = []
    queue = []
    end = find_nearest_not_wall(end)
    # as start is guaranteed not to be wall, both ends are now places a Movable may move to
    neighbours = thegraph[start[0]][start[1]]
    print(forbidden)
    print(neighbours)
    try:
        if len(neighbours) > 1:
            neighbours.remove([forbidden[0], forbidden[1]])
    except Exception:
        pass
    queue.append([end[0], end[1]])
    visited.append(end)
    for point in queue:
        if point in neighbours:
            print(datetime.now()-beginning)
            return point
        for node in thegraph[point[0]][point[1]]:
            if node not in visited:
                visited.append(node)
                queue.append(node)


# ----- ----- -----


def loadlevel(file):
    global level, coins_total, player
    # level-loading procedure with input of standard 64x64 bitmap level file
    level = readlevel(file)
    for col in range(0, resources.constants.gamesize):
        for row in range(0, resources.constants.gamesize):
            box = level[col][row]
            if box == resources.constants.leveldef["coin"]:
                eatable = Eatable(0, (col, row))
                eatables_list.add(eatable)
                coins_total += 1
            elif box == resources.constants.leveldef["wall"]:
                wall = Wall((col, row), walltypecheck((col, row)))
                walls_list.add(wall)
            elif box == resources.constants.leveldef["player"]:
                print("player init")
                player = Player((col, row))
                players_list.add(player)
            elif box == resources.constants.leveldef["red_ghost"]:
                redghost = Ghost((col, row), 'red')
                ghosts_list.add(redghost)

eatables_list = pygame.sprite.Group()
walls_list = pygame.sprite.Group()
players_list = pygame.sprite.Group()
ghosts_list = pygame.sprite.Group()


def prepare_level(levelfile):
    global eatables_list, walls_list, players_list, ghosts_list, player
    eatables_list = pygame.sprite.Group()
    walls_list = pygame.sprite.Group()
    players_list = pygame.sprite.Group()
    ghosts_list = pygame.sprite.Group()
    loadlevel(levelfile)
    graphbuilder()
    # print(thegraph[3][21])


def maingame():
    global coins_eaten, coins_total
    prepare_level("level1.bmp")
    pygame.init()
    pygame.display.set_caption("PycMan by Jan Dziedzic (13MF2)")

    screen = pygame.display.set_mode(resources.constants.windowSize)
    # game starter
    gameOn = True
    clock = pygame.time.Clock()

    eatables_list.update()
    walls_list.update()
    players_list.update()
    ghosts_list.update()
    # ----- Main game loop -----
    while gameOn:
        # ----- Level - finish handling -----
        if coins_eaten == coins_total:
            # TODO: do stuff
            print("lol, you got it")


        # ----- Handling user input ------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False
                break

        # ----- input handling pt 1 -----
        keys = pygame.key.get_pressed()  # checking pressed keys
        # ----- ghost movement handling pt 1 -----
        for ghost in ghosts_list.sprites():
            ghost.nexttile = find_next_move(ghost.location, player.location, ghost.previouslocation)
        # ----- wall collision check -----
        surroundings = walltypecheck(player.location)
        # ----- handling some frames/move -----
        timeSegment = resources.constants.timeSegmentSize

        while timeSegment:
            part = resources.constants.timeSegmentSize - timeSegment

            # ----- input handling pt 2 -----
            if keys[pygame.K_LEFT] and surroundings[2] == '0':
                player.move('left', part)
            elif keys[pygame.K_RIGHT] and surroundings[0] == '0':
                player.move('right', part)
            elif keys[pygame.K_UP] and surroundings[1] == '0':
                player.move('up', part)
            elif keys[pygame.K_DOWN] and surroundings[3] == '0':
                player.move('down', part)

            # ----- ghost movement handling pt 2 -----
            for ghost in ghosts_list.sprites():
                ghost.move((ghost.nexttile[0] - ghost.location[0], -ghost.nexttile[1] + ghost.location[1]), part)

            # ----- Updating sprites position -----
            eatables_list.update()
            walls_list.update()
            players_list.update()
            ghosts_list.update()
            # ----- Fill screen with background -----
            screen.fill(resources.colors.background)
            # ----- ...and sprites -----
            eatables_list.draw(screen)
            walls_list.draw(screen)
            players_list.draw(screen)
            ghosts_list.draw(screen)
            # ----- Refresh Screen -----
            pygame.display.flip()

            # ----- FPS handling -----
            timeSegment -= 1
            clock.tick(resources.constants.fps)

        # ----- eating handling -----
        for eatable in eatables_list.sprites():
            if eatable.location == player.location:
                eatable.kill()
                coins_eaten += 1


maingame()
