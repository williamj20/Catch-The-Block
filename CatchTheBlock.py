import random
import pygame
import time
import sys

pygame.init()

#sets the size of the screen as well as an FPS counter, and the name of the window
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
game_width, game_length = pygame.display.get_surface().get_size()
pygame.display.set_caption("Catch The Block")
clock = pygame.time.Clock()

#colours
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLUE = (0, 245, 255)
RED = (255, 0, 0)

#creates text objects
def text_objects(text, font):
   textSurface = font.render(text, True, RED)
   return textSurface, textSurface.get_rect()

#message function that appears when you lose
def message_lose(text):
   LargeText = pygame.font.Font("freesansbold.ttf", int(game_width / 20))
   TextSurf, TextRect = text_objects(text, LargeText)
   TextRect.center = ((game_width / 2), (game_length / 2))
   display.blit(TextSurf, TextRect)
   pygame.display.flip()
   time.sleep(5)
   endgame()
   
#introduction & instructions to the game
def message_intro(intro):
   IntroText = pygame.font.Font("freesansbold.ttf", int(game_width/70))
   TextSurf, TextRect = text_objects(intro, IntroText)
   TextRect.center = ((game_width/2), (game_length / 2))
   display.blit(TextSurf, TextRect)
   pygame.display.flip()
   time.sleep (5)

  

#extra function that creates the text used to introduce the game   
def initiategame():
   message_intro("Catch the blocks by moving underneath them before they hit the bottom! Use arrow keys to move and the 'B' key to accelerate!")
   
#score counter
def message_win(score):
   font = pygame.font.SysFont(None, 50)
   text = font.render("Score: " + str(score), True, RED)
   display.blit(text, (0, 0))

#extra function that creates the text used after you lose the game
def gameover(score):
   message_lose("You missed the block! Game over!")
   time.sleep(3)
   quit



#drawing the rectangles
def blocks(blocksx, blocksy, width, height):
   pygame.draw.rect(display, WHITE, (blocksx, blocksy, width, height))

#drawing the circle
def circle(x, y, colour, radius):
   circle = pygame.draw.circle(display, colour, (x, y), radius, 0)
#function used to close game
def endgame():
   pygame.quit()
   sys.exit()
#actual game
def game():
   #a lot of variables introduced
   x = int(game_length * 0.9) #x-axis value of circle
   y = int(game_width * 0.54) #y-axis value of circle
   radius = 25 #radius of circle
   x_change = 0 #x-axis movement of circle
   x_posaccel = 0 #x-axis acceleration of circle
   x_negaccel = 0 #x-axis acceleration of circle
   colour = GREEN #colour of circle
   blocksx = random.randrange(0, game_width) #initial spawn of rectangle
   blocksy = -300 #initial spawn of rectangle
   block_speed = game_length/190 #speed at which the rectangle travels
   width = 55 #width of rectangle
   height = 100#length of rectangle
   score = 0
   close = False
   
   while not close:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               close = True
            #keyboard movements & controls
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_LEFT:
                   x_change = -5
               if event.key == pygame.K_RIGHT:
                   x_change = 5
               if event.key == pygame.K_b:
                   x_posaccel = 6
                   x_negaccel = -6
                   colour = RED #if you are accelerating, the circle becomes red
               if event.key == pygame.K_ESCAPE:
                   endgame()
           if event.type == pygame.KEYUP:
               if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                   x_change = 0
               if event.key == pygame.K_b:
                   x_posaccel = 0
                   x_negaccel = 0
                   colour = GREEN#if you stop accelerating, the circle returns back to green
                   
      #acceleration of the circle
       if x_change > 0:
           x_change += x_posaccel
           if x_change > 11:
               x_change = 11
       if x_change < 0:
           x_change += x_negaccel
           if x_change < -11:
               x_change = -11
       x += x_change
       display.fill(BLUE)
       
       #movement of the circle
       if x + 25 > game_width:
           x_change = 0
           x = game_width - 25

       if x - 25 < 0:
           x_change = 0
           x = 0 + 25

       blocks(blocksx, blocksy, width, height)#initiates block drawer
       
       circle(x, y, colour, radius) #initates circle drawer
       
       blocksy += block_speed #initiates block speed
       message_win(score) #initiates score counter
       #if the circle successfully "catches" the block - collision interaction
       if blocksy + height - radius < y < blocksy + height + radius: 
           if blocksx - radius < x < blocksx + width + radius:
               blocksy = 0
               blocksx = random.randrange(0, game_width-width)
               score += 1
       #if the circle misses the block        
       if blocksy > game_length:
           gameover(score)

       pygame.display.flip()
       clock.tick(144)
#runs intro of the game and actual game
initiategame()
game()



