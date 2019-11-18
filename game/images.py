import os
import pygame
import pygame.transform

images = {}

def load(fileName):
    loadedImage = loadImageFile(fileName)
    key = getKeyFromFilename(fileName)
    images[key] = loadedImage

def get(key):
    return images[key]

def set (key, image):
    images[key] = image

def loadImageFile(fileName):
    return pygame.image.load(os.path.join('images', fileName)).convert_alpha()

def generateRotatedImages(fileName):
    baseKey = getKeyFromFilename(fileName)
    northImage = loadImageFile(fileName)
    eastImage = pygame.transform.rotate(northImage, 270)
    southImage = pygame.transform.rotate(northImage, 180)
    westImage = pygame.transform.rotate(northImage, 90)

    images[baseKey + '_north'] = northImage
    images[baseKey + '_east'] = eastImage
    images[baseKey + '_south'] = southImage
    images[baseKey + '_west'] = westImage

def getKeyFromFilename(fileName):
    return os.path.splitext(fileName)[0]