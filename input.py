import pygame

tankController = None

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