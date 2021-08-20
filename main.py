# Author: Marvin Wiebe

# Horserace is a drinking game using playing cards that is inspired by horse racing.
# Instead of alcohol, participants bet amounts of virtual coins on one of four aces,
# much like bettors would bet money on horses at a racing track.
# The winner of the game is the player who collects the most coins after 5 rounds.
# In every round each player chooses an amount of coins, an ace to bet on and another
# player to snatch the coins from. The game will end earlier if any player loses all
# his coins.

# To play the game, you need python installed on your computer as well as the
# pygame module. Furthermore, there are files provided which are necessary
# for the execution of the game:
# 1. colorcodes
# 2. font
# which which used within the game

# If your environment is set up, you just need 3 other players to join the game.
# Enjoy!


# importing the the necessary modules
import pygame as pg
import time
import random
import sys
from colorcodes import *
from pygame.locals import *

# initalizing the game clock
clock = pg.time.Clock()


# setting various global variables (e.g. width/height of the screen, position of cards)
W = 1200
H = 675

X_TRACK_START = 300
Y_TRACK_START = 150
X_TRACK_FINISH = 900
Y_TRACK_FINISH = 590

TRACK_LENGTH = X_TRACK_FINISH - X_TRACK_START
TRACK_HEIGHT = Y_TRACK_FINISH - Y_TRACK_START

CARD_WIDTH = 130
CARD_HEIGHT = 90

track_card1_covered = True
track_card2_covered = True
track_card3_covered = True

pos_diamonds = 0
pos_hearts = 0
pos_spades = 0
pos_clubs = 0
x_pos = [310, 460, 610, 760]

Y_DIAMONDS = 160
Y_HEARTS = 270
Y_SPADES = 380
Y_CLUBS = 490

STANDARD_DISTANCE = 10
DISTANCE_DASHED_LINES = 20
ADD_X_Y = 15

PLAYER_CORNER_WIDTH = 250
PLAYER_CORNER_HEIGHT = 150

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675

font_custom = 'seguisym.ttf'

# RGB codes for various colors
RED = (200,0,0)
GREEN = (0, 200, 0)
LIGHT_GREEN = (0, 255, 0)
LIGHT_RED = (255, 0, 0)
BLUE = (0,0,255)
SKY_BLUE = (0,255,255)
PINK = (255,100,180)
PURPLE = (240,0,255)
LIGHT_GRAY = (200,200,200)
DARK_GRAY = ((50,50,50))
GOLD = (255,215,0)
PALE_GOLD = (238,232,170)
LIGHT_GOLDEN = (250,250,210)
active_colors = [LIGHT_GREEN, LIGHT_RED, SKY_BLUE, PURPLE]
passive_colors = [GREEN,RED,BLUE,PINK]

# unicodes for card symbols
heart = "\u2661"
diamond = "\u2662"
club = "\u2663"
spade = "\u2660"

symbols = [club, diamond, heart, spade]
values = ["7", "8", "9", "10", "Jack", "Queen", "King"]
players = ["Player1", "Player2", "Player3", "Player4"]
coins_stake_options = [5, 10, 15, 20, 25, 30]

#player coins
player_coins = [100, 100, 100, 100]

#lists of choosen options
players_symbols = [None,None,None,None]
players_stakes = [None,None,None,None]
players_target = [None,None,None,None]

# button coordinates to select symbols
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 100
BUTTON1_X_POS = ((SCREEN_WIDTH*0.2)-(BUTTON_WIDTH/2))
BUTTON2_X_POS = ((SCREEN_WIDTH*0.4)-(BUTTON_WIDTH/2))
BUTTON3_X_POS = ((SCREEN_WIDTH*0.6)-(BUTTON_WIDTH/2))
BUTTON4_X_POS = ((SCREEN_WIDTH*0.8)-(BUTTON_WIDTH/2))
BUTTON_Y = SCREEN_HEIGHT*0.25-(BUTTON_HEIGHT/2)

# button coordinates - select amount of coins
BUTTON_COINS_Y = SCREEN_HEIGHT*0.5
BUTTON5_COINS_X = (SCREEN_WIDTH*(1/7))
BUTTON10_COINS_X = SCREEN_WIDTH*(2/7)
BUTTON15_COINS_X = SCREEN_WIDTH*(3/7)
BUTTON20_COINS_X = SCREEN_WIDTH*(4/7)
BUTTON25_COINS_X = SCREEN_WIDTH*(5/7)
BUTTON30_COINS_X = SCREEN_WIDTH*(6/7)
BUTTON_COINS_RADIUS = 30

# button coordinates - select player you want to snatch your profit fromn
BUTTON_PLAYERS_HEIGHT = 75
BUTTON_PLAYERS_WIDTH = 125
BUTTON_PLAYERS_Y = SCREEN_HEIGHT*0.75-(BUTTON_PLAYERS_HEIGHT/2)
BUTTON_PLAYER1_X_POS = ((SCREEN_WIDTH*0.2)-(BUTTON_WIDTH/2))
BUTTON_PLAYER2_X_POS = ((SCREEN_WIDTH*0.4)-(BUTTON_WIDTH/2))
BUTTON_PLAYER3_X_POS = ((SCREEN_WIDTH*0.6)-(BUTTON_WIDTH/2))
BUTTON_PLAYER4_X_POS = ((SCREEN_WIDTH*0.8)-(BUTTON_WIDTH/2))

button_symbols_x = [BUTTON1_X_POS, BUTTON2_X_POS, BUTTON3_X_POS, BUTTON4_X_POS]
button_coins_x = [BUTTON5_COINS_X, BUTTON10_COINS_X, BUTTON15_COINS_X, BUTTON20_COINS_X, BUTTON25_COINS_X, BUTTON30_COINS_X]
button_player_x = [BUTTON_PLAYER1_X_POS, BUTTON_PLAYER2_X_POS, BUTTON_PLAYER3_X_POS, BUTTON_PLAYER4_X_POS]

# lists to manage all buttons
buttons_select_symbol = []
buttons_select_amount_of_coins = []
button_select_player = []


# card coordinates

CARD_POS0 = [X_TRACK_FINISH + 70 + 3 * ADD_X_Y, Y_TRACK_START + TRACK_HEIGHT / 2 - (CARD_HEIGHT - 2 * ADD_X_Y)]
CARD_POS1 = [x_pos[1] + STANDARD_DISTANCE, Y_TRACK_START - STANDARD_DISTANCE - CARD_HEIGHT]
CARD_POS2 = [x_pos[2] + STANDARD_DISTANCE, Y_TRACK_START - STANDARD_DISTANCE - CARD_HEIGHT]
CARD_POS3 = [x_pos[3] + STANDARD_DISTANCE, Y_TRACK_START - STANDARD_DISTANCE - CARD_HEIGHT]


#combining symbols and values (except aces) of cards
cards = []
for s in symbols:
    for v in values:
        cards.append(s+v)

random.shuffle(cards)


#combining symbols and values of aces
value_ace = ["Ace"]

aces = []
for s in symbols:
    for v in value_ace:
        aces.append(s+v)


# button class for symbols
class buttonSymbols():
    def __init__(self, color_pass, color_act, x , y , width, height, text):
        self.color_act = color_act
        self.color_pass = color_pass
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active = False

# function to check if the mouse hovers over a button
    def isOver(self):
        pos = pg.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

# function to check if the button is clicked
    def isClicked(self):
        if self.isOver():
            for event in event_list:
                if event.type == pg.MOUSEBUTTONDOWN:
                    return True
        return False


# getter and setter
    def setStatus(self, status):
        self.active = status

    def getStatus(self):
        return self.active

    def getSymbol(self):
        return self.text

# function that allow to compare buttons with the equal operater (==)
    def __eq__(self, other):
        if (isinstance(other, buttonSymbols)):
            return self.x == other.x
        return false

# function to draw the button
    def draw(self, screen ,outline=None):
        if outline:
            pg.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0,3)
        if self.isOver() or self.active:
            pg.draw.rect(screen, self.color_act, (self.x-2,self.y-2,self.width+4,self.height+4),0,3)
        else:
            pg.draw.rect(screen, self.color_pass, (self.x-2,self.y-2,self.width+4,self.height+4),0,3)

        if self.text != '':
            font = pg.font.Font('seguisym.ttf', 40)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


# button class for coins
class buttonCoins():
    def __init__(self, x , y , radius, value, text):
        self.x = x
        self.y = y
        self.radius = radius
        self.value = value
        self.text = text
        self.active = False

# function to check if the mouse hovers over a button
    def isOver(self):
        pos = pg.mouse.get_pos()
        if pos[0] > self.x - self.radius and pos[0] < self.x + self.radius:
            if pos[1] > self.y - self.radius and pos[1] < self.y + self.radius:
                return True
        return False

# function to check if the button is clicked
    def isClicked(self):
        if self.isOver():
            for event in event_list:
                if event.type == pg.MOUSEBUTTONDOWN:
                    return True
        return False

# getter and setter
    def setStatus(self, status):
        self.active = status

    def getStatus(self):
        return self.active

    def getCoins(self):
        return self.value

# function that allows to compare buttons with the equal operator (==)
    def __eq__(self, other):
        if (isinstance(other, buttonCoins)):
            return self.x == other.x
        return false

# function to draw the button
    def draw(self, screen ,outline=None):
        if outline:
            pg.draw.circle(screen, outline, (self.x, self.y) ,self.radius,0)
        if self.isOver() or self.active:
            pg.draw.circle(screen, DARK_GRAY, (self.x, self.y) ,self.radius,0)
        else:
            pg.draw.circle(screen, LIGHT_GRAY, (self.x, self.y) ,self.radius,0)

        if self.text != '':
            font = pg.font.Font('seguisym.ttf', (self.radius))
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x - self.radius*0.6 , self.y - self.radius*0.7))


# button class for players (to snatch the coins from)
class buttonPlayers():
    def __init__(self, color_pass, color_act, x , y , width, height, text=''):
        self.color_act = color_act
        self.color_pass = color_pass
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active = False

# function to check if the mouse hovers over a button
    def isOver(self):
        pos = pg.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

# function to check if the button is clicked
    def isClicked(self):
        if self.isOver():
            for event in event_list:
                if event.type == pg.MOUSEBUTTONDOWN:
                    return True
        return False

# getter and setter
    def setStatus(self, status):
        self.active = status

    def getStatus(self):
        return self.active

    def getPlayer(self):
        player_num = int(self.text[-1])-1
        return player_num

# function that allows to compare buttons with the equal operator (==)
    def __eq__(self, other):
        if (isinstance(other, buttonPlayers)):
            return self.x == other.x
        return false

# function to draw the buttons
    def draw(self, screen ,outline=None):
        if outline:
            pg.draw.ellipse(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        if self.isOver() or self.active:
            pg.draw.ellipse(screen, self.color_act, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        else:
            pg.draw.ellipse(screen, self.color_pass, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        if self.text != '':
            font = pg.font.Font('seguisym.ttf', 35)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))



# functions to build all of the necessary buttons
def build_playerbuttons():
    i = 0
    for player in players:
        button = buttonPlayers(PALE_GOLD, GOLD,button_player_x[i] , BUTTON_PLAYERS_Y, BUTTON_PLAYERS_WIDTH, BUTTON_PLAYERS_HEIGHT,player)
        button_select_player.append(button)
        i = i+1

def build_coinbuttons():
    i = 0
    for stake_option in coins_stake_options:
        button = buttonCoins(button_coins_x[i], BUTTON_COINS_Y, BUTTON_COINS_RADIUS, stake_option, str(stake_option))
        buttons_select_amount_of_coins.append(button)
        i = i+1

def build_symbolbuttons():
    i = 0
    for symbol in symbols:
        button = buttonSymbols(passive_colors[i], active_colors[i], button_symbols_x[i], BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT,symbol)
        buttons_select_symbol.append(button)
        i = i + 1

def build_all_buttons():
    build_playerbuttons()
    build_coinbuttons()
    build_symbolbuttons()


# updating the state of the buttons in every loop
def update_configbuttons(events):
    global config_players

    # if a button is click -> set its status on True and all the other buttons of this category on False
    for button in buttons_select_symbol:
        button.draw(screen)
        if button.isClicked():
            button.setStatus(True)
            players_symbols[config_players] = button.getSymbol()
            for other in buttons_select_symbol:
                if button == other:
                    continue
                other.setStatus(False)

    # if a button is click -> set its status on True and all the other buttons of this category on False
    # additionally check if the player has enough coins available
    for button in buttons_select_amount_of_coins:
        button.draw(screen)
        if button.isClicked():
            if player_coins[config_players] >= button.getCoins():
                button.setStatus(True)
                players_stakes[config_players] = button.getCoins()
                for other in buttons_select_amount_of_coins:
                    if button == other:
                        continue
                    other.setStatus(False)
            else:
                print("Not enough coins available, select a smaller amount of coins.")

    # if a button is click -> set its status on True and all the other buttons of this category on False
    for button in button_select_player:
        button.draw(screen)
        if button.isClicked():
            button.setStatus(True)
            players_target[config_players] = button.getPlayer()
            for other in button_select_player:
                if button == other:
                    continue
                other.setStatus(False)


# function to count the seconds a player has to choose his options
def countdown():
    global init, counter, ticks, config_players, game_state
    if ticks % 10 == 0:
        if counter > 0:
            counter -= 1
        else:
            counter = 15
            # if not all 4 player took their decisions, reset the buttons and jump to the next player
            if config_players < 3:
                config_players += 1
                reset_buttons()
            # else translate to the next gaming phase
            else:
                config_players = 0
                draw_game_background()
                draw_all_aces()
                game_state = "game"



# function to reset the state of all buttons
def reset_buttons():
    for button in button_select_player:
        button.setStatus(False)
    for button in buttons_select_amount_of_coins:
        button.setStatus(False)
    for button in buttons_select_symbol:
        button.setStatus(False)

# function to reset the choices of the player after every round
def reset_choices():
    for i in range(4):
        players_symbols[i]=None
        players_stakes[i]=None
        players_target[i]=None


# function to offset the coins after every round
def offset_coins():
    global winner

    for i in range(4):
        # case either a symbol, amount of coins or player to snatch the coins from was not selected
        if players_symbols[i] == None or players_stakes[i] == None or players_target[i] == None:
            player_coins[i] -= 30
        # case the player selected the winner
        elif players_symbols[i] == winner:
            player_coins[i] += players_stakes[i]
            player_coins[players_target[i]] -= players_stakes[i]
        # case the player did not select the winner
        else:
            player_coins[i] -= players_stakes[i]

# function to check if any player has lost all his coins
def check_loser():
    global round_number
    for c in player_coins:
        if c <= 0:
            round_number = 5

# function to determine the sequence of winners
def get_winner_sequence():
    sequence = []
    for i in range(4):
        next_place = player_coins.index(max(player_coins))
        player_coins[next_place] = -150
        sequence.append("Player"+str(next_place+1))
    return sequence

# function to draw text on the screen
def draw_message(string, size, color, position_x, position_y, prefix=1):
    font = pg.font.Font(font_custom, size)
    message = font.render(string, True, color)
    text_width = message.get_size()[0]
    text_height = message.get_size()[1]
    if prefix == 0:
        screen.blit(message, [position_x - (text_width//2), position_y-text_height])
    elif prefix == 1:
        screen.blit(message, [position_x - (text_width//2), position_y])
    else:
        screen.blit(message, [position_x, position_y])

# function to draw the starting screen with instructions
def draw_init_screen():
    global screen
    draw_message("Welcome to horse-race",60,BLACK,SCREEN_WIDTH//2,10)
    draw_message("Players game goal:",20,BLACK, 10, SCREEN_HEIGHT-575,2)
    draw_message("Pick your golden horse which are embodied by the four aces of a skat set.",20,BLACK,10, SCREEN_HEIGHT- 550,2)
    draw_message("Set a respective amount of your coin budget as a stake. Either you will lose it or receive double profit.",20,BLACK,10, SCREEN_HEIGHT- 525,2)
    draw_message("The game contains 5 races but it ends when any player has no more coins available.",20,RED,10,SCREEN_HEIGHT-500,2)
    draw_message("The player with the highest final amount of coins will be crowned as the winner",20,BLACK,10,SCREEN_HEIGHT-475,2)
    draw_message("Configurations before every race:",20,BLACK,10,SCREEN_HEIGHT- 400,2)
    draw_message("1. Select a symbol you bet on", 20, BLACK,10,SCREEN_HEIGHT-375,2)
    draw_message("2. Enter an amount of coins as your stake", 20, BLACK,10,SCREEN_HEIGHT-350,2)
    draw_message("3. Pick a player you want to grab your potential profit from", 20, BLACK,10,SCREEN_HEIGHT-325,2)
    draw_message("Ready, steady, go!", 20, BLUE,10,SCREEN_HEIGHT-275,2)
    draw_message("Press an optional key for moving forward", 30, RED,SCREEN_WIDTH//2, SCREEN_HEIGHT-20,0)

# function to draw the configuration screen to take the choices for the coming race
def draw_config_text():
    global counter, config_players, round_number

    draw_message("CONFIGURATION: " + str(players[config_players]) + " ( you have "+ str(player_coins[config_players])+" coins left)", 35, BLACK, SCREEN_WIDTH//2, 10)
    draw_message("Select a symbol you bet up on", 25, LIGHT_GRAY, SCREEN_WIDTH//2, BUTTON_Y-40 )
    draw_message("Select an amount of Coins as a stake", 25, LIGHT_GRAY, SCREEN_WIDTH//2, BUTTON_COINS_Y-80 )
    draw_message("Select a player you want to snatch your potential profit from", 25, LIGHT_GRAY, SCREEN_WIDTH//2, BUTTON_PLAYERS_Y-40)
    draw_message("Round: {} of 5".format(round_number+1), 20, BLACK, SCREEN_WIDTH-80, SCREEN_HEIGHT-40 )
    draw_message("sec left. Else, you're going to lose 30 coins and get banned from the upcoming race.", 20, RED, 50, SCREEN_HEIGHT-40, 2)
    draw_message(str(counter), 30, BLACK, 10, SCREEN_HEIGHT-50, 2)


# function to draw the finish line of the racetrack
def draw_finish_line():
    finish_line_y_pos = Y_TRACK_START

    while finish_line_y_pos < Y_TRACK_FINISH:
        pg.draw.line(screen, BLACK, (X_TRACK_FINISH, finish_line_y_pos), (X_TRACK_FINISH, finish_line_y_pos + DISTANCE_DASHED_LINES))
        pg.draw.line(screen, WHITE, (X_TRACK_FINISH, finish_line_y_pos + DISTANCE_DASHED_LINES), (X_TRACK_FINISH, finish_line_y_pos + (DISTANCE_DASHED_LINES * 2)))
        finish_line_y_pos = finish_line_y_pos + (DISTANCE_DASHED_LINES * 2)

# function to draw dashed line on the sides of the track
def draw_lines_dashed():
    dashed_lines_x_pos = X_TRACK_START

    while dashed_lines_x_pos < (X_TRACK_START + 0.75 * TRACK_LENGTH):
        dashed_lines_y_pos = Y_TRACK_START + DISTANCE_DASHED_LINES / 2
        dashed_lines_x_pos = dashed_lines_x_pos + (0.25 * TRACK_LENGTH)
        while dashed_lines_y_pos < Y_TRACK_FINISH:
            pg.draw.line(screen, BLACK, (dashed_lines_x_pos, dashed_lines_y_pos), (dashed_lines_x_pos, dashed_lines_y_pos + DISTANCE_DASHED_LINES))
            dashed_lines_y_pos = dashed_lines_y_pos + (DISTANCE_DASHED_LINES * 2)

# function to draw text on the track
def draw_track_text():
    start_text = font.render("START", True, BLACK)
    start_text = pg.transform.rotate(start_text, 90)
    screen.blit(start_text, [X_TRACK_START - 20 - start_text.get_rect().width, ((Y_TRACK_FINISH + Y_TRACK_START - start_text.get_rect().height) / 2)])

    finish_text = font.render("FINISH", True, BLACK)
    finish_text = pg.transform.rotate(finish_text, 270)
    screen.blit(finish_text, [X_TRACK_FINISH + 20, ((Y_TRACK_FINISH + Y_TRACK_START - finish_text.get_rect().height) / 2)])

    round_text = font.render("Round " + str(round_number+1), True, BLACK)
    screen.blit(round_text, [(PLAYER_CORNER_WIDTH - round_text.get_rect().width) / 2, ((Y_TRACK_FINISH + Y_TRACK_START - round_text.get_rect().height) / 2)])

# function to draw the racetrack
def draw_track():
    pg.draw.line(screen, BLACK, (X_TRACK_START, Y_TRACK_START), (X_TRACK_FINISH, Y_TRACK_START))
    pg.draw.line(screen, BLACK, (X_TRACK_START, Y_TRACK_FINISH), (X_TRACK_FINISH, Y_TRACK_FINISH))
    pg.draw.line(screen, BLACK, (X_TRACK_START, Y_TRACK_START), (X_TRACK_START, Y_TRACK_FINISH))

    draw_finish_line()
    draw_lines_dashed()
    draw_track_text()

# function to draw the text above the card deck
def draw_card_deck_text():
    card_deck_text = font.render("DECK OF CARDS", True, BLACK)
    screen.blit(card_deck_text, [X_TRACK_FINISH + 70, Y_TRACK_START + 70])

# function to draw the card deck
def draw_card_deck():
    draw_card_deck_text()

    covered_card_x_pos = X_TRACK_FINISH + 70
    covered_card_y_pos = Y_TRACK_START + TRACK_HEIGHT / 2 - (CARD_HEIGHT + ADD_X_Y)

    while covered_card_y_pos <= Y_TRACK_START + TRACK_HEIGHT / 2 - (CARD_HEIGHT - ADD_X_Y):
        pg.draw.rect(screen, BLACK, pg.Rect(covered_card_x_pos, covered_card_y_pos, CARD_WIDTH, CARD_HEIGHT),  0, 3)
        covered_card_x_pos = covered_card_x_pos + ADD_X_Y
        covered_card_y_pos = covered_card_y_pos + ADD_X_Y

# function to draw the selected symbol, budget and stake for this race (for each player)
def draw_player_selection():
    pg.draw.rect(screen, BLACK, pg.Rect(0, 0, PLAYER_CORNER_WIDTH, PLAYER_CORNER_HEIGHT), 1)
    pg.draw.rect(screen, BLACK, pg.Rect(W - PLAYER_CORNER_WIDTH, 0, PLAYER_CORNER_WIDTH, PLAYER_CORNER_HEIGHT),  1)
    pg.draw.rect(screen, BLACK, pg.Rect(0, H - PLAYER_CORNER_HEIGHT, PLAYER_CORNER_WIDTH, PLAYER_CORNER_HEIGHT),  1)
    pg.draw.rect(screen, BLACK, pg.Rect(W - PLAYER_CORNER_WIDTH, H - PLAYER_CORNER_HEIGHT, PLAYER_CORNER_WIDTH, PLAYER_CORNER_HEIGHT),  1)

    draw_message("Player 1: "+str(players_symbols[0]), 20, BLACK, STANDARD_DISTANCE, STANDARD_DISTANCE,2)
    draw_message("Budget: "+str(player_coins[0]), 20, BLACK, STANDARD_DISTANCE, STANDARD_DISTANCE*4,2)
    draw_message("Stake: "+str(players_stakes[0]), 20, BLACK, STANDARD_DISTANCE, STANDARD_DISTANCE*7,2)

    draw_message("Player 2: "+str(players_symbols[1]), 20, BLACK, W - PLAYER_CORNER_WIDTH + STANDARD_DISTANCE, STANDARD_DISTANCE,2)
    draw_message("Budget: "+str(player_coins[1]), 20, BLACK,W - PLAYER_CORNER_WIDTH + STANDARD_DISTANCE, STANDARD_DISTANCE*4,2)
    draw_message("Stake: "+str(players_stakes[1]), 20, BLACK,W - PLAYER_CORNER_WIDTH + STANDARD_DISTANCE, STANDARD_DISTANCE*7,2)

    draw_message("Player 3: "+str(players_symbols[2]), 20, BLACK, STANDARD_DISTANCE, H - PLAYER_CORNER_HEIGHT + STANDARD_DISTANCE,2)
    draw_message("Budget: "+str(player_coins[2]), 20, BLACK, STANDARD_DISTANCE,  H - PLAYER_CORNER_HEIGHT + STANDARD_DISTANCE*4,2)
    draw_message("Stake: "+str(players_stakes[2]), 20, BLACK, STANDARD_DISTANCE, H - PLAYER_CORNER_HEIGHT + STANDARD_DISTANCE*7,2)

    draw_message("Player 4: "+str(players_symbols[3]), 20, BLACK, W - PLAYER_CORNER_WIDTH + STANDARD_DISTANCE, H - PLAYER_CORNER_HEIGHT + STANDARD_DISTANCE,2)
    draw_message("Budget: "+str(player_coins[3]), 20, BLACK,W - PLAYER_CORNER_WIDTH + STANDARD_DISTANCE, H - PLAYER_CORNER_HEIGHT + STANDARD_DISTANCE*4,2)
    draw_message("Stake: "+str(players_stakes[3]), 20, BLACK,W - PLAYER_CORNER_WIDTH + STANDARD_DISTANCE, H - PLAYER_CORNER_HEIGHT + STANDARD_DISTANCE*7,2)

# function to draw the covered card on the side of the track
def draw_covered_cards():
    pg.draw.rect(screen, BLACK, pg.Rect(x_pos[1] + STANDARD_DISTANCE, Y_TRACK_START - STANDARD_DISTANCE - CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    pg.draw.rect(screen, BLACK, pg.Rect(x_pos[2] + STANDARD_DISTANCE, Y_TRACK_START - STANDARD_DISTANCE - CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    pg.draw.rect(screen, BLACK, pg.Rect(x_pos[3] + STANDARD_DISTANCE, Y_TRACK_START - STANDARD_DISTANCE - CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT),  0, 3)

# function to draw the background (everything except the aces and face-up cards)
def draw_game_background():
    screen.fill(LIGHT_GOLDEN)
    draw_track()
    draw_card_deck()
    draw_player_selection()
    draw_covered_cards()

# function to draw each ace
def draw_ace_diamonds():
    pg.draw.rect(screen, WHITE, pg.Rect(x_pos[pos_diamonds], Y_DIAMONDS, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    pg.draw.rect(screen, RED, pg.Rect(x_pos[pos_diamonds] + 0.5 * STANDARD_DISTANCE, Y_DIAMONDS + 0.5 * STANDARD_DISTANCE, CARD_WIDTH - STANDARD_DISTANCE, CARD_HEIGHT - STANDARD_DISTANCE),  1, 3)
    ace_diamonds = font.render("\u2662Ace", True, RED)
    screen.blit(ace_diamonds, [x_pos[pos_diamonds] + (CARD_WIDTH - ace_diamonds.get_rect().width) / 2, Y_DIAMONDS + (CARD_HEIGHT - ace_diamonds.get_rect().height) / 2])

def draw_ace_hearts():
    pg.draw.rect(screen, WHITE, pg.Rect(x_pos[pos_hearts], Y_HEARTS, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    pg.draw.rect(screen, RED, pg.Rect(x_pos[pos_hearts] + 0.5 * STANDARD_DISTANCE, Y_HEARTS + 0.5 * STANDARD_DISTANCE, CARD_WIDTH - STANDARD_DISTANCE, CARD_HEIGHT - STANDARD_DISTANCE),  1, 3)
    ace_hearts = font.render("\u2661Ace", True, RED)
    screen.blit(ace_hearts, [x_pos[pos_hearts] + (CARD_WIDTH - ace_hearts.get_rect().width) / 2, Y_HEARTS + (CARD_HEIGHT - ace_hearts.get_rect().height) / 2])

def draw_ace_spades():
    pg.draw.rect(screen, WHITE, pg.Rect(x_pos[pos_spades], Y_SPADES, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    pg.draw.rect(screen, BLACK, pg.Rect(x_pos[pos_spades] + 0.5 * STANDARD_DISTANCE, Y_SPADES + 0.5 * STANDARD_DISTANCE, CARD_WIDTH - STANDARD_DISTANCE, CARD_HEIGHT - STANDARD_DISTANCE),  1, 3)
    ace_spades = font.render("\u2660Ace", True, BLACK)
    screen.blit(ace_spades, [x_pos[pos_spades] + (CARD_WIDTH - ace_spades.get_rect().width) / 2, Y_SPADES + (CARD_HEIGHT - ace_spades.get_rect().height) / 2])

def draw_ace_clubs():
    pg.draw.rect(screen, WHITE, pg.Rect(x_pos[pos_clubs], Y_CLUBS, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    pg.draw.rect(screen, BLACK, pg.Rect(x_pos[pos_clubs] + 0.5 * STANDARD_DISTANCE, Y_CLUBS + 0.5 * STANDARD_DISTANCE, CARD_WIDTH - STANDARD_DISTANCE, CARD_HEIGHT - STANDARD_DISTANCE),  1, 3)
    ace_clubs = font.render("\u2663Ace", True, BLACK)
    screen.blit(ace_clubs, [x_pos[pos_clubs] + (CARD_WIDTH - ace_clubs.get_rect().width) / 2, Y_CLUBS + (CARD_HEIGHT - ace_clubs.get_rect().height) / 2])


# function to execute the draw functions for each ace
def draw_all_aces():
    global pos_diamonds, pos_hearts, pos_spades, pos_clubs

    for number in x_pos:
        pg.draw.rect(screen, LIGHT_GRAY, pg.Rect(number, Y_DIAMONDS, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    draw_ace_diamonds()

    for number in x_pos:
        pg.draw.rect(screen, LIGHT_GRAY, pg.Rect(number, Y_HEARTS, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    draw_ace_hearts()

    for number in x_pos:
        pg.draw.rect(screen, LIGHT_GRAY, pg.Rect(number, Y_SPADES, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    draw_ace_spades()

    for number in x_pos:
        pg.draw.rect(screen, LIGHT_GRAY, pg.Rect(number, Y_CLUBS, CARD_WIDTH, CARD_HEIGHT),  0, 3)
    draw_ace_clubs()

# function to draw to result (winner) of the race
def draw_round_result():
    global winner

    pg.draw.rect(screen, WHITE, pg.Rect(W/2 - 1.5 * CARD_WIDTH, H/2 - 1.5 * CARD_HEIGHT, 3 * CARD_WIDTH, 1.5 * CARD_HEIGHT),  0, 3)
    headline_text = font.render(cards[3][:1] + " has won Round " + str(round_number) + "!", True, BLACK)
    text_width = headline_text.get_size()[0]
    screen.blit(headline_text, [(W - text_width) / 2, (H - text_width) / 2])

    winner = cards[3][:1]

# function to reveal a new staple card
def show_new_card_from_stapel():
    global pos_diamonds, pos_hearts, pos_spades, pos_clubs

    pg.draw.rect(screen, WHITE, pg.Rect(CARD_POS0[0], CARD_POS0[1], CARD_WIDTH, CARD_HEIGHT),  0, 3)

    if (cards[3].startswith("\u2662") or cards[3].startswith("\u2661")):
        pg.draw.rect(screen, RED, pg.Rect(CARD_POS0[0]+ 0.5 * STANDARD_DISTANCE, CARD_POS0[1]+ 0.5 * STANDARD_DISTANCE , CARD_WIDTH - STANDARD_DISTANCE, CARD_HEIGHT - STANDARD_DISTANCE),  1, 3)
        card_to_draw = font.render(cards[3], True, RED)
        screen.blit(card_to_draw, [CARD_POS0[0] + (CARD_WIDTH - card_to_draw.get_rect().width) / 2, CARD_POS0[1] + (CARD_HEIGHT - card_to_draw.get_rect().height) / 2])
    else:
        pg.draw.rect(screen, BLACK, pg.Rect(CARD_POS0[0]+ 0.5 * STANDARD_DISTANCE, CARD_POS0[1]+ 0.5 * STANDARD_DISTANCE , CARD_WIDTH - STANDARD_DISTANCE, CARD_HEIGHT - STANDARD_DISTANCE),  1, 3)
        card_to_draw = font.render(cards[3], True, BLACK)
        screen.blit(card_to_draw, [CARD_POS0[0] + (CARD_WIDTH - card_to_draw.get_rect().width) / 2, CARD_POS0[1] + (CARD_HEIGHT - card_to_draw.get_rect().height) / 2])

    if (cards[3].startswith("\u2662")):
        pos_diamonds = pos_diamonds + 1
        if(pos_diamonds < 4):
            cards.pop(3)
    elif (cards[3].startswith("\u2661")):
        pos_hearts = pos_hearts + 1
        if(pos_hearts < 4):
            cards.pop(3)
    elif (cards[3].startswith("\u2660")):
        pos_spades = pos_spades + 1
        if(pos_spades < 4):
            cards.pop(3)
    elif (cards[3].startswith("\u2663")):
        pos_clubs = pos_clubs + 1
        if(pos_clubs < 4):
            cards.pop(3)

# function to reveal a new trackside card
def show_new_trackside_card():
    global track_card1_covered, track_card2_covered, track_card3_covered, pos_diamonds, pos_hearts, pos_spades, pos_clubs

    # reveal 3rd trackside card
    if (pos_diamonds == 3 and pos_hearts == 3 and pos_spades == 3 and pos_clubs == 3):
        x_reveal = CARD_POS3[0]
        y_reveal = CARD_POS3[1]
        index_reveal = 2
        track_card3_covered = False

    # reveal 2nd trackside card
    elif (pos_diamonds >= 2 and pos_hearts >= 2 and pos_spades >= 2 and pos_clubs >= 2):
        x_reveal = CARD_POS2[0]
        y_reveal = CARD_POS2[1]
        index_reveal = 1
        track_card2_covered = False

    # reveal 1st trackside card
    elif (pos_diamonds >= 1 and pos_hearts >= 1 and pos_spades >= 1 and pos_clubs >= 1):
        x_reveal = CARD_POS1[0]
        y_reveal = CARD_POS1[1]
        index_reveal = 0
        track_card1_covered = False

    else:
        return

    pg.draw.rect(screen, WHITE, pg.Rect(x_reveal, y_reveal, CARD_WIDTH, CARD_HEIGHT),  0, 3)

    if (cards[index_reveal].startswith("\u2662") or cards[index_reveal].startswith("\u2661")):
        pg.draw.rect(screen, RED, pg.Rect(x_reveal + 0.5 * STANDARD_DISTANCE, y_reveal + 0.5 * STANDARD_DISTANCE , CARD_WIDTH - STANDARD_DISTANCE, CARD_HEIGHT - STANDARD_DISTANCE),  1, 3)
        card_to_draw = font.render(cards[index_reveal], True, RED)
        screen.blit(card_to_draw, [x_reveal + (CARD_WIDTH - card_to_draw.get_rect().width) / 2, y_reveal + (CARD_HEIGHT - card_to_draw.get_rect().height) / 2])
    else:
        pg.draw.rect(screen, BLACK, pg.Rect(x_reveal + 0.5 * STANDARD_DISTANCE, y_reveal + 0.5 * STANDARD_DISTANCE , CARD_WIDTH - STANDARD_DISTANCE, CARD_HEIGHT - STANDARD_DISTANCE),  1, 3)
        card_to_draw = font.render(cards[index_reveal], True, BLACK)
        screen.blit(card_to_draw, [x_reveal + (CARD_WIDTH - card_to_draw.get_rect().width) / 2, y_reveal + (CARD_HEIGHT - card_to_draw.get_rect().height) / 2])

    # move diamond ace backwards if the revealed card has the diamond symbol
    if (cards[index_reveal].startswith("\u2662")):
        pos_diamonds = pos_diamonds - 1

    # move heart ace backwards if the revealed card has the heart symbol
    elif (cards[index_reveal].startswith("\u2661")):
        pos_hearts = pos_hearts - 1

    # move spade ace backwards if the revealed card has the spade symbol
    elif (cards[index_reveal].startswith("\u2660")):
        pos_spades = pos_spades - 1

    # move club ace backwards if the revealed card has the club symbol
    elif (cards[index_reveal].startswith("\u2663")):
        pos_clubs = pos_clubs - 1


# function that is executed as long as the game state is "init"
def function_state_init(events):
    global running, screen, init_state, game_state

    screen.fill(LIGHT_GOLDEN)
    draw_init_screen()

    # if any key is pressed, continue with the next phase
    for event in events:
        if event.type == KEYDOWN:
            game_state = "config"
            init_state = True
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


# # function that is executed as long as the game state is "config"
def function_state_config(events):
    global running, screen, init_state, game_state, counter, config_players

    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # draws the configurations menu, updates the buttons and runs the countdown
    screen.fill(LIGHT_GOLDEN)
    draw_config_text()
    update_configbuttons(events)
    countdown()


# function that is executed as long as the game state is "game"
def function_state_game():
    global pos_diamonds, pos_hearts, pos_spades, pos_clubs, game_state, ticks, round_number

    if ticks % 5 == 0:
        # reveal either a trackside card or staple card
        if (track_card1_covered == True and pos_diamonds >= 1 and pos_hearts >= 1 and pos_spades >= 1 and pos_clubs >= 1):
            show_new_trackside_card()
        elif (track_card2_covered == True and pos_diamonds >= 2 and pos_hearts >= 2 and pos_spades >= 2 and pos_clubs >= 2):
            show_new_trackside_card()
        elif (track_card3_covered == True and pos_diamonds >= 3 and pos_hearts >= 3 and pos_spades >= 3 and pos_clubs >= 3):
            show_new_trackside_card()
        else:
            show_new_card_from_stapel()

        # if one ace reaches the finish line, continue to the next phase
        if (pos_diamonds >= 4 or  pos_hearts >= 4 or pos_spades >= 4 or pos_clubs >= 4):
            pg.draw.rect(screen, WHITE, pg.Rect(CARD_POS0[0], CARD_POS0[1], CARD_WIDTH, CARD_HEIGHT),  0, 3)
            ticks = 0
            round_number = round_number + 1
            game_state = "end"
        else:
            draw_all_aces()


## function that is executed as long as the game state is "end"
def function_state_end():
    global pos_diamonds, pos_hearts, pos_spades, pos_clubs, game_state, ticks, round_number, track_card1_covered,track_card2_covered,track_card3_covered, cards, winners

    # reset the racetrack and positions of the aces, shuffle the cards for the next round
    if ticks == 1:
        show_new_card_from_stapel()
        draw_round_result()

        symbols = ["\u2660", "\u2661", "\u2662","\u2663"]
        values = ["7", "8", "9", "10", "Jack", "Queen", "King"]

        cards = []
        for s in symbols:
            for v in values:
                cards.append(s+v)

        random.shuffle(cards)

        track_card1_covered = True
        track_card2_covered = True
        track_card3_covered = True

        pos_diamonds = 0
        pos_hearts = 0
        pos_spades = 0
        pos_clubs = 0


    # offset the coins and check if any player lost all his coins
    if ticks == 50:
        ticks = 0
        offset_coins()
        check_loser()
        # if the game is over, continue with the last phase
        if (round_number == 5):
            game_state = "results"
            winners = get_winner_sequence()
        # else reset player choices / buttons and repeat the configuration phase
        else:
            game_state = "config"
            reset_choices()
            reset_buttons()

# function that is executed as long as the game state is "result"
def function_state_result():
    global winners

    screen.fill(LIGHT_GOLDEN)
    font = pg.font.Font('seguisym.ttf', 30)

    headline_text = font.render("Results:", True, LIGHT_RED)

    text_width = headline_text.get_size()[0]
    screen.blit(headline_text, [(W - text_width) / 2, (H - text_width) / 6])

    # draw the winners in the correct order
    headline_text = font.render("1. "+ winners[0], True, BLACK)
    text_width = headline_text.get_size()[0]
    screen.blit(headline_text, [(W - text_width) / 2, (H - text_width) / 6 * 2])

    headline_text = font.render("2. "+ winners[1], True, BLACK)
    text_width = headline_text.get_size()[0]
    screen.blit(headline_text, [(W - text_width) / 2, (H - text_width) / 6 * 3])

    headline_text = font.render("3. "+ winners[2], True, BLACK)
    text_width = headline_text.get_size()[0]
    screen.blit(headline_text, [(W - text_width) / 2, (H - text_width) / 6 * 4])

    headline_text = font.render("4. "+ winners[3], True, BLACK)
    text_width = headline_text.get_size()[0]
    screen.blit(headline_text, [(W - text_width) / 2, (H - text_width) / 6 * 5])



# initialize pygame
pg.init()

# creating the game screen and initializing the font
screen = pg.display.set_mode([W,H])

pg.font.init()
font = pg.font.Font('seguisym.ttf', 20)

# build the buttons (but do not drwa them) and set a caption
build_all_buttons()
pg.display.set_caption("Horse Race")

# setting various global variables for the start of the game
counter = 15
config_players = 0
game_state = "init"
running = True
ticks = 0
round_number = 0

# main loop of the game, execute different functions depending on the game state
while running:
    global event_list
    event_list = pg.event.get()

    if game_state == "init":
        function_state_init(event_list)

    elif game_state == "config":
        function_state_config(event_list)

    elif game_state == "game":
        function_state_game()

    elif game_state == "end":
        function_state_end()

    if game_state == "results":
        function_state_result()

    for event in event_list:
        if event.type == pg.QUIT:
            running = False
            pg.quit()
            exit()

    # update window and set refresh rate
    pg.display.flip()
    clock.tick(10)
    ticks += 1

pg.quit()
