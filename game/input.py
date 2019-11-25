import pygame
import pygame.joystick

class ButtonStates():
    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.fire = False

tankController = None
joystick = None
buttonStates = ButtonStates()

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
            buttonStates.left = True
        if event.key == pygame.K_RIGHT:
            buttonStates.right = True
        if event.key == pygame.K_UP:
            buttonStates.up = True
        if event.key == pygame.K_DOWN:
            buttonStates.down = True
        if event.key == pygame.K_SPACE:
            buttonStates.fire = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            buttonStates.left = False
        if event.key == pygame.K_RIGHT:
            buttonStates.right = False
        if event.key == pygame.K_UP:
            buttonStates.up = False
        if event.key == pygame.K_DOWN:
            buttonStates.down = False
        if event.key == pygame.K_SPACE:
            buttonStates.fire = False

def update():
    if joystick != None:
        checkJoystickButtons()

def checkJoystickButtons():
    buttonStates.fire = joystick.get_button(1)

    xAxis = joystick.get_axis(0)
    yAxis = joystick.get_axis(1)
    buttonStates.left = xAxis < -0.01
    buttonStates.right = xAxis > 0.01
    buttonStates.up = yAxis < -0.01
    buttonStates.down = yAxis > 0.01