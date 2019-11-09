import unittest
import pygame

import images
import playfield
from playfield import Tile
from playfield import TileType

import entities.manager
from powerupspawner import PowerupSpawner
from entities.powerup import *

class TestPowerupSpawner(unittest.TestCase):
    def setUp(self):
        images.set('brick', None)
        images.set('concrete', None)
        images.set('water', None)
        images.set('tree', None)
        images.set('powerup', pygame.Surface((1, 1)))
        entities.manager.clear()
        playfield.initialize(10, 10)

    def test_createRandomPowerup(self):
        powerup = PowerupSpawner().createRandomPowerup()
        self.assertTrue(isinstance(powerup, Powerup))

    def test_getRandomPowerupLocation(self):
        setupPlayfield(['B-'])
        location = PowerupSpawner().getRandomPowerupLocation()
        self.assertEqual((1,0), location)

    def test_getRandomPowerupLocation_noRoom(self):
        setupPlayfield(['B'])
        location = PowerupSpawner().getRandomPowerupLocation()
        self.assertIsNone(location)

    def test_createRandomPowerupAtRandomLocation(self):
        setupPlayfield(['B-'])
        createdPowerup = PowerupSpawner().createRandomPowerupAtRandomLocation()

        self.assertIsNotNone(createdPowerup)
    
    def test_spawn_powerupIsAddedToManager(self):
        setupPlayfield(['-'])
        powerup = PowerupSpawner().spawn()

        self.assertTrue(entities.manager.contains(powerup))

def setupPlayfield(data):
    height = len(data)
    width = len(data[0])
    playfield.initialize(width, height)

    for x in range(width):
        for y in range(height):
            tile = createTileFromCharacter(data[y][x])
            playfield.setTile(x, y, tile)

def createTileFromCharacter(chr):
    if chr == ' ':
        return '-'
    elif chr == 'B':
        return Tile(TileType.BRICK)
    elif chr == 'C':
        return Tile(TileType.CONCRETE)
    elif chr == 'W':
        return Tile(TileType.WATER)
    elif chr == 'T':
        return Tile(TileType.TREE)