from PIL import Image
import resources


def readlevel(file):
    # level-loading procedure with input of standard 64x64 bitmap level file
    level = [[resources.constants.leveldef['nothing'] for i in range(64)] for j in range(64)]
    im = Image.open(resources.paths.levels + file)
    im.load()
    for col in range(0, 64):
        for row in range(0, 64):
            pixel = im.getpixel((col, row))
            if pixel == resources.constants.editordef["coin"]:
                level[col][row] = resources.constants.leveldef['coin']
            elif pixel == resources.constants.editordef["wall"]:
                level[col][row] = resources.constants.leveldef['wall']
            elif pixel == resources.constants.editordef["player"]:
                level[col][row] = resources.constants.leveldef['player']
    return level
