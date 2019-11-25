class Scene():
    def activate(self):
        pass

    def deactivate(self):
        pass

    def update(sefl, time, timePassed):
        pass

    def render(self, surface):
        pass

activeScene = None

def setScene(scene):
    global activeScene
    if activeScene != None:
        activeScene.deactivate()

    activeScene = scene
    activeScene.activate()

def getActiveScene():
    return activeScene
