import os, pygame
#This method returns a pygame styled image from a directory that can then be drawn onto the surface
def getImage(path):
    image_library = {}
    image = image_library.get(path)
    if image == None: 
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            image_library[path] = image
    return image