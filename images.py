import os
import pygame

images = {}

def load(fileName, key):
    loadedImage = pygame.image.load(os.path.join('images', fileName))
    images[key] = loadedImage

def get(key):
    return images[key]