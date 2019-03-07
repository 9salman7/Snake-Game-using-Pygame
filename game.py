#Importing modules 
import pygame, sys, time, random

#Initialization of sound module
pygame.mixer.pre_init(44100, -16, 1, 512)

#initialising pygame and checking for error
check_error = pygame.init()
if check_error[1] > 0:
    print("Error in initialising PyGame")
    sys.exit(1)
else:
    print("PyGame successfully initialized, starting project")

#defining the Play Surface
playSurface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('---SNAKE v1.0---')

#defining the Colors used (RBG values in parentheses)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
brown = pygame.Color(162,42,42)
gray = pygame.Color(50, 50, 50)
yellow = pygame.Color(255,255,0)

#declaring the sound variables
pop = pygame.mixer.Sound('sounds/pop.wav')
explosion = pygame.mixer.Sound('sounds/explosion.wav')
select = pygame.mixer.Sound('sounds/select.wav')
select2 = pygame.mixer.Sound('sounds/select2.wav')

#FPS Controller variable
fpsController = pygame.time.Clock()

#Variables used for game logic
class gamevar:

    direction = 'RIGHT'
    changeTo = direction
    score = 0

snakePos = [100,50]
snakeBody = [[100,50],[90,50],[80,50]] #,[70,50],[60,50],[50,50],[40,50],[30,50],[20,50]

foodPos = [random.randrange(1,72)*10, random.randrange(1,46)*10]
foodSpawn = True

font = "8-Bit-Madness.ttf"

#opening the high score text file
highscore_file = open('highscore.dat', "r")
highscore_int = int(highscore_file.read())


#Text rendering function
def message_to_screen(message, textfont, size, color):
   
    my_font = pygame.font.Font(textfont, size)
    my_message = my_font.render(message, 0, color)

    return my_message


#Game Over Function
def gameOver():

    if gamevar.score > highscore_int:
        highscore_file = open('highscore.dat', "w")          
        highscore_file.write(str(gamevar.score))            #writes data to the file using write mode
        highscore_file.close()
   
    myFont = pygame.font.Font(font,100)
    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360,15)
    playSurface.blit(GOsurf, GOrect)
    sFont = pygame.font.SysFont('Sawasdee', 50)
    Ssurf = sFont.render('Your Score : {0}'.format(gamevar.score), True, white)
    Srect = Ssurf.get_rect()
    Srect.midtop = (360, 150)
    
    playSurface.blit(Ssurf, Srect)
    pygame.display.flip()

    time.sleep(2)
    pygame.quit()
    quit()
    

#Score function
def showScore(choice=1):
   
    sFont = pygame.font.SysFont('Sawasdee', 27)
    Ssurf = sFont.render('Score : {0}'.format(gamevar.score), True, white)
    Srect = Ssurf.get_rect()
    Srect.midtop = (80, 10)
    playSurface.blit(Ssurf, Srect)
    hi_score_message = sFont.render("High Score : {0}".format(highscore_int), True, white)
    hi_score_message_rect = hi_score_message.get_rect()
    playSurface.blit(hi_score_message, (400-hi_score_message_rect[2]-10, 10))
    pygame.draw.line(playSurface,red, (120, 230), (600, 230), 4)


#Menu function
def menu():
 
    menu = True
    choice = "Play"
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                pygame.mixer.Sound.play(select2)

                if event.key == pygame.K_UP:
                    choice = "Play"
                elif event.key == pygame.K_DOWN:
                    choice = "Quit"
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN: 
                    pygame.mixer.Sound.play(select)
                    if choice == "Play":
                        menu = False
                    if choice == "Quit":
                        pygame.quit()
                        quit()
        playSurface.fill(brown)
        title = message_to_screen("SNAKE", font, 100, black)
        controls_1 = message_to_screen("Use the arrow kews to move the snake", font, 30, black)
        if choice == "Play":
            play = message_to_screen("PLAY", font, 75, white)
        else:
            play = message_to_screen("PLAY", font, 75, black)
        if choice == "Quit":
            game_quit = message_to_screen("QUIT", font, 75, white)
        else:
            game_quit = message_to_screen("QUIT", font, 75, black)

        title_rect = title.get_rect()
        controls_1_rect = controls_1.get_rect()
        play_rect = play.get_rect()
        quit_rect = game_quit.get_rect()

        #Drawing the text
        playSurface.blit(title, (720/2 - (title_rect[2]/2), 40))
        playSurface.blit(controls_1, (720/2 - (controls_1_rect[2]/2), 120))
        playSurface.blit(play, (720/2 - (play_rect[2]/2), 200))
        playSurface.blit(game_quit, (720/2 - (quit_rect[2]/2), 260))

        pygame.display.update()
        fpsController.tick(30)


#main game function
def game():
    
    global changeTo
    global direction
    global score
    global foodSpawn
    global foodPos

    menu = True
    choice = "easy"
    FPS = 15
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                pygame.mixer.Sound.play(select2)

                if event.key == pygame.K_UP:
                    choice = "easy"
                    FPS = 15
                elif event.key == pygame.K_DOWN:
                    choice = "medium"
                    FPS = 30
                elif event.key == pygame.K_LEFT:
                    choice = "hard"
                    FPS = 45
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN: 
                    pygame.mixer.Sound.play(select)
                    if choice == "easy":
                        menu = False
      
                    if choice == "medium":
                        menu = False
                    if choice == "hard":
                        menu = False
        
        playSurface.fill(brown)
        
        if choice == "easy":
            ez = message_to_screen("EASY", font, 75, white)
        else:
            ez = message_to_screen("EASY", font, 75, black)
        if choice == "medium":
            med = message_to_screen("MEDIUM", font, 75, white)
        else:
            med = message_to_screen("MEDIUM", font, 75, black)
        if choice == "hard":
            hd = message_to_screen("HARD", font, 75, white)
        else:
            hd = message_to_screen("HARD", font, 75, black)
        ez_rect = ez.get_rect()
        med_rect = med.get_rect()
        hd_rect = hd.get_rect()

        # drawing text
        playSurface.blit(ez, (720/2 - (ez_rect[2]/2), 160))
        playSurface.blit(med, (720/2 - (med_rect[2]/2), 220))
        playSurface.blit(hd, (720/2 - (hd_rect[2]/2),280))
        pygame.display.update()
        fpsController.tick(30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    gamevar.changeTo = 'RIGHT'
                if event.key == pygame.K_LEFT:
                    gamevar.changeTo = 'LEFT'
                if event.key == pygame.K_UP:
                    gamevar.changeTo = 'UP'
                if event.key == pygame.K_DOWN:
                    gamevar.changeTo = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    gamevar.pygame.event.post(pygame.event.Event(pygame.QUIT))


        # Validation of direction
        if gamevar.changeTo == 'RIGHT' and not gamevar.direction == 'LEFT':
            gamevar.direction = 'RIGHT'
        if gamevar.changeTo == 'LEFT' and not gamevar.direction == 'RIGHT':
            gamevar.direction = 'LEFT'
        if gamevar.changeTo == 'UP' and not gamevar.direction == 'DOWN':
            gamevar.direction = 'UP'
        if gamevar.changeTo == 'DOWN' and not gamevar.direction == 'UP':
            gamevar.direction = 'DOWN'

        if gamevar.direction == 'RIGHT':
            snakePos[0] += 10
        if gamevar.direction == 'LEFT':
            snakePos[0] -= 10
        if gamevar.direction == 'UP':
            snakePos[1] -= 10
        if gamevar.direction == 'DOWN':
            snakePos[1] += 10

        
        #Snake body mechanism
        snakeBody.insert(0, list(snakePos))
        if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
            gamevar.score+=10
            pygame.mixer.Sound.play(pop)
            foodSpawn = False
        else:
            snakeBody.pop()

        #Spawning food as a random function    
        if foodSpawn == False:
            foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
        foodSpawn = True

        
        pygame.draw.line(playSurface,red, (60, 60), (120, 60), 4)

        playSurface.fill(gray)
        for pos in snakeBody:
            pygame.draw.rect(playSurface,green,pygame.Rect(pos[0], pos[1],10,10))

        pygame.draw.rect(playSurface, yellow, pygame.Rect(foodPos[0], foodPos[1], 10, 10))

        #Conditions for Game Over
        if snakePos[0] > 710 or snakePos[0] < 0:
            pygame.mixer.Sound.play(explosion)
            gameOver()
        if snakePos[1] > 450 or snakePos[1] < 0:
            pygame.mixer.Sound.play(explosion) 
            gameOver()
        for block in snakeBody[1:]:
            if snakePos[0] == block[0] and snakePos[1] == block[1]:
                pygame.mixer.Sound.play(explosion)
                gameOver()
        if snakePos[0] > 120 and snakePos[0] < 600 and snakePos[1] == 230:
            pygame.mixer.Sound.play(explosion)
            gameOver()
        showScore()
        pygame.display.flip()
        fpsController.tick(FPS)

menu()    #calling the menu function
game()    #calling the game function