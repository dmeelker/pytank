import pygame
import pygame.joystick

tankController = None
joystick = None

def initialize():
    global joystick
    print(f'Detected {pygame.joystick.get_count()} joysticks')
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        print(f'Initializing joystick {joystick.get_name()}')
        joystick.init()

def handleEvent(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            tankController.moveLeft = True
        if event.key == pygame.K_RIGHT:
            tankController.moveRight = True
        if event.key == pygame.K_UP:
            tankController.moveUp = True
        if event.key == pygame.K_DOWN:
            tankController.moveDown = True
        if event.key == pygame.K_SPACE:
            tankController.fire = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            tankController.moveLeft = False
        if event.key == pygame.K_RIGHT:
            tankController.moveRight = False
        if event.key == pygame.K_UP:
            tankController.moveUp = False
        if event.key == pygame.K_DOWN:
            tankController.moveDown = False
        if event.key == pygame.K_SPACE:
            tankController.fire = False

def update():
    if joystick != None:
        checkJoystickButtons()

def checkJoystickButtons():
    tankController.fire = joystick.get_button(1)

    xAxis = joystick.get_axis(0)
    yAxis = joystick.get_axis(1)
    tankController.moveLeft = xAxis < -0.01
    tankController.moveRight = xAxis > 0.01
    tankController.moveUp = yAxis < -0.01
    tankController.moveDown = yAxis > 0.01