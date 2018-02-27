from PIL import Image
import resources


def readlevel(file):
    # level-loading procedure with input of gamesize^2 bitmap level file
    level = [[resources.constants.leveldef['nothing'] for i in range(resources.constants.gamesize)] for j in range(resources.constants.gamesize)]
    im = Image.open(resources.paths.levels + file)
    im.load()
    for col in range(0, resources.constants.gamesize):
        for row in range(0, resources.constants.gamesize):
            pixel = im.getpixel((col, row))
            if pixel == resources.constants.editordef["coin"]:
                level[col][row] = resources.constants.leveldef['coin']
            elif pixel == resources.constants.editordef["heart"]:
                level[col][row] = resources.constants.leveldef['heart']
            elif pixel == resources.constants.editordef["wall"]:
                level[col][row] = resources.constants.leveldef['wall']
            elif pixel == resources.constants.editordef["player"]:
                level[col][row] = resources.constants.leveldef['player']
            elif pixel == resources.constants.editordef["red_ghost"]:
                level[col][row] = resources.constants.leveldef['red_ghost']
            elif pixel == resources.constants.editordef["green_ghost"]:
                level[col][row] = resources.constants.leveldef['green_ghost']
            elif pixel == resources.constants.editordef["blue_ghost"]:
                level[col][row] = resources.constants.leveldef['blue_ghost']
    return level
