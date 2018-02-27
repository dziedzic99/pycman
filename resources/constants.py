eatableSize = [20, 20]
movableSize = [20, 20]
playerSize = [20, 20]
speedFactor = 1
windowSize = [640, 660]
playerTimeSegmentSize = 10
ghostTimeSegmentSize = 12
tileWidth = 20
tileSize = [tileWidth, tileWidth]
fps = 60
fontsize = 15
gamesize = 32
scatterSize = 2
totallevels = 5

leveldef = {
    'nothing': 0,
    'wall': 1,
    'coin': 2,
    'player': 3,
    'red_ghost': 4,
    'green_ghost': 5,
    'blue_ghost': 6,
    'heart': 7,
}

editordef = {
    'nothing': (255, 255, 255),
    'wall': (0, 0, 0),
    'coin': (255, 255, 0),
    'heart': (200, 200, 255),
    'player': (255, 0, 0),
    'red_ghost': (200, 100, 100),
    'green_ghost': (0, 255, 0),
    'blue_ghost': (0, 0, 255)
}

tutorialStringList = ["Welcome to PycMan Jan Dziedzic's CS project.",
                      "If you remember PacMan, you pretty much know",
                      "what to do. If not - try not to die, use arrow",
                      "keys to move, eat coins and hearts to progress.",
                      "Good luck."]


congratsStringList = ["Wee, you completed another easy level.",
                      "Feeling proud, don't be, please. There are more",
                      "ahead. Actually it's only gonna get harder",
                      "and harder, until you eventually fail"]

realCongratsStringList = ["Ok, that was unexpected, you actually managed",
                          "to complete the game, write an email to:",
                          "jandziedzic99@gmail.com and tell me that",
                          "I can't even make a seriously hard game"]

theEndStringList = ["Oh, you run out of lifes? What a shame",
                    "Don't worry though - no one actually",
                    "expected you to perform better.",
                    "Try again or better not, it's a boring",
                    "game. Either way... Cheers",
                    "Jan"]