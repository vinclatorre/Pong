# Import
import pygame
import sys

# Functions
def global_variable():
    global player_x, player_y, player_speed, loop
    global opponent_x, opponent_y, oppo_speed
    global ball_x, ball_y, ballx_speed, bally_speed
    
    
def run_game():
    ''' Main loop '''
    global_variable()
    global player, opponent, ball, screen, left_render, right_render, you_won, game_over
    menu()
    while loop:
        # Create screen and game rectangles
        screen = pygame.display.set_mode((screen_width,screen_height))
        screen.fill(black)
        player = pygame.Rect(player_x,player_y,p_width,p_height)
        opponent = pygame.Rect(opponent_x, opponent_y, p_width,p_height)
        ball = pygame.Rect(ball_x,ball_y,15,15)
        left_render = FONT.render(str(left_points), 1, white)
        right_render = FONT.render(str(right_points), 1, white)
        you_won = FONT.render('you  won',1, white)
        game_over = FONT.render('game  over',1, white)
       
        # Call functions
        events()
        check_collision()
        ai()
        draw()
        check_points()
        update_speed()
        pygame.display.update()
        
def events():
    ''' keyboard command '''
    global loop, event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            key_down_events()
        if event.type == pygame.KEYUP:
            key_up_events()
    
def key_down_events():
    '''check key_down_events'''
    global player_speed, ballx_speed, bally_speed, game_over
    if event.key == pygame.K_UP:
        player_speed -= 5
    if event.key == pygame.K_DOWN:
        player_speed += 5

def key_up_events():
    '''check key_up_events'''
    global player_speed
    if event.key == pygame.K_UP:
        player_speed = 0
    if event.key == pygame.K_DOWN:
        player_speed = 0

def check_collision(): 
    player_collision()
    opponent_collision()
    ball_collision()
    
def player_collision():
    '''Player-Border collision'''
    global player_y, player_speed
    if player.bottom >= screen_height:
        player_speed = 0
        player_y -= 1
    if player.top <= 0:
        player_speed = 0
        player_y += 1

def opponent_collision():
    '''Opponent-Border collision'''
    global opponent_y, oppo_speed
    if opponent.bottom >= screen_height:
        oppo_speed = 0
        opponent_y -= 1
    if opponent.top <= 0:
        oppo_speed = 0
        opponent_y += 1

def ball_collision():
    '''Ball-Border collision'''
    global bally_speed, ballx_speed, ball_x, ball_y, left_points, right_points
    # top and bottom collision
    if ball.bottom >= screen_height or ball.top <= 0:
        pygame.mixer.Sound.play(pong_sound)
        bally_speed *= -1
    # player score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        ball_x, ball_y = 325, 210
        left_points += 1
    # opponent score
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        ball_x, ball_y = 325, 210
        right_points += 1

    '''Ball-Player collision'''
    tollerance = 10
    if ball.colliderect(player) and ballx_speed < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(player.right - ball.left) < tollerance:
            ballx_speed *= -1
        if abs(ball.bottom - player.top) < 10 and bally_speed > 0:
            bally_speed *= -1
        if abs(ball.top - player.bottom) < 10 and bally_speed < 0:
            bally_speed *= -1
            
    '''Ball-Opponent collision'''
    if ball.colliderect(opponent) and ballx_speed > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(opponent.left - ball.right) < tollerance:
            ballx_speed *= -1
        if abs(ball.bottom - opponent.top) < 10 and bally_speed > 0:
            bally_speed *= -1
        if abs(ball.top - opponent.bottom) < 10 and bally_speed < 0:
            bally_speed *= -1

def ai():
    '''Move automatically the opponent'''
    global oppo_speed
    if ball_y == 210:
        oppo_speed = 0
    if opponent_y < ball_y and abs(opponent_y - ball_y) > 10:
        oppo_speed += 0.10
    if opponent_y > ball_y and abs(opponent_y - ball_y) > 10:
        oppo_speed -= 0.10

def update_speed():
    '''Constanly updates x and y values to make rectangles move'''
    global player_y, opponent_y, ball_x, ball_y
    player_y += player_speed
    opponent_y += oppo_speed
    ball_x += ballx_speed
    ball_y += bally_speed

def draw():
    '''Draw object on the screen'''
    pygame.draw.rect(screen,white,player)
    pygame.draw.rect(screen,white,opponent)
    pygame.draw.rect(screen,white,ball)
    screen.blit(left_render,(260,0))
    screen.blit(right_render,(375,0))
    y = 0
    for i in range(0,15):
        pygame.draw.rect(screen,white,[325,y,15,15])
        y+=30

def menu():
    '''Start menu'''
    global loop
    while not loop:
        menu = pygame.display.set_mode((screen_width,screen_height))
        menu.fill(black)
        start = FONT.render('press space to play', False, white)
        menu.blit(start, (150,225))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    loop = True
                    run_game()
                    
        # print on the screen if you win or not
        if win == True:
            menu.blit(you_won,(250,170))
            
        if loose == True:
            menu.blit(game_over,(220,170))
            
        pygame.display.update()

def check_points():
    '''If left points or right points are equal to 5 stop game and open menu'''
    global loop, left_points, right_points, win, loose
    if left_points == 5:
        left_points, right_points = 0, 0
        loop = False
        win = True
        loose = False
        menu()
        
    if right_points == 5: 
        left_points, right_points = 0, 0
        loop = False
        loose = True
        win = False
        menu()
        
# Inizialize pygame
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

# Variables
screen_width, screen_height = 650,450

player_x,player_y,p_width,p_height = 30,0,15,80
opponent_x, opponent_y = 620, 180
player_speed = 0
oppo_speed = 0
ball_x, ball_y = 325, 210
ballx_speed, bally_speed = -2,2

FONT = pygame.font.SysFont('8-BIT WONDER', 50, bold = True)
left_points = 0
right_points = 0

pong_sound = pygame.mixer.Sound('pong.ogg')
score_sound = pygame.mixer.Sound('score.ogg')

white = ((240, 240, 240))
black = ((0, 0, 20))

win = False
loose = False

loop = False

# Game
run_game()




