import pygame, Entities, sys, random, Image
class SceneBase:
    def __init__(self, width, height):
        self.next = self
        self.width, self.height = width, height
    def ProcessInput(self, events, pressed_keys):
        print("ProcessInput not overwritten")
    def Update(self):
        print("Update not overwritten")
    def Render(self, screen):
        print("Render not overwritten")
    def SwitchToScene(self, next_scene):
        self.next = next_scene
    def Terminate(self):
        self.SwitchToScene(None)
        pygame.quit()

class TitleScene(SceneBase):
    def __init__(self, width, height):
        self.font = pygame.font.SysFont("arial", 64)
        self.toRender = []
        self.title = self.font.render("WHACK-A-MOLE", True, (50, 255, 128))
        self.start = self.font.render("Start", True, (0, 255, 128))
        self.exit = self.font.render("Exit", True, (0, 255, 128))
        self.toRender.extend([self.title, self.start, self.exit])
        self.option = 0
        super().__init__(width, height)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                if self.option == 0:
                    self.SwitchToScene(MoleScene(self.width, self.height))
                if self.option == 1:
                    self.Terminate()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                self.option = 1
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_w):
                self.option = 0
    def Update(self):
        if self.option == 0:
            self.toRender[1] = self.font.render("Start <", True, (0, 255, 255))
            self.toRender[2] = self.font.render("Exit", True, (50, 50, 50))
        elif self.option == 1:
            self.toRender[1] = self.font.render("Start", True, (50, 50, 50))
            self.toRender[2] = self.font.render("Exit <", True, (0, 255, 255))
    def Render(self, screen):
        screen.fill((255, 0, 0))
        for i in range(0,len(self.toRender)):
            screen.blit(self.toRender[i], ((self.width / 2) - (self.title.get_width())/2, self.height / (len(self.toRender)-i) - (self.title.get_height())))
            
class MoleScene(SceneBase):
    def __init__(self, width, height):
        self.font = pygame.font.SysFont("arial", 48)
        self.entities = []
        self.score = 0
        self.scoreDisplay = None
        self.livesDisplay = None
        self.missDisplay = None
        self.misses = 0
        #This is disgustingly hardcoded, but it works and Im too tired to deal with this
        self.grid = [[0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]
        self.hammer = Entities.Hammer(0,0)
        self.difficulty = 3000
        self.challenge = self.difficulty
        self.offset = 75
        self.lives = 5
        self.moleHill = Image.getImage("res/moleHill.png")
        self.moleHill = pygame.transform.scale(self.moleHill, (100,100))
        super().__init__(width, height)
    def ProcessInput(self, events, press_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickMole = False
                self.hammer.strike = True
                for each in self.entities:
                    if(each.isClick(pygame.mouse.get_pos())):
                        clickMole = True
                        self.score += each.returnScore()
                        gridx = int(((each.x - self.offset)/ each.sprite.get_width()))
                        gridy = int(((each.y - self.offset)/ each.sprite.get_height()))
                        self.grid[gridy][gridx] = 0
                        self.entities.remove(each)
                        break
                if not clickMole:
                    self.score -= 50
                    self.misses += 1
            if event.type == pygame.MOUSEBUTTONUP:
                self.hammer.strike = False
    def Update(self):
        if self.score < 0: self.score = 0
        self.scoreDisplay = self.font.render(("Score: "+str(self.score)), True, (0, 0, 0))
        self.livesDisplay = self.font.render(("Lives: "+str(self.lives)), True, (0, 0, 0))
        self.populateMoles()
        if self.misses == 0:
            self.missDisplay = self.font.render("- - -", True, (0, 0, 0))
        elif self.misses == 1:
            self.missDisplay = self.font.render("X - -", True, (0, 0, 0))
        elif self.misses == 2:
            self.missDisplay = self.font.render("X X -", True, (0, 0, 0))
        else:
            self.lives -= 1
            self.misses = 0
        #Possibly check for a death flag in the mole class that turns true after a couple seconds, losing lives
        for each in self.entities:
            each.Update()
            if each.isDead:
                self.entities.remove(each)
                self.lives -= 1
        self.hammer.Update()
        #Yay for digusting hard coded messes of if statements where switch case would have been so much nicer but python doesnt support it \o/
        if self.score in range(1000,2000):
            self.difficulty = 2600
        elif self.score in range(2000,3000):
            self.difficulty = 2200
        elif self.score in range(3000,4000):
            self.difficulty = 1800
        elif self.score in range(4000,5000):
            self.difficulty = 1400
        elif self.score in range(5000,6000):
            self.difficulty = 1200
        elif self.difficulty in range(6000,10000):
            self.difficulty = 800
        elif self.difficulty in range(10000, 15000):
            self.difficulty = 500
        elif self.difficulty in range(15000,20000):
            self.difficulty = 250
        if self.lives <= 0:
            self.SwitchToScene(EndScene(self.width, self.height, self.score))
    def Render(self, screen):
        screen.fill((50,255,50))
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                screen.blit(self.moleHill, ((c * self.moleHill.get_width() + self.offset), ((r * self.moleHill.get_height() + self.offset))))
        for each in self.entities:
            each.Render(screen)
        self.hammer.Render(screen)
        screen.blit(self.scoreDisplay, (0,0))
        screen.blit(self.livesDisplay, (self.scoreDisplay.get_width() + 25,0))
        screen.blit(self.missDisplay, (screen.get_width() - 150, 0))
    def populateMoles(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 0:
                    rand = random.randint(0,self.challenge)
                    rare = random.randint(0,5)
                    if rand == 0:
                        self.challenge = self.difficulty
                        if not rare == 0:
                            mole = Entities.Mole(0,0)
                        else:
                            mole = Entities.RareMole(0,0)
                        #places them nicely so they don't overlap
                        mole.x = (c * mole.sprite.get_width()) + self.offset
                        mole.y = (r * mole.sprite.get_height()) + self.offset
                        self.grid[r][c] = 1
                        self.entities.append(mole)
                    else: 
                        self.challenge -= 1

class EndScene(SceneBase):
    def __init__(self, width, height, score):
        self.font = pygame.font.SysFont("arial", 64)
        self.toRender = []
        self.title = self.font.render("GAME OVER!", True, (50, 255, 128))
        self.scoreDisplay = self.font.render("Your Score was: " + str(score), True, (0,255,255))
        self.toRender.extend([self.title, self.scoreDisplay])
        super().__init__(width, height)
    def Update(self):
        pass
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                self.Terminate()
    def Render(self, screen):
        screen.fill((255, 0, 0))
        #So redundant for rendering two fonts, literally the same lines of code for rendering two items, but Im lazy and so will just copy paste my old code
        for i in range(0,len(self.toRender)):
            screen.blit(self.toRender[i], ((self.width / 2) + 25 - (self.title.get_width()), self.height / (len(self.toRender)-i) - (self.title.get_height())))
             