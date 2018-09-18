import Image, pygame
class Entity:
    def __init__(self, x, y, spritePath):
        self.x, self.y, self.sprite = x, y, Image.getImage(spritePath)
    def Update(self):
        pass
    def Render(self, screen):
        screen.blit(self.sprite,(self.x,self.y))
    def isClick(self, mousePos):
        pass
#Would add some form of animation method, but not enough time to make assessts and fix code to support it
class Mole(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "res/mole.png") 
        self.sprite = pygame.transform.scale(self.sprite, (100,100))
        self.score = 100
        self.isDead = False
        self.deathTime = pygame.time.get_ticks() + 2000
    def Update(self):
        if pygame.time.get_ticks() >= self.deathTime:
            self.isDead = True
    def isClick(self, mousePos):
        return self.sprite.get_rect(topleft=(self.x, self.y)).collidepoint(mousePos)
    def returnScore(self):
        return self.score
class RareMole(Mole):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Image.getImage("res/rare.png")
        self.sprite = pygame.transform.scale(self.sprite, (100,100))
        self.score = 250
        self.deathTime = pygame.time.get_ticks() + 1000
class Hammer(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "res/hammer.png") 
        self.sprite = pygame.transform.scale(self.sprite, (50,50))
        self.strike = False
    def Update(self):
        (self.x, self.y) = pygame.mouse.get_pos()
        if not self.strike:
            self.x -= self.sprite.get_width()/4
            self.y -= self.sprite.get_height()/2 
            self.sprite = Image.getImage("res/hammer.png")
            self.sprite = pygame.transform.scale(self.sprite, (50,50))
        else: 
            self.x -= self.sprite.get_width()/4
            self.y -= self.sprite.get_height()/2
            self.sprite = Image.getImage("res/hammerStrike.png")
            self.sprite = pygame.transform.scale(self.sprite, (55,55))