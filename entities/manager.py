entities = []

def add(entity):
    entities.append(entity)

def remove(entity):
    entities.remove(entity)

def update(time, timePassed):
    disposableEntities = []

    for entity in entities:
        entity.update(time, timePassed)
        if entity.disposable:
            disposableEntities.append(entity)

    for entity in disposableEntities:
        entities.remove(entity)

def render(screen, offset):
    for entity in entities:
        entity.render(screen, offset)

def findEntitiesInRectangle(rectangle, exceptEntity = None):
    result = []
    for entity in entities:
        if entity != exceptEntity and entity.boundingRectangle.colliderect(rectangle):
            result.append(entity)

    return result
