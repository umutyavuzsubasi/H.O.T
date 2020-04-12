import pygame
import sys

done = False
# img = pygame.image.load(os.path.join('C:/Users/Gebruiker/Desktop/Renders', 'Render.png')).convert()

while not done:

    keystate = pygame.key.get_pressed()

    if keystate[pygame.K_DOWN]:
        print("AŞAĞI")
    if keystate[pygame.K_UP]:
        print("YUKARI")
    if keystate[pygame.K_LEFT]:
        print("SOL")



sys.exit()