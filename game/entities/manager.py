entities = []

def add(entity):
    entities.append(entity)

def remove(entity):
    entities.remove(entity)

def clear():
    entities.clear()

def update(time, timePassed):
    disposableEntities = []

    for entity in entities:
        entity.update(time, timePassed)
        if entity.disposable:
            disposableEntities.append(entity)

    for entity in disposableEntities:
        entity.dispose()
        entities.remove(entity)

def render(screen, offset, time):
    for entity in entities:
        entity.render(screen, offset, time)

def findEntitiesInRectangle(rectangle, typeFilter = None, exceptEntity = None):
    for entity in entities:
        if entity == exceptEntity:
            continue

        if not typeFilter == None and not isinstance(entity, typeFilter):
            continue
        
        if entity.boundingRectangle.colliderect(rectangle):
            yield entity