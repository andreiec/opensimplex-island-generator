from opensimplex import OpenSimplex
import numpy as np
from PIL import Image

# Variables
# SEED = 209
WIDTH = 256
HEIGHT = 256
BIAS = 10
SCALE = max(WIDTH, HEIGHT) / 4
OCTAVES = 11
PERSISTANCE = 0.5
LACUNARITY = 2

# Colors
COLOR_DEEPWATER = (0, 62, 178)
COLOR_WATER = (9, 82, 198)
COLOR_SAND = (254, 224, 179)
COLOR_GRASS = (9, 120, 93)
COLOR_DARKGRASS = (10, 107, 72)
COLOR_DARKESTGRASS = (11, 94, 51)
COLOR_DARKROCKS = (140, 142, 123)
COLOR_ROCKS = (160, 162, 143)
COLOR_SNOW = (255, 255, 255)


# Return corresponding color from 0 - 255
def getColor(val):
    if val < 0:
        val = 0
    if val > 255:
        val = 255

    if val <= 84:
        return COLOR_DEEPWATER
    elif val <= 102:
        return COLOR_WATER
    elif val <= 112:
        return COLOR_SAND
    elif val <= 134:
        return COLOR_GRASS
    elif val <= 164:
        return COLOR_DARKGRASS
    elif val <= 200:
        return COLOR_DARKESTGRASS
    elif val <= 224:
        return COLOR_DARKROCKS
    elif val <= 242:
        return COLOR_ROCKS
    elif val <= 255:
        return COLOR_SNOW
    return COLOR_DEEPWATER


# A seed is considered to be 'good' if it gas a mountain in the center
def findGoodSeed(startingSeed, numberOfSeeds):
    s = startingSeed
    seedArray = []
    nr = 0

    while nr < numberOfSeeds:
        n = OpenSimplex(seed=s)
        nH = 0
        a = 1
        f = 1

        for o in range(0, OCTAVES):
            sX = (WIDTH / 2) / SCALE * f
            sY = (HEIGHT / 2) / SCALE * f

            v = n.noise2d(sX, sY)
            nH += v * a

            a *= PERSISTANCE
            f *= LACUNARITY

        if int((nH + 1) * 128) > 245:
            seedArray.append(s)
            nr += 1
        s += 1

    return seedArray


# NoiseMap Generation
def generateMap(height, width, seed, scale, octaves, bias, persistance, lacunarity, name):
    heightMap = np.empty((height, width), dtype=np.short)
    noise = OpenSimplex(seed=seed)

    print("Started generating map '" + name + "' (" + str(height) + "x" + str(width) + ") with seed: " + str(seed))
    for y in range(0, height):
        for x in range(0, width):
            amplitude = 1
            frequency = 1
            noiseHeight = 0

            # Calculating values for each octave
            for octave in range(0, octaves):
                sampleX = x / scale * frequency
                sampleY = y / scale * frequency

                value = noise.noise2d(sampleX, sampleY)
                noiseHeight += value * amplitude

                amplitude *= persistance
                frequency *= lacunarity
                heightMap[y][x] = (noiseHeight + 1) * 128

            # Circular square mask
            distX = abs(width / 2 - x)
            distY = abs(height / 2 - y)
            dist = max(distX, distY)

            # Applying mask
            maxWidth = width / 2 - bias
            delta = dist / maxWidth
            gradient = delta ** 2
            heightMap[y][x] *= max(0.0, 1.0 - gradient)

        # print("Now at y: " + str(y))

    print("Creating image..")
    colourMap = np.zeros((height, width, 3), dtype=np.uint8)

    # Assigning colors for each value
    for y in range(0, height):
        for x in range(0, width):
            colourMap[x][y] = getColor(heightMap[x][y])

    image = Image.fromarray(colourMap, 'RGB')
    image.save(name + '.png')
    return image


if __name__ == "__main__":
    generateMap(HEIGHT, WIDTH, 6913374206969, SCALE, OCTAVES, BIAS, PERSISTANCE, LACUNARITY, "MapSeed11" + str(6913374206969))
