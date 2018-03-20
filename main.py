from classes import *
import resources
from levelprocesser import readlevel
from time import sleep
player = None
coins_total = 0
coins_eaten = 0
level = None
levelno = 1
lives = 30
pygame.init()
myfont = pygame.font.SysFont("monospace", resources.constants.fontsize)
pygame.display.set_caption("PycMan by Jan Dziedzic (13MF2)")
screen = pygame.display.set_mode(resources.constants.windowSize)

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
    global level, thegraph
    thegraph = [[[] for i in range(resources.constants.gamesize)] for j in range(resources.constants.gamesize)]
    for i in range(resources.constants.gamesize):
        for j in range(resources.constants.gamesize):
            # iterating through all tiles in the grid
            if level[i][j] != resources.constants.leveldef["wall"]:
                # taking advantage of the fact that Movables can move on all tiles that are not initially marked as walls
                location = [i, j]
                # and now, iterating through all possible neighbours of the processed tile (with checking if it isn't by any chance a border tile)
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
    visited = []
    # storing visited nodes
    queue = []
    # storing nodes to visit
    end = find_nearest_not_wall(end)
    # as start is guaranteed not to be wall, both ends are now places a Movable may move to
    neighbours = thegraph[start[0]][start[1]].copy()
    # preventing corrupting thegraph when excluding forbidden tile
    try:
        # try as forbidden tile may be any tile after reset
        # particularly it may not be in neighbors
        neighbours.remove([forbidden[0], forbidden[1]])
        # removing forbidden tile from neighbors
    except Exception:
        pass
    queue.append([end[0], end[1]])
    # start search from the end (target tile)
    visited.append(end)
    # mark end as a visited node
    for point in queue:
        if point not in visited:
            visited.append(point)
            # mark current point as visited
        if point in neighbours:
            return point
            # if solution is find return next tile for the ghost
        for node in thegraph[point[0]][point[1]]:
            if node not in visited and node != [forbidden[0], forbidden[1]]:
                queue.append(node)
                # add all unvisited neighbors of current node to the queue


# ----- ----- -----


def loadlevel(file):
    global level, coins_total, player
    # level-loading procedure with input of standard 32x32 bitmap level file
    level = readlevel(file)
    for col in range(0, resources.constants.gamesize):
        for row in range(0, resources.constants.gamesize):
            box = level[col][row]
            if box != resources.constants.leveldef["wall"]\
                    and box != resources.constants.leveldef['nothing']\
                    and box != resources.constants.leveldef['heart']:
                eatable = Eatable('coin', (col, row))
                eatables_list.add(eatable)
                coins_total += 1
            if box == resources.constants.leveldef["wall"]:
                wall = Wall((col, row), walltypecheck((col, row)))
                walls_list.add(wall)
            elif box == resources.constants.leveldef["heart"]:
                heart = Eatable('heart', (col, row))
                eatables_list.add(heart)
            elif box == resources.constants.leveldef["player"]:
                player = Player((col, row))
                players_list.add(player)
            elif box == resources.constants.leveldef["red_ghost"]:
                redghost = Ghost((col, row), 'red')
                ghosts_list.add(redghost)
            elif box == resources.constants.leveldef["blue_ghost"]:
                redghost = Ghost((col, row), 'blue')
                ghosts_list.add(redghost)
            elif box == resources.constants.leveldef["green_ghost"]:
                redghost = Ghost((col, row), 'green')
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


def show_message(messageboard):
    screen.fill(resources.colors.background)
    for i in range(len(messageboard)):
        label = myfont.render(messageboard[i], 1, (255, 255, 0))
        screen.blit(label, (0, resources.constants.fontsize * i))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == 32:
                waiting = False
        sleep(0.05)


def show_tutorial():
    show_message(resources.constants.tutorialStringList)


def show_congrats():
    screen.fill(resources.colors.background)
    for i in range(len(resources.constants.congratsStringList)):
        label = myfont.render(resources.constants.congratsStringList[i], 1, (255, 255, 0))
        screen.blit(label, (0, resources.constants.fontsize*i))
    pygame.display.flip()
    sleep(5)


def show_real_congrats():
    screen.fill(resources.colors.background)
    for i in range(len(resources.constants.realCongratsStringList)):
        label = myfont.render(resources.constants.realCongratsStringList[i], 1, (255, 255, 0))
        screen.blit(label, (0, resources.constants.fontsize*i))
    pygame.display.flip()
    sleep(5)


def show_permanent_death():
    screen.fill(resources.colors.background)
    for i in range(len(resources.constants.theEndStringList)):
        label = myfont.render(resources.constants.theEndStringList[i], 1, (255, 255, 0))
        screen.blit(label, (0, resources.constants.fontsize*i))
    pygame.display.flip()
    sleep(5)


def reset():
    for ghost in ghosts_list.sprites():
        ghost.reset()
    player.reset()


def playlevel():
    global coins_eaten, coins_total, lives, levelno, screen
    # marking variables as global
    coins_total = coins_eaten = 0
    # resetting coin counters
    prepare_level(resources.paths.levelorder[levelno])
    # level loading
    game_on = True
    # game starter
    clock = pygame.time.Clock()
    # clock init
    eatables_list.update()
    walls_list.update()
    players_list.update()
    ghosts_list.update()
    # updating Sprite Groups
    player_time_segment = resources.constants.playerTimeSegmentSize
    ghost_time_segment = resources.constants.ghostTimeSegmentSize
    # forcing pathfinding to update
    # ----- Main game loop -----
    while game_on:
        # ----- Level - winning handling -----
        if coins_eaten == coins_total:
            levelno += 1
            game_on = False
            # ----- stop the level if all coins are eaten -----
        if player_time_segment == resources.constants.playerTimeSegmentSize:
            # ----- Handling user input pt1 ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_on = False
                    exit(0)
            # ----- checking pressed keys -----
            keys = pygame.key.get_pressed()
            # ----- wall collision check -----
            surroundings = walltypecheck(player.location)

        # ----- ghost movement handling pt 1 -----
        if ghost_time_segment == resources.constants.ghostTimeSegmentSize:
            # if it's time to update paths update them
            for ghost in ghosts_list.sprites():
                if ghost.color == 'red':
                    ghost.nexttile = find_next_move(ghost.location, player.location, ghost.previouslocation)
                elif ghost.color == 'blue':
                    ghost.nexttile = find_next_move(ghost.location,
                                                    [player.location[0] + resources.constants.scatterSize,
                                                     player.location[1] + resources.constants.scatterSize],
                                                    ghost.previouslocation)
                elif ghost.color == 'green':
                    ghost.nexttile = find_next_move(ghost.location,
                                                    [player.location[0] - resources.constants.scatterSize,
                                                     player.location[1] - resources.constants.scatterSize],
                                                    ghost.previouslocation)

        # ----- handling some frames/move -----
        player_part = resources.constants.playerTimeSegmentSize - player_time_segment
        ghost_part = resources.constants.ghostTimeSegmentSize - ghost_time_segment

        # ----- input handling pt 2 / player movement handling -----
        if keys[pygame.K_LEFT] and surroundings[2] == '0':
            player.move('left', player_part)
        elif keys[pygame.K_RIGHT] and surroundings[0] == '0':
            player.move('right', player_part)
        elif keys[pygame.K_UP] and surroundings[1] == '0':
            player.move('up', player_part)
        elif keys[pygame.K_DOWN] and surroundings[3] == '0':
            player.move('down', player_part)

        # ----- player dying handling -----
        for ghost in ghosts_list.sprites():
            if ghost.location == player.location:
                # decrease lives counter
                lives -= 1
                reset()
                # reset the board
                player_time_segment = resources.constants.playerTimeSegmentSize + 1
                ghost_time_segment = resources.constants.ghostTimeSegmentSize + 1
                # force game to update ghost paths after respawning
                show_message(resources.constants.lossOfLifeStringList)
        # ----- ghost movement handling pt 2 -----
        for ghost in ghosts_list.sprites():
            try:
                ghost.move((ghost.nexttile[0] - ghost.location[0], -ghost.nexttile[1] + ghost.location[1]), ghost_part)
            except Exception:
                # if for some unforseen reason it's impossible to move the ghost just leave it there
                pass

        if lives <= 0:
            # if the player is dead for good
            break

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

        # ----- Counter info -----
        label = myfont.render("Coins eaten " + str(coins_eaten) + " / " + str(coins_total) +
                              "     Lives remaining " + str(lives) +
                              "     Level " + str(levelno), 1, (255, 255, 0))
        screen.blit(label, (resources.constants.tileWidth / 2,
                            resources.constants.gamesize * resources.constants.tileWidth))

        # ----- Refresh Screen -----
        pygame.display.flip()

        # ----- FPS handling -----
        player_time_segment -= 1
        ghost_time_segment -= 1
        clock.tick(resources.constants.fps)

        # ----- eating handling -----
        for eatable in eatables_list.sprites():
            if eatable.location == player.location:
                eatable.kill()
                if eatable.type == 'coin':
                    coins_eaten += 1
                    # increasing eaten points counter
                elif eatable.type == 'heart':
                    lives += 1
                    # increasing number of lives

        # ----- initializing new time periods -----
        if not player_time_segment:
            player_time_segment = resources.constants.playerTimeSegmentSize
        if not ghost_time_segment:
            ghost_time_segment = resources.constants.ghostTimeSegmentSize


def main():
    show_message(resources.constants.tutorialStringList)
    while lives > 0 and levelno <= resources.constants.totallevels:
        print(levelno)
        playlevel()
        show_message(resources.constants.congratsStringList)
    if lives > 0:
        show_message(resources.constants.realCongratsStringList)
    else:
        show_message(resources.constants.theEndStringList)

main()
#show_message(resources.constants.realCongratsStringList)
