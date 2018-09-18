def run(width, height, fps, scene):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("WACK OF MOLE")
    pygame.display.set_icon(Image.getImage("res/hammer.png"))
    clock = pygame.time.Clock()
    score = 0
    activeScene = scene
    while activeScene != None:
        pressedKeys = pygame.key.get_pressed()
        #Event filtering - Detects if user wants to close the game, otherwise sends inputs to be handled by scene
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            #Checks if window is being closed or if alt-f4 is pressed (pygame doesn't close on alt-f4 by default)
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressedKeys[pygame.K_LALT] or pressedKeys[pygame.K_RALT]
                if event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            if quit_attempt:
                activeScene.Terminate()
            else:
                filtered_events.append(event)

        #Call the methods in the active scene
        activeScene.ProcessInput(filtered_events, pressedKeys)
        activeScene.Update()
        activeScene.Render(screen)

        #Check if scene needs to be changed
        activeScene = activeScene.next
        #Update the buffer and tick to the next frame
        pygame.display.flip()
        clock.tick(fps)
        #print ("fps:", clock.get_fps())

WIDTH, HEIGHT = 640, 480
if __name__ == "__main__":
    import pygame, sys, Image
    import SceneBase as Scene
    pygame.init()
    pygame.mouse.set_visible(False)
    title = Scene.TitleScene(WIDTH, HEIGHT)
    run(WIDTH, HEIGHT, 60, title)
input()